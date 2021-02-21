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

from gphoto.cache_util import CacheUtil
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

        def handle_media_item(mediaItem):
            mediaItemID = mediaItem['id']

            google_image_idx = None
            if mediaItemID not in google_image_ids:
                google_image_idx = GoogleImages.add_mediaItem(mediaItem)
                google_image_ids[mediaItemID] = google_image_idx
                mediaItem['mine'] = False
            else:
                google_image_idx = google_image_ids[mediaItemID]

            album_image_list.append(google_image_idx)

            # add album as image's parent
            google_image = google_images[google_image_idx]
            if 'parent' not in google_image:
                parent_album_ids = {google_album_idx: None}
                google_image['parent'] = parent_album_ids
            else:
                parent_album_ids = google_image['parent']
                parent_album_ids += {google_album_idx: None}

        GoogleAlbumImages._cache = {}

        service = GoogleService.service()
        if not service:
            logging.error("cache_album_images: GoogleService.service() is not initialized")
            return

        # Hold local vars for google images/albums cache
        google_image_cache = GoogleImages.cache()
        google_image_ids = google_image_cache['ids']
        google_images = google_image_cache['list']
        google_album_cache = GoogleAlbums.cache()
        google_album_list = google_album_cache['list']

        # API initializations
        # Loop through each Google Album already cached
        # ---------------------------------------------
        for google_album_idx, google_album in enumerate(google_album_list):
            google_album_id = google_album['id']
            google_album_title = "NONE"
            if 'title' in google_album:
                google_album_title = google_album['title']

            logging.info(f"GAI: Processing album '{google_album_title}', '{google_album_id}'")

            request_body = {
                'albumId': google_album_id,
                'pageSize': 100
            }

            response = service.mediaItems().search(body=request_body).execute()
            mediaItems = response.get('mediaItems')
            nextPageToken = response.get('nextPageToken')

            # If there are no images in the album then move on to the next one
            if not mediaItems:
                continue

            album_image_list = []
            GoogleAlbumImages._cache[google_album_id] = album_image_list

            for mediaItem in mediaItems:
                handle_media_item(mediaItem)

            # Loop through rest of the pages of mediaItems
            while nextPageToken:
                request_body['pageToken'] = nextPageToken

                response = service.mediaItems().search(body=request_body).execute()
                mediaItems = response.get('mediaItems')
                nextPageToken = response.get('nextPageToken')

                if not mediaItems:
                    continue

                for mediaItem in mediaItems:
                    handle_media_item(mediaItem)

                nextPageToken = response.get('nextPageToken')
        
        return True

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_album_images():
        gphoto.save_to_file(GoogleAlbumImages._cache, GoogleAlbumImages._CACHE_FILE_NAME)

    # --------------------------------------
    # Load library cache from local file
    # --------------------------------------
    @staticmethod
    def load_album_images():
        GoogleAlbumImages._cache = CacheUtil.load_from_file(GoogleAlbumImages._CACHE_FILE_NAME)
        return GoogleAlbumImages._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_album_images():
        GoogleAlbumImages.cache_album_images()
        GoogleImages.save_images()
        GoogleAlbumImages.save_album_images()