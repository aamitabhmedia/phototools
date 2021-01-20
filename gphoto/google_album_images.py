import os
from pathlib import Path
import json
import logging

import gphoto

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

class GoogleAlbumImages:

    _CACHE_FILE_NAME = "google_album_images.json"
    _cache = None
    _cache_path = None

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogleAlbumImages._cache


    # -----------------------------------------------------
    # Cache media items to in-memory buffer from google api
    # -----------------------------------------------------
    @staticmethod
    def cache_album_images():
        service = GoogleService.service()
        if not service:
            logging.error("cache_album_images: GoogleService.service() is not initialized")
            return
        
        # Get the first page of mediaItems
        pageSize=100
        response = service.mediaItems().list(
            pageSize=pageSize
        ).execute()

        GoogleImages._cache = response.get('mediaItems')
        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of mediaItems
        while nextPageToken:
            response = service.mediaItems().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            GoogleImages._cache.extend(response.get('mediaItems'))
            nextPageToken = response.get('nextPageToken')
        
        return True

    # --------------------------------------
    # Get path to local cache file
    # --------------------------------------
    @staticmethod
    def get_cache_filepath():

        cache_dir = os.path.join(Path.home(), AppData.APPDATA_NAME, "cache")
        p = Path(cache_dir)
        if (not p.exists()):
            try:
                p.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logging.critical(f"media_mgr:cache_filepath: Unable to create cache dir '{cache_dir}'.  Aborting")
                exit

        GoogleImages._cache_path = os.path.join(cache_dir, "mediaItem_cache.json")
        return GoogleImages._cache_path

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_images():

        cache_filepath = GoogleImages.get_cache_filepath()

        try:
            cache_file = open(cache_filepath, "w")
            json.dump(GoogleImages._cache, cache_file, indent=2)
            cache_file.close()
            logging.info(f"media_mgr:save_images_to_local_cache: Successfully saved mediaItems to cache '{cache_filepath}'")
            return True
        except Exception as e:
            logging.critical(f"media_mgr:save_images_to_local_cache: unable to save mediaItems cache locally")
            raise

    # --------------------------------------
    # Load library cache from local file
    # --------------------------------------
    @staticmethod
    def load_images():
        """
        Loads in-memory cache from local cache file
            Return: cache object
        You can also get the cache object later
        by calling cache() defined in this file
        """

        # We will reload the cache from local file
        GoogleImages._cache = None

        cache_filepath = GoogleImages.get_cache_filepath()
        if not os.path.exists(cache_filepath):
            logging.warning(f"load_images: No mediaItem cache file available.  Ignored")
            return

        try:
            cache_file = open(cache_filepath)
        except Exception as e:
            logging.critical(f"load_images: Unable top open mediaItems cache file")
            raise

        try:
            GoogleImages._cache = json.load(cache_file)
            logging.info(f"load_images: Successfully loaded mediaItems from cache '{cache_filepath}'")
        except Exception as e:
            GoogleImages._cache = None
            logging.error(f"load_images: Error occurred while loading mediaItem cache")
            raise

        return GoogleImages._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_images():
        GoogleImages.cache_album_images()
        GoogleImages.save_images()