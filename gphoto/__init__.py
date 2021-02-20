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

# ---------------------------------------------
# Core functions
# ---------------------------------------------
def init():
    """
    Default initializes:
        AppData variables
        LogMgr
        GoogleService
    """
    core.init()

# ---------------------------------------------
# Cache functions
# ---------------------------------------------
def cache_dir():
    """
    Folder location on disk where pics folder
    and Google Photos data is cached
    """
    return CacheUtil.cache_dir()

# ---------------------------------------------
# Save Cache to file functions
# ---------------------------------------------
def save_to_file(cache, filename):
    CacheUtil.save_to_file(cache, filename)

# ---------------------------------------------
# Load Cache from file
# ---------------------------------------------
def load_from_file(filename):
    return CacheUtil.load_from_file(filename)

