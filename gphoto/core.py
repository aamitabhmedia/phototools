from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

def init():
    AppData.init()
    LogMgr.init(AppData.APPDATA_NAME, "gphoto.log")
    GoogleService.init()