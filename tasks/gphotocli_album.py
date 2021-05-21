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

from tasks.gphotocli_album_tasks import GphotoAlbumCLITasks
from tasks.gphotocli_album_task_map import GphotoAlbumCLITaskMap

class GphotoAlbumCLI(object):
    """Module to handle Google album specific commands"""

    def __init__(self):
        self._gphotocli_album_tasks = GphotoAlbumCLITasks()
        self._gphotocli_album_task_map = GphotoAlbumCLITaskMap()

    # -------------------------------------------------
    def upload(self, root):
        """Create shareable albums for 'root' and its subfolders"""
        self._gphotocli_album_tasks.upload(root)

    # -------------------------------------------------
    def map(self, root):
        """Given local album folder pattern, map all albums to their images"""
        self._gphotocli_album_task_map.map(root)

    # -------------------------------------------------
    def get(self, title=None, id=None):
        """Return 'album' object given the 'title' or 'id'"""
        return self._gphotocli_album_tasks(title, id)
