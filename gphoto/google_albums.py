"""
Example of calling method for interactive shell

import gphoto
from gphoto.google_albums import GoogleAlbums
gphoto.init()
GoogleAlbums.download_albums()
"""

import os
from pathlib import Path
import json
import logging

import gphoto

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

class GoogleAlbums:

    _CACHE_FILE_NAME = "google_albums.json"
    _cache = None
    _cache_path = None

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogleAlbums._cache


    # -----------------------------------------------------
    # Cache media items to in-memory buffer from google api
    # -----------------------------------------------------
    @staticmethod
    def cache_albums():
        """
        Caches both albums and shared albums from google photos
        """
        service = GoogleService.service()
        if not service:
            logging.error("cache_albums: GoogleService.service() is not initialized")
            return
        
        pageSize=50

        # Get unshared albums
        response = service.albums().list(
            pageSize=pageSize
        ).execute()

        GoogleAlbums._cache = response.get('albums')
        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of albums
        while nextPageToken:
            response = service.albums().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            GoogleAlbums._cache.extend(response.get('albums'))
            nextPageToken = response.get('nextPageToken')

        # Get SHARED albums
        response = service.sharedAlbums().list(
            pageSize=pageSize
        ).execute()

        GoogleAlbums._cache.extend(response.get('sharedAlbums'))
        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of albums
        while nextPageToken:
            response = service.sharedAlbums().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            GoogleAlbums._cache.extend(response.get('sharedAlbums'))
            nextPageToken = response.get('nextPageToken')

        return True

    # --------------------------------------
    # Get path to local cache file
    # --------------------------------------
    @staticmethod
    def get_cache_filepath():

        if not GoogleAlbums._cache_path:
            cache_dir = gphoto.cache_dir()
            GoogleAlbums._cache_path = os.path.join(cache_dir, GoogleAlbums._CACHE_FILE_NAME)
        
        return GoogleAlbums._cache_path

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_albums():

        cache_filepath = GoogleAlbums.get_cache_filepath()

        try:
            cache_file = open(cache_filepath, "w")
            json.dump(GoogleAlbums._cache, cache_file, indent=2)
            cache_file.close()
            logging.info(f"GoogleAlbums:save_albums: Successfully saved albums to cache '{cache_filepath}'")
            return True
        except Exception as e:
            logging.critical(f"GoogleAlbums:save_albums: unable to save albums cache locally")
            raise

    # --------------------------------------
    # Load library cache from local file
    # --------------------------------------
    @staticmethod
    def load_albums():
        """
        Loads in-memory cache from local cache file
            Return: cache object
        You can also get the cache object later
        by calling cache() defined in this file
        """

        # We will reload the cache from local file
        GoogleAlbums._cache = None

        cache_filepath = GoogleAlbums.get_cache_filepath()
        if not os.path.exists(cache_filepath):
            logging.warning(f"GoogleAlbums:load_albums: No album cache file available.  Ignored")
            return

        try:
            cache_file = open(cache_filepath)
        except Exception as e:
            logging.critical(f"GoogleAlbums:load_albums: Unable top open albums cache file")
            raise

        try:
            GoogleAlbums._cache = json.load(cache_file)
            logging.info(f"GoogleAlbums:load_albums: Successfully loaded albums from cache '{cache_filepath}'")
        except Exception as e:
            GoogleAlbums._cache = None
            logging.error(f"GoogleAlbums:load_albums: Error occurred while loading mediaItem cache")
            raise

        return GoogleAlbums._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_albums():
        GoogleAlbums.cache_albums()
        GoogleAlbums.save_albums()