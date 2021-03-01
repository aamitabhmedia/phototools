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

The cache has 2 structure:
    below is dictionary of albums and their list of images

    "album_images": {
        "album id": [list of indices into images cache],
            ...
    }

    below is dictionary of images and it parent album dictionary
    "image_albums": {
        "image_id": [list of indices of albums]
    }
"""

from gphoto.cache_util import CacheUtil
import os
from pathlib import Path
import json
import logging

import gphoto

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages

class GoogleAlbumImages:

    _CACHE_FILE_NAME = "google_album_images.json"
    _cache = None

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogleAlbumImages._cache


    # -----------------------------------------------------
    # Handle each media item
    # -----------------------------------------------------
    @staticmethod
    def add_media_item(mediaItem, album,
            google_album_ids, google_album_titles,
            google_image_ids, google_image_filenames,
            album_images_cache, image_albums_cache):

        mediaItemID = mediaItem['id']

        # if mediaItem not in images then add it
        google_image = None
        if mediaItemID not in google_image_ids:
            mediaItem['mine'] = False
            google_image_ids[mediaItemID] = mediaItem
            google_image_filenames[mediaItem['filename']] = mediaItemID
            google_image = mediaItem
        else:
            google_image = google_image_ids[mediaItemID]

        # Add image to album images
        album_id = album['id']
        if album_id not in album_images_cache:
            album_images = {
                mediaItemID: None
            }
            album_images_cache[album_id] = album_images
        else:
            album_images = album_images_cache[album_id]
            album_images[mediaItemID] = None

        # If album to image albums
        if mediaItemID not in image_albums_cache:
            image_albums = {
                album_id: None
            }
            image_albums_cache[mediaItemID] = image_albums
        else:
            image_albums = image_albums_cache[mediaItemID]
            image_albums[album_id] = None

    # ------------------------------------------------------
    # Cache album images to in-memory buffer from google api
    # ------------------------------------------------------
    @staticmethod
    def cache_album_images():

        # Service initialization
        service = GoogleService.service()
        if not service:
            logging.error("cache_album_images: GoogleService.service() is not initialized")
            return

        # Hold local vars for google images/albums cache
        google_image_cache = GoogleImages.cache()
        google_image_ids = google_image_cache['ids']
        google_image_filenames = google_image_cache['filenames']

        google_album_cache = GoogleAlbums.cache()
        google_album_ids = google_album_cache['ids']
        google_album_titles = google_album_cache['titles']

        # Initialize album_image and image_album caches
        album_images_cache = {}
        image_albums_cache = {}
        GoogleAlbumImages._cache = {
            "album_images": album_images_cache,
            "image_albums": image_albums_cache
        }

        # Loop through each Google Album already cached
        # ---------------------------------------------
        for google_album_id, google_album in google_album_ids.items():
            google_album_title = "NONE"
            if 'title' in google_album:
                google_album_title = google_album['title']

            logging.info(f"GAI: Processing album '{google_album_title}', '{google_album_id}'")

            request_body = {
                'albumId': google_album_id,
                'pageSize': 100
            }

            # get first set of images for this album
            response = service.mediaItems().search(body=request_body).execute()
            mediaItems = response.get('mediaItems')
            nextPageToken = response.get('nextPageToken')

            # If there are no images in the album then move on to the next one
            if not mediaItems:
                continue

            for mediaItem in mediaItems:
                GoogleAlbumImages.add_media_item(mediaItem, google_album,
                    google_album_ids, google_album_titles,
                    google_image_ids, google_image_filenames,
                    album_images_cache, image_albums_cache)

            # Loop through rest of the pages of mediaItems
            # ------------------------------------------------
            while nextPageToken:
                request_body['pageToken'] = nextPageToken

                response = service.mediaItems().search(body=request_body).execute()
                mediaItems = response.get('mediaItems')
                nextPageToken = response.get('nextPageToken')

                for mediaItem in mediaItems:
                    GoogleAlbumImages.add_media_item(mediaItem, google_album,
                        google_album_ids, google_album_titles,
                        google_image_ids, google_image_filenames,
                        album_images_cache, image_albums_cache)

                nextPageToken = response.get('nextPageToken')
        
        return GoogleAlbumImages.cache()

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
        GoogleAlbumImages.save_album_images()
        GoogleImages.save_images()
