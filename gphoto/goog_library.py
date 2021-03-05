"""
The library contains images, albums, and mapping of album to images
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

from gphoto.google_library_images import GoogleLibraryImages

class GoogleLibraryCache(object):
    albums = None
    album_ids = None
    album_titles = None
    images = None
    image_ids = None
    image_filenames = None

class GoogLibrary:

    _CACHE_FILE_NAME = "google_library.json"
    _cache = None

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogLibrary._cache

    # -----------------------------------------------------
    # Cache an image
    # -----------------------------------------------------
    @staticmethod
    def cache_image(mediaItem, google_image_ids, google_image_filenames):
        mediaItemID = mediaItem['id']
        google_image_ids[mediaItemID] = mediaItem

        filename = mediaItem['filename']
        google_image_filenames[filename] = mediaItemID

    # -----------------------------------------------------
    # cache images
    # -----------------------------------------------------
    @staticmethod
    def cache_images():

        # Initialize images fields of the cache
        cache = GoogLibrary.cache()
        google_images = []
        google_image_ids = {}
        google_image_filenames = {}
        cache.images = google_images
        cache.image_ids = google_image_ids
        cache.image_filenames= google_image_filenames

        service = GoogleService.service()
        if not service:
            logging.error("GoogleImages.cache_images: GoogleService.service() is not initialized")
            return

        # Get the first page of mediaItems
        pageSize=25
        response = service.mediaItems().list(
            pageSize=25
        ).execute()

        mediaItems = response.get('mediaItems')
        for mediaItem in mediaItems:
            GoogleLibraryImages.cache_image(mediaItem, google_image_ids, google_image_filenames)
        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of mediaItems
        while nextPageToken:
            response = service.mediaItems().list(
                pageSize=100,
                pageToken=nextPageToken
            ).execute()
            for mediaItem in mediaItems:
                GoogleLibraryImages.cache_image(mediaItem, google_image_ids, google_image_filenames)
            nextPageToken = response.get('nextPageToken')

    # -----------------------------------------------------
    # Cach Google Photos use API
    # -----------------------------------------------------
    @staticmethod
    def cache_library():

        GoogLibrary._cache = GoogleLibraryCache()
        GoogLibrary.cache_images()

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_library():
        gphoto.save_to_file(GoogLibrary._cache,GoogLibrary._CACHE_FILE_NAME)

    # --------------------------------------
    # Load library cache from local file
    # --------------------------------------
    @staticmethod
    def load_library():
        GoogLibrary._cache = CacheUtil.load_from_file(GoogLibrary._CACHE_FILE_NAME)
        return GoogLibrary._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_library():
        GoogLibrary.cache_library()
        GoogLibrary.save_library()
