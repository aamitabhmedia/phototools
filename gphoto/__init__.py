"""
gphoto has packages to work with local albums and google api
Here is how to use it after you import gphoto:
>>> gphoto.init()
>>> ....cal any other function...
"""

from gphoto import core

def init():
    """
    Initializes:
        AppData variables
        LogMgr
        GoogleService
    """
    core.init()