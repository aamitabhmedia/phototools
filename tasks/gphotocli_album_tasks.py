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

class GphotoCLIAlbumTasks(object):
    """Module to handle Google album specific commands"""

    def __init__(self):
        LocalLibrary.load_library('jpg')
        GoogleLibrary.load_library()
        self.modified = False

    # -------------------------------------------------
    def create_shareable_album(self, service, album_name, test):

        # Create google album
        request_body = {
            'album': {
                'title': album_name
            }
        }

        if test:
            logging.info(f"Test Album Create: {album_name}")
            return None

        album_create_response = service.albums().create(body=request_body).execute()
        google_album_id = album_create_response.get('id')
        logging.info(f"Album Created: {album_create_response}")

        # Make Google album sharable
        request_body = {
            'sharedAlbumOptions': {
                'isCollaborative': True,
                'isCommentable': True
            }
        }
        album_share_response = service.albums().share(
            albumId=google_album_id,
            body=request_body
        ).execute()

        # Now get the album from Google to see if it has been created as shareable
        album_get_response = service.albums().get(albumId=google_album_id).execute()

        # We will now add it to our local cache and save the cache
        google_cache = GoogleLibrary.cache()
        google_album_ids = google_cache.get('album_ids')
        google_album_titles = google_cache.get('album_titles')

        if album_get_response is not None:
            GoogleLibrary.cache_album(
                album_get_response,
                google_album_ids,
                google_album_titles,shared=True)

        return album_get_response

    # -------------------------------------------------
    def upload_recursive(self, root, test):

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

        # Traverse all the sub folders in the cache
        local_cache = LocalLibrary.cache('jpg')
        local_albums = local_cache.get('albums')

        for local_album in local_albums:

            local_album_name = local_album['name']
            local_album_path = local_album['path']

            if not local_album_path.lower().startswith(root.lower()):
                continue

            # Check if album already in Google Cache
            google_album_id = google_album_titles.get(local_album_name)
            google_album = google_album_ids[google_album_id] if google_album_id is not None else None

            if google_album is not None:
                logging.info(f"Album already uploaded: '{google_album.get('title')}'")
                continue

            # Do the actual creating of Google album
            album_response = self.create_shareable_album(service=service, album_name=local_album_name, test=test)
            if album_response:
                self.modified = True

    # -------------------------------------------------
    def upload(self, root, test=False):
        self.modified = False

        try:
            self.upload_recursive(root, test)

        finally:
            if self.modified:
                GoogleLibrary.save_library()

