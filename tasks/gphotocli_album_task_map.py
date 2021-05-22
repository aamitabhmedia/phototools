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
    def map_album(self, local_album, google_album, test):

        logging.error(f"Mapping album: '{google_album.get('title')}'")

        # Initialize Google API and load cache.
        google_cache = GoogleLibrary.cache()
        google_album_ids = google_cache.get('album_ids')
        google_album_titles = google_cache.get('album_titles')
        google_image_ids = google_cache.get('image_ids')
        google_album_to_images = google_cache.ge_ids('album_images')

        # Load local library cache
        local_cache = LocalLibrary.cache('jpg')
        local_albums = local_cache.get('albums')
        local_images = local_cache.get('images')
        # local_image_ids = local_cache.get('image_ids')

        # Collect local images belonging to local album
        local_album_image_idxs = local_album.get('images')
        if local_album_image_idxs is None or len(local_album_image_idxs) <= 0:
            logging.info(f"No images found in album '{local_album.get('name')}'")
            return

        # from local album images indices, build local album image list
        local_album_images = {}
        for idx in local_album_image_idxs:
            local_image = local_images[idx]
            local_image_name = local_image.get('name')
            local_album_images[local_image_name] = local_image

        # From google album get images already in it
        google_album_id = google_album.get('id')
        google_album_to_image_ids = google_album_to_images.get(id)
        google_album_images = {}
        for google_image_id in google_album_to_image_ids:
            google_album_image = google_image_ids.get(google_image_id)
            google_album_images[google_image_id] = google_album_image

        # Compare the the two sets
        # Any image not in local album, not in Google album, add it to google album


        # Compare the 2 images sets
        # Any image in Google album not in Local album, remove it from Google album
        # TODO:

    # -------------------------------------------------
    def map_recursive(self, root, test):
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

            # If album not in Google Cache, ignore and then error out
            google_album_id = google_album_titles.get(local_album_name)
            google_album = google_album_ids[google_album_id] if google_album_id is not None else None

            if google_album is None:
                logging.error(f"Ignoring album not in Google Cache: '{google_album.get('title')}'")
                continue

            # Do mapping for each Local/Google album
            self.map_album(local_album, google_album, test)


    # -------------------------------------------------
    def map(self, root, test=False):
        self.modified = False

        try:
            self.map_recursive(root, test)

        finally:
            if self.modified:
                GoogleLibrary.save_library()
