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
from gphoto.cache_util import CacheUtil
from googleapi.google_service import GoogleService

class GoogleImages:
    """
    Manages the cache that represent google photos images
    The cache is of the form:

    {
        'ids': {
            "image id": { image object }
            ...
        },
        'filenames': {
            "image filename": image id
                ...
        }
    """

    _CACHE_FILE_NAME = "google_images.json"
    _cache = None

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogleImages._cache

    # -----------------------------------------------------
    # Add new media item and return index into images list
    # -----------------------------------------------------
    @staticmethod
    def add_mediaItem(mediaItem):
        google_image_ids = GoogleImages.cache()['ids']
        google_image_filenames = GoogleImages.cache()['filenames']

        mediaItemID = mediaItem['id']
        google_image_ids[mediaItemID] = mediaItem
        google_image_filenames[mediaItem['filename']] = mediaItemID

    # -----------------------------------------------------
    # Cache media items to in-memory buffer from google api
    # -----------------------------------------------------
    @staticmethod
    def cache_images():

        GoogleImages._cache = {
            'ids': {},
            'filenames': {}
        }

        cache_ids = GoogleImages._cache['ids']
        cache_filenames = GoogleImages._cache['filenames']

        service = GoogleService.service()
        if not service:
            logging.error("GoogleImages.cache_images: GoogleService.service() is not initialized")
            return
        
        # Get the first page of mediaItems
        pageSize=100
        response = service.mediaItems().list(
            pageSize=pageSize
        ).execute()

        mediaItems = response.get('mediaItems')
        for mediaItem in mediaItems:
            GoogleImages.add_mediaItem(mediaItem)
        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of mediaItems
        while nextPageToken:
            response = service.mediaItems().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            for mediaItem in mediaItems:
                GoogleImages.add_mediaItem(mediaItem)
            nextPageToken = response.get('nextPageToken')

        return GoogleImages.cache()

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_images():
        gphoto.save_to_file(GoogleImages._cache, GoogleImages._CACHE_FILE_NAME)

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

        GoogleImages._cache = CacheUtil.load_from_file(GoogleImages._CACHE_FILE_NAME)
        return GoogleImages._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_images():
        GoogleImages.cache_images()
        GoogleImages.save_images()
