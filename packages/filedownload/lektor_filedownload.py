# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from lektor.reporter import reporter
import os
import urllib.request as curl
import urllib.error as webError


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
            try:
                curl.urlretrieve(src_url, dest)
                success = True
            except webError.HTTPError:
                success = False
            self.ongoing.remove(dest)
            return success

        def dl_yt_cover(vid, dest_dir, quality='maxres'):
            # vid = sender._data['vid']
            pth = os.path.join(dest_dir, 'yt-{}.jpg'.format(vid))
            if not vid:
                return pth
            # try with highest desired and available resolution first,
            # fallback to lower res if needed
            success = False
            url = 'https://i.ytimg.com/vi/{}'.format(vid)
            if not success and quality == 'maxres':
                success = dl_file(url + '/maxresdefault.jpg', pth)
                quality = 'hq'
            if not success and quality == 'hq':
                success = dl_file(url + '/hqdefault.jpg', pth)
            if not success:
                success = dl_file(url + '/default.jpg', pth)
            return pth

        self.env.jinja_env.globals['yt_cover'] = dl_yt_cover
