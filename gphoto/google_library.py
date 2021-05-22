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

class GoogleLibrary:

    _CACHE_FILE_NAME = "google_library.json"
    _cache = {
        'summary': {
            'album_count': None,
            'image_count': None
        },
        'album_ids': None,        
        'album_titles': None,
        'image_ids': None,
        'image_filenames': None,
        'album_images': None,
        'image_albums': None
    }

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogleLibrary._cache

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
        cache = GoogleLibrary.cache()
        google_image_ids = {}
        google_image_filenames = {}
        cache['image_ids'] = google_image_ids
        cache['image_filenames'] = google_image_filenames

        service = GoogleService.service()
        if not service:
            logging.error("GoogleLibrary.cache_images: GoogleService.service() is not initialized")
            return

        # Get the first page of mediaItems
        pageSize=100
        response = service.mediaItems().list(
            pageSize=pageSize
        ).execute()
        mediaItems = response.get('mediaItems')
        nextPageToken = response.get('nextPageToken')

        for mediaItem in mediaItems:
            GoogleLibrary.cache_image(mediaItem, google_image_ids, google_image_filenames)

        # Loop through rest of the pages of mediaItems
        while nextPageToken:
            response = service.mediaItems().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            mediaItems = response.get('mediaItems')
            nextPageToken = response.get('nextPageToken')

            if mediaItems is not None:
                for mediaItem in mediaItems:
                    GoogleLibrary.cache_image(mediaItem, google_image_ids, google_image_filenames)

        summary = cache.get('summary')
        summary['image_count'] = len(google_image_ids)

    # -----------------------------------------------------
    # Cache media items to in-memory buffer from google api
    # -----------------------------------------------------
    @staticmethod
    def cache_album(album, google_album_ids, google_album_titles, shared):

        album['shared'] = shared
        album_id = album['id']
        google_album_ids[album_id] = album

        if 'title' in album:
            google_album_titles[album['title']] = album_id

    # -----------------------------------------------------
    # cache albums
    # -----------------------------------------------------
    @staticmethod
    def cache_albums():

        # Initialize album fields of the cache
        cache = GoogleLibrary.cache()
        google_album_ids = {}
        google_album_titles = {}
        cache['album_ids'] = google_album_ids
        cache['album_titles'] = google_album_titles

        service = GoogleService.service()
        if not service:
            logging.error("GoogleLibrary.cache_albums: GoogleService.service() is not initialized")
            return
        
        # Get unshared albums, first page
        pageSize=50
        response = service.albums().list(
            pageSize=pageSize,
            excludeNonAppCreatedData=False
        ).execute()

        response_albums = response.get('albums')
        nextPageToken = response.get('nextPageToken')

        if response_albums:
            for album in response_albums:
                GoogleLibrary.cache_album(album, google_album_ids, google_album_titles, shared=False)

        # Loop through rest of the pages of unshared albums
        while nextPageToken:
            response = service.albums().list(
                pageSize=pageSize,
                excludeNonAppCreatedData=False,
                pageToken=nextPageToken
            ).execute()
            response_albums = response.get('albums')
            nextPageToken = response.get('nextPageToken')

            if response_albums:
                for album in response_albums:
                    GoogleLibrary.cache_album(album, google_album_ids, google_album_titles, shared=False)


        # Get SHARED albums, first page
        response = service.sharedAlbums().list(
            pageSize=pageSize
        ).execute()
        response_albums = response.get('sharedAlbums')
        nextPageToken = response.get('nextPageToken')

        for album in response_albums:
            GoogleLibrary.cache_album(album, google_album_ids, google_album_titles, shared=True)

        # Loop through rest of the pages of albums
        while nextPageToken:
            response = service.sharedAlbums().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            response_albums = response.get('sharedAlbums')
            nextPageToken = response.get('nextPageToken')

            for album in response_albums:
                GoogleLibrary.cache_album(album, google_album_ids, google_album_titles, shared=True)

        summary = cache.get('summary')
        summary['album_count'] = len(google_album_ids)

    # -----------------------------------------------------
    # Handle each media item
    # -----------------------------------------------------
    @staticmethod
    def cache_album_image_reln(mediaItem, album,
            google_album_ids, google_album_titles,
            google_image_ids, google_image_filenames,
            album_images_cache, image_albums_cache):

        mediaItemID = mediaItem['id']

        # if mediaItem not in images then add it
        google_image = google_image_ids.get(mediaItemID)
        if google_image is None:
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

    # -----------------------------------------------------
    # Cache album images relationship
    # -----------------------------------------------------
    @staticmethod
    def cache_album_images():

        cache = GoogleLibrary.cache()

        # Service initialization
        service = GoogleService.service()
        if not service:
            logging.error("cache_album_images: GoogleService.service() is not initialized")
            return

        # Hold local vars for google images/albums cache
        google_image_ids = cache['image_ids']
        google_image_filenames = cache['image_filenames']

        google_album_ids = cache['album_ids']
        google_album_titles = cache['album_titles']

        # Initialize album_image and image_album caches
        album_images_cache = {}
        image_albums_cache = {}
        cache['album_images'] = album_images_cache
        cache['image_albums'] = image_albums_cache

        # Loop through each Google Album already cached
        # ---------------------------------------------
        for google_album_id, google_album in google_album_ids.items():
            google_album_title = google_album.get('title')

            # logging.info(f"GAI: Processing album '{google_album_title}', '{google_album_id}'")

            # get first set of images for this album
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

            for mediaItem in mediaItems:
                GoogleLibrary.cache_album_image_reln(mediaItem, google_album,
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
                    GoogleLibrary.cache_album_image_reln(mediaItem, google_album,
                        google_album_ids, google_album_titles,
                        google_image_ids, google_image_filenames,
                        album_images_cache, image_albums_cache)

    # -----------------------------------------------------
    # Cache Google library by using API
    # -----------------------------------------------------
    @staticmethod
    def cache_library():
        GoogleLibrary.cache_albums()
        GoogleLibrary.cache_images()
        GoogleLibrary.cache_album_images()

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_library():
        gphoto.save_to_file(GoogleLibrary._cache,GoogleLibrary._CACHE_FILE_NAME)

    # --------------------------------------
    # Load library cache from local file
    # --------------------------------------
    @staticmethod
    def load_library():
        if GoogleLibrary._cache.get('album_ids') is None or GoogleLibrary._cache.get('image_ids') is None:
            GoogleLibrary._cache = CacheUtil.load_from_file(GoogleLibrary._CACHE_FILE_NAME)
        return GoogleLibrary._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_library():
        GoogleLibrary.cache_library()
        GoogleLibrary.save_library()
