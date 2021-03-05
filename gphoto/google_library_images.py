import os
from pathlib import Path
import json
import logging

import gphoto

from util.appdata import AppData
from util.log_mgr import LogMgr
from gphoto.cache_util import CacheUtil
from googleapi.google_service import GoogleService

from gphoto.goog_library import GoogLibrary, GoogleLibraryCache

class GoogleLibraryImages:

    @staticmethod
    def add_mediaItem(mediaItem, google_image_ids, google_image_filenames):
        mediaItemID = mediaItem['id']
        google_image_ids[mediaItemID] = mediaItem

        filename = mediaItem['filename']
        google_image_filenames[filename] = mediaItemID

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
            GoogleLibraryImages.add_mediaItem(mediaItem, google_image_ids, google_image_filenames)
        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of mediaItems
        while nextPageToken:
            response = service.mediaItems().list(
                pageSize=100,
                pageToken=nextPageToken
            ).execute()
            for mediaItem in mediaItems:
                GoogleLibraryImages.add_mediaItem(mediaItem, google_image_ids, google_image_filenames)
            nextPageToken = response.get('nextPageToken')
