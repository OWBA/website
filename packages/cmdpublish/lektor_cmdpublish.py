# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from lektor.publisher import Publisher
import subprocess


class SysCmdPublisher(Publisher):
    def publish(self, target_url, credentials=None, **extra):
        cmd = "{} {}".format(target_url.host, target_url.path[1:])
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE) as proc:
            for line in proc.stdout:
                yield line[:-1].decode("utf-8")


class CmdPublishPlugin(Plugin):
    name = u'CmdPublish'
    description = u'Lektor plugin to perform system commands. e.g., git commit'

    def on_setup_env(self, **extra):
        self.env.add_publisher('cmd', SysCmdPublisher)
