from re import I
import context; context.set_context()

import fire

from util.appdata import AppData
from util.log_mgr import LogMgr

from tasks.gphotocli_album import GphotoAlbumCLI
from tasks.gphotocli_image import GphotoImageCLI

class Root(object):

    def __init__(self):
        self.album = GphotoAlbumCLI()
        self.image = GphotoImageCLI()

    def run(self):
        # self.ingestion.run()
        # self.digestion.run()
        return 'Root complete'


if __name__ == '__main__':
    AppData.init()
    LogMgr.init(AppData.APPDATA_NAME, LogMgr.DEFAULT_LOGNAME)
    fire.Fire(Root)
