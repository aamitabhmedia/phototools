import context; context.set_context()

import os
import logging
import json
import fire
from datetime import datetime

import gphoto
from tasks.gphotocli_album_tasks import GphotoAlbumCLITasks

from googleapi.google_service import GoogleService
from gphoto.google_library import GoogleLibrary
from gphoto.local_library import LocalLibrary


class GphotoAlbumCLI(object):
    """Module to handle Google album specific commands"""

    def __init__(self):
        self._gphotocli_album_tasks = GphotoAlbumCLITasks()

    # -------------------------------------------------
    def upload_tree(self, root):
        """Create albums in the root folder, and make all albums shareable"""
        self._gphotocli_album_tasks.upload_tree(root)

    # -------------------------------------------------
    def get(self, title=None, id=None):
        """Return 'album' object given the 'title' or 'id'"""
        return self._gphotocli_album_tasks(title, id)
