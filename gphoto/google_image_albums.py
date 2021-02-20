import os
from pathlib import Path
import json
import logging

import gphoto
from gphoto import google_albums
from gphoto import google_images

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages

class GoogleImageAlbums:

    _CACHE_FILE_NAME = "google_image_albums.json"
    _cache = None
    _cache_path = None

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogleImageAlbums._cache


    # ------------------------------------------------------
    # Cache album images to in-memory buffer from google api
    # ------------------------------------------------------
    @staticmethod
    def cache_album_images():

        GoogleImageAlbums._cache = {}

        service = GoogleService.service()
        if not service:
            logging.error("cache_album_images: GoogleService.service() is not initialized")
            return

        # Hold local vars for google images/albums cache
        google_image_cache = GoogleImages.cache()
        google_image_ids = google_image_cache['ids']
        google_album_cache = GoogleAlbums.cache()
        google_album_list = google_album_cache['list']
