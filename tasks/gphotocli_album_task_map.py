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

class GphotoCLIAlbumTaskMap(object):
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
            - Add local images to Google Album from the Local album if missing
            - Remove images from Google album that are not in Local album
        """
        # Argument validation
        if not os.path.exists(root):
            logging.error(f"Folder does not exist: ({root})")
            return

        # Remove trailing slash
        slash_char = root[len(root) - 1]
        if slash_char == '/' or slash_char == '\\':
            root = root[:len(root)-1]

        # Get Google API service
        service = GoogleService.service()

        # Initialize Google API and load cache.
        google_cache = GoogleLibrary.cache()
        google_album_ids = google_cache.get('album_ids')
        google_album_titles = google_cache.get('album_titles')

        # Load local library cache
        local_cache = LocalLibrary.cache('jpg')
        local_albums = local_cache.get('albums')

        # Traverse all the sub folders in the cache
        for local_album in local_albums:

            local_album_name = local_album['name']
            local_album_path = local_album['path']

            if not local_album_path.lower().startswith(root.lower()):
                continue

            # Check if album already in Google Cache
            google_album_id = google_album_titles.get(local_album_name)
            google_album = google_album_ids[google_album_id] if google_album_id is not None else None

            # Google album not in cache. Error out
            if google_album is None:
                logging.error(f"Album already uploaded: '{google_album.get('title')}'")
                continue

            # Do the actual creating of Google album
            album_response = self.create_shareable_album(service=service, album_name=local_album_name)
            if album_response:
                self.modified = True

    # -------------------------------------------------
    def map(self, root):
        self.modified = False
        self.map_recursive(root)
        if self.modified:
            GoogleLibrary.save_library()
