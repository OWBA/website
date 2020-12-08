# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from lektor.reporter import reporter
import os
import urllib.request as curl


class FileDownloadPlugin(Plugin):
    name = u'FileDownload'
    description = u'Lektor plugin to download files from the internet.'
    ongoing = []

    def on_setup_env(self, **extra):
        def dl_file(src_url, tgt_file):
            dest = os.path.join(self.env.root_path, 'content' + tgt_file)
            if os.path.isfile(dest) or dest in self.ongoing:
                return  # exists or in progress
            self.ongoing.append(dest)
            reporter.report_generic('Download: ' + src_url)
            curl.urlretrieve(src_url, dest)
            self.ongoing.remove(dest)

        def dl_yt_cover(vid, dest_dir, quality='maxres'):
            # vid = sender._data['vid']
            pth = os.path.join(dest_dir, f'yt-{vid}.jpg')
            dl_file(f'https://i.ytimg.com/vi/{vid}/{quality}default.jpg', pth)
            return pth

        self.env.jinja_env.globals['yt_cover'] = dl_yt_cover
