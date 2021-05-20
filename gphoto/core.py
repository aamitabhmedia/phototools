import pathlib

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.nef', '.cr2']
VIDEO_EXTENSIONS = ['.mp4', '.mov', '.avi']
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS
IGNORE_FOLDERS = ['corrupted', 'raw', 'undelete', 'misc', 'orig', 'ipPhone', 'praw', 'craw', 'cr2']

def init():
    AppData.init()
    LogMgr.init(AppData.APPDATA_NAME, LogMgr.DEFAULT_LOGNAME)
    GoogleService.init()

def get_image_mime(image_name):

    mime = None
    fileext = pathlib.Path(image_name).suffix.lower()
    if fileext in VIDEO_EXTENSIONS:
        mime_ext = fileext[1:]
        if fileext == '.mov':
            mime_ext = 'quicktime'
        elif fileext == '.avi':
            mime_ext = 'x-msvideo'
        mime = f"video/{mime_ext}"
    else:
        mime_ext = fileext[1:]
        if fileext == '.jpg':
            mime_ext = 'jpeg'
        mime = f"image/{mime_ext}"

    return mime