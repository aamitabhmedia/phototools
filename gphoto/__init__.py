"""
gphoto has packages to work with local albums and google api
Here is how to use it after you import gphoto:
>>> gphoto.init()
>>> ....cal any other function...
"""

from gphoto import core
from gphoto import cache_util

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
    return cache_util.CacheUtil.cache_dir()
