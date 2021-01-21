"""
Example of calling method for interactive shell

import gphoto
from gphoto.google_images import GoogleImages
gphoto.init()
GoogleImages.download_images()

If the images were saved in the previous session
then you can call load_images() instead like this:

import gphoto
from gphoto.google_images import GoogleImages
gphoto.init()
image_cache = GoogleImages.load_images()
"""

import os
from pathlib import Path
import json
import logging

import gphoto

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

class GoogleImages:
    """
    Manages the cache that represent google photos images
    The cache is of the form:

    {
        'list': [list of image objects, see google photos api],
        'iddict': {
            "image id": 37  # list[37] image object>
            ...
        },
        'namedict': {
            "image filename": 37 # list[37] image object
                ...
        }
    """

    _CACHE_FILE_NAME = "google_images.json"
    _cache = None
    _cache_path = None

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogleImages._cache

    # -----------------------------------------------------
    # Cache media items to in-memory buffer from google api
    # -----------------------------------------------------
    @staticmethod
    def cache_images():

        GoogleImages._cache = {
            'list': [],
            'iddict': {},
            'namedict': {}
        }

        cache_list = GoogleImages._cache['list']
        cache_iddict = GoogleImages._cache['iddict']
        cache_namedict = GoogleImages._cache['namedict']

        service = GoogleService.service()
        if not service:
            logging.error("GoogleImages.cache_images: GoogleService.service() is not initialized")
            return
        
        # Get the first page of mediaItems
        pageSize=100
        response = service.mediaItems().list(
            pageSize=pageSize
        ).execute()

        cache_list.extend(response.get('mediaItems'))
        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of mediaItems
        while nextPageToken:
            response = service.mediaItems().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            cache_list.extend(response.get('mediaItems'))
            nextPageToken = response.get('nextPageToken')

        # update dict cash now
        for idx, image in enumerate(cache_list):
            cache_iddict[image['id']] = idx
            if 'filename' in image:
                cache_namedict[image['filename']] = idx

        return True

    # --------------------------------------
    # Get path to local cache file
    # --------------------------------------
    @staticmethod
    def getif_cache_filepath():

        if not GoogleImages._cache_path:
            GoogleImages._cache_path = os.path.join(gphoto.cache_dir(), GoogleImages._CACHE_FILE_NAME)
        
        return GoogleImages._cache_path

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_images():

        cache_filepath = GoogleImages.getif_cache_filepath()

        try:
            cache_file = open(cache_filepath, "w")
            json.dump(GoogleImages._cache, cache_file, indent=2)
            cache_file.close()
            logging.info(f"GoogleImages.save_images: Successfully saved mediaItems to cache '{cache_filepath}'")
            return True
        except Exception as e:
            logging.critical(f"GoogleImages.save_images: unable to save mediaItems cache locally")
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

        cache_filepath = GoogleImages.getif_cache_filepath()
        if not os.path.exists(cache_filepath):
            logging.warning(f"GoogleImages.load_images: No mediaItem cache file available.  Ignored")
            return

        try:
            cache_file = open(cache_filepath)
        except Exception as e:
            logging.critical(f"GoogleImages.load_images: Unable top open mediaItems cache file")
            raise

        try:
            GoogleImages._cache = json.load(cache_file)
            logging.info(f"GoogleImages.load_images: Successfully loaded mediaItems from cache '{cache_filepath}'")
        except Exception as e:
            GoogleImages._cache = None
            logging.error(f"GoogleImages.load_images: Error occurred while loading mediaItem cache")
            raise

        return GoogleImages._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_images():
        GoogleImages.cache_images()
        GoogleImages.save_images()
