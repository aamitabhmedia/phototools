import context; context.set_context()

import os
import logging
import json
import fire
from datetime import datetime

import gphoto
from googleapi.google_service import GoogleService
from gphoto.google_library import GoogleLibrary
from gphoto.local_library import LocalLibrary

class GphotoAlbumCLITasks(object):
    """Module to handle Google album specific commands"""

    def __init__(self):
        LocalLibrary.load_library('jpg')
        GoogleLibrary.load_library()
        self.modified = False

    # -------------------------------------------------
    def map_recursive(self, root):
        """
        High-level algorithm:
        1. For each local folder locate the Google album in cache
        2. If Google album does not exist then call 'gphotocli album upload <...path_to_album...>'
        3. 
        """


    # -------------------------------------------------
    def map(self, root):
        self.modified = False
        self.map_recursive(root)
        if self.modified:
            GoogleLibrary.save_library()
