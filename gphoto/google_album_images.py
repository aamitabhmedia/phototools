"""
Example of calling method for interactive shell:
(Requires album and images are loaded in the cache)

import gphoto
from gphoto.google_album_images import GoogleAlbumImages
from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages
gphoto.init()
albums_cache = GoogleAlbums.load_albums()
images_cache = GoogleImages.load_images()
album_images_cache = GoogleAlbumImages.download_album_images()

If the albums/images were saved in the previous session
then you can call load_album_images() instead like this:

import gphoto
from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages
from gphoto.google_album_images import GoogleAlbumImages
gphoto.init()
albums_cache = GoogleAlbums.load_albums()
images_cache = GoogleImages.load_images()
album_images_cache = GoogleAlbumImages.load_album_images()

The cache has this structure:

{
    "album id": [list of indices into images cache],
        ...
}
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

        # Hold local vars for google images/albums cache
        google_image_cache = GoogleImages.cache()
        google_image_ids = google_image_cache['ids']
        google_album_cache = GoogleAlbums.cache()
        google_album_list = google_album_cache['list']

        # API initializations
        request_body = {
            'albumId': None,
            'pageSize': 100
        }

        # Loop through each Google Album already cached
        # ---------------------------------------------
        for google_album in google_album_list:
            google_album_id = google_album['id']
            google_album_title = "NONE"
            if 'title' in google_album:
                google_album_title = google_album['title']

            logging.info(f"GoogleAlbumImages.cache_album_images: Processing album '{google_album_title}', '{google_album_id}'")

            image_list = []
            GoogleAlbumImages._cache[google_album_id] = image_list

            request_body['albumId'] = google_album_id
            response = service.mediaItems().search(body=request_body).execute()
            mediaItems = response.get('mediaItems')
            nextPageToken = response.get('nextPageToken')

            for mediaItem in mediaItems:
                mediaItemID = mediaItem['id']
                google_image_idx = google_image_ids[mediaItemID]
                image_list.append(google_image_idx)

            # Loop through rest of the pages of mediaItems
            while nextPageToken:
                request_body['pageToken'] = nextPageToken

                response = service.mediaItems().search(body=request_body).execute()
                mediaItems = response.get('mediaItems')
                nextPageToken = response.get('nextPageToken')

                for mediaItem in mediaItems:
                    mediaItemID = mediaItem['id']
                    google_image_idx = google_image_ids[mediaItemID]
                    image_list.append(google_image_idx)

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