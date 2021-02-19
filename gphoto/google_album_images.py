"""
Example of calling method for interactive shell:
(Requires album and images are loaded in the cache)

import gphoto
from gphoto.google_album_images import GoogleAlbumImages
from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages
gphoto.init()
GoogleAlbums.download_albums()
GoogleImages.download_album_images()
GoogleAlbumImages.download_album_images()

If the albums/images were saved in the previous session
then you can call load_album_images() instead like this:

import gphoto
from gphoto.google_images import GoogleImages
gphoto.init()
GoogleAlbumImages.load_albums()
GoogleAlbumImages.load_images()
album_images_cache = GoogleAlbumImages.load_album_images()
"""

import os
from pathlib import Path
import json
import logging

import gphoto
from gphoto import google_albums

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages

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


    # ------------------------------------------------------
    # Cache album images to in-memory buffer from google api
    # ------------------------------------------------------
    @staticmethod
    def cache_album_images():

        GoogleAlbumImages._cache = {}

        service = GoogleService.service()
        if not service:
            logging.error("cache_album_images: GoogleService.service() is not initialized")
            return

        # Loop through each Google Album already cached
        # ---------------------------------------------
        google_album_cache = GoogleAlbums.cache()
        google_album_list = google_album_cache['list']
        for google_album in google_album_list:

        # Get the first page of mediaItems
        pageSize=100
        response = service.mediaItems().list(
            pageSize=pageSize
        ).execute()

        GoogleAlbumImages._cache = response.get('mediaItems')
        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of mediaItems
        while nextPageToken:
            response = service.mediaItems().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            GoogleAlbumImages._cache.extend(response.get('mediaItems'))
            nextPageToken = response.get('nextPageToken')
        
        return True

    # --------------------------------------
    # Get path to local cache file
    # --------------------------------------
    @staticmethod
    def getif_cache_filepath():

        if not GoogleAlbumImages._cache_path:
            cache_dir = gphoto.cache_dir()
            GoogleAlbumImages._cache_path = os.path.join(cache_dir, GoogleAlbumImages._CACHE_FILE_NAME)
        
        return GoogleAlbumImages._cache_path

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_album_images():

        cache_filepath = GoogleAlbumImages.getif_cache_filepath()

        try:
            cache_file = open(cache_filepath, "w")
            json.dump(GoogleAlbumImages._cache, cache_file, indent=2)
            cache_file.close()
            logging.info(f"media_mgr:save_album_images_to_local_cache: Successfully saved mediaItems to cache '{cache_filepath}'")
            return True
        except Exception as e:
            logging.critical(f"media_mgr:save_album_images_to_local_cache: unable to save mediaItems cache locally")
            raise

    # --------------------------------------
    # Load library cache from local file
    # --------------------------------------
    @staticmethod
    def load_album_images():
        """
        Loads in-memory cache from local cache file
            Return: cache object
        You can also get the cache object later
        by calling cache() defined in this file
        """

        # We will reload the cache from local file
        GoogleAlbumImages._cache = None

        cache_filepath = GoogleAlbumImages.getif_cache_filepath()
        if not os.path.exists(cache_filepath):
            logging.warning(f"load_images: No mediaItem cache file available.  Ignored")
            return

        try:
            cache_file = open(cache_filepath)
        except Exception as e:
            logging.critical(f"load_images: Unable top open mediaItems cache file")
            raise

        try:
            GoogleAlbumImages._cache = json.load(cache_file)
            logging.info(f"load_images: Successfully loaded mediaItems from cache '{cache_filepath}'")
        except Exception as e:
            GoogleAlbumImages._cache = None
            logging.error(f"load_images: Error occurred while loading mediaItem cache")
            raise

        return GoogleAlbumImages._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_album_images():
        GoogleAlbumImages.cache_album_images()
        GoogleAlbumImages.save_album_images()