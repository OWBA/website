# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from lektor.publisher import Publisher, Command
from subprocess import Popen, PIPE, STDOUT


def execute_command(params):
    with Command(params) as pipe:
        for line in pipe:
            yield line


def execute_shell(cmd):
    with Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT) as pipe:
        for line in pipe.stdout:
            yield line[:-1].decode('utf-8')


class MyLocalRsyncPublisher(Publisher):
    def publish(self, target_url, credentials=None, **extra):
        options = extra['server_info'].extra
        cmd = [
            'rsync', '-rclzv', '--delete', '--no-motd',
            '--exclude=.lektor', '--exclude=.git/', '--exclude=.DS_Store']

        if options.get('dryrun') in ['yes', 'true', '1']:
            cmd.append('--dry-run')

        cmd.append(self.output_path.rstrip('/\\') + '/')
        cmd.append(options['destination'].rstrip('/') + '/')
        yield from execute_command(cmd)


class MyGitPublisher(Publisher):
    def publish(self, target_url, credentials=None, **extra):
        if target_url.host == 'push':
            yield from execute_shell(
                'git add * && git commit -m "Automerge changes"; git push')
        else:
            yield from execute_command(['git', target_url.host])


class MyCmdPublisher(Publisher):
    def publish(self, target_url, credentials=None, **extra):
        cmd = '{} {}'.format(target_url.host, target_url.path[1:])
        yield from execute_shell(cmd)


class MyPublishPlugin(Plugin):
    name = u'MyPublish'
    description = u'Lektor plugin to perform system commands. e.g., git commit'

    def on_setup_env(self, **extra):
        self.env.add_publisher('cmd', MyCmdPublisher)
        self.env.add_publisher('git', MyGitPublisher)
        self.env.add_publisher('lrsync', MyLocalRsyncPublisher)
