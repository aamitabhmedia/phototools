"""
gphoto has packages to work with local albums and google api
Here is how to use it after you import gphoto:
>>> gphoto.init()
>>> ....cal any other function...
"""

from gphoto.google_images import GoogleImages
from gphoto.google_albums import GoogleAlbums
from gphoto import core
from gphoto.cache_util import CacheUtil
from gphoto.google_library import GoogleLibrary

def init():
    """
    Initializes:
        AppData variables
        LogMgr
        GoogleService
    """
    core.init()

def cache_dir():
    """
    Folder location on disk where pics folder
    and Google Photos data is cached
    """
    return CacheUtil.cache_dir()

def download_google_library():
    """
    Get an in-memory cache of Google Photos albums and images
    Also, save both the caches to local cache files
    Make sure to call gphoto.init() first
    """
    GoogleLibrary.download_library()

def load_google_library():
    """
    Load from local cache file to in-memory Google Photos albums and images
    It is good practice to call gphoto.init() first
    """
    GoogleLibrary.load_library()

def google_album_cache():
    """Returns the Google Photos album cache handle
    """
    return GoogleAlbums.cache()

def google_images_cache():
    """Returns the Google Photos album cache handle
    """
    return GoogleImages.cache()


