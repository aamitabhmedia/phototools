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
    def upload_recursive(self, root):

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

            # Create google album now
            request_body = {
                'album': {
                    'title': local_album_name
                }
            }
            album_create_response = service.albums().create(body=request_body).execute()
            google_album_id = album_create_response.get('id')

            logging.info(f"Album Created: {album_create_response}")

            # Make album sharable
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
            logging.info(f"Album Shared: {album_share_response}")

            # Now get the album from Google to see if it has been created as shareable
            # We will now add it to our local cache and save the cache
            album_get_response = service.albums().get(albumId=google_album_id).execute()
            if album_create_response is not None:
                GoogleLibrary.cache_album(
                    album_get_response,
                    google_album_ids,
                    google_album_titles,shared=True)
                self.modified = True


    # -------------------------------------------------
    def upload(self, root):
        self.modified = False
        self.upload_recursive(root)
        if self.modified:
            GoogleLibrary.save_library()

    # -------------------------------------------------
    def get(self, title=None, id=None):
        """Return 'album' object given the 'title' or 'id'"""
        return None