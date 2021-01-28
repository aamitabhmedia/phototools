from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".nef", ".cr2", ".mp4", ".mov"]
VIDEO_EXTENSIONS = [".mp4", ".mov"]
IGNORE_FOLDERS = ['corrupted', 'raw', 'undelete', 'misc', 'orig', 'ipPhone', 'praw', 'craw', 'cr2']

def init():
    AppData.init()
    LogMgr.init(AppData.APPDATA_NAME, "phototools.log")
    GoogleService.init()