# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from lektor.publisher import Publisher, Command


class PathPublisher(Publisher):
    def publish(self, target_url, credentials=None, **extra):
        cmd = [
            'rsync', '-rclzv', '--delete',
            '--exclude=.lektor', '--exclude=.git/', '--exclude=.DS_Store']

        cmd.append(self.output_path.rstrip('/\\') + '/')
        cmd.append((target_url.host or '') + target_url.path.rstrip('/') + '/')

        for line in Command(cmd):
            yield line


class PathPublishPlugin(Plugin):
    name = u'PathPublish'
    description = u'Lektor plugin to publish your site to a local path.'

    def on_setup_env(self, **extra):
        self.env.add_publisher('path', PathPublisher)
