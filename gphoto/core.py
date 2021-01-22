from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".nef", ".cr2"]

def init():
    AppData.init()
    LogMgr.init(AppData.APPDATA_NAME, "gphoto.log")
    GoogleService.init()