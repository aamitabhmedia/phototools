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

class GoogLibrary:

    _CACHE_FILE_NAME = "google_library.json"
    _cache = {
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
        google_image_ids = {}
        google_image_filenames = {}
        cache['image_ids'] = google_image_ids
        cache['image_filenames'] = google_image_filenames

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
        nextPageToken = response.get('nextPageToken')

        for mediaItem in mediaItems:
            GoogLibrary.cache_image(mediaItem, google_image_ids, google_image_filenames)

        # Loop through rest of the pages of mediaItems
        while nextPageToken:
            response = service.mediaItems().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            mediaItems = response.get('mediaItems')
            nextPageToken = response.get('nextPageToken')

            for mediaItem in mediaItems:
                GoogLibrary.cache_image(mediaItem, google_image_ids, google_image_filenames)

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
        cache = GoogLibrary.cache()
        google_album_ids = {}
        google_album_titles = {}
        cache['album_ids'] = google_album_ids
        cache['album_titles'] = google_album_titles

        service = GoogleService.service()
        if not service:
            logging.error("GoogLibrary.cache_albums: GoogleService.service() is not initialized")
            return
        
        # Get unshared albums, first page
        pageSize=50
        response = service.albums().list(
            pageSize=pageSize,
            excludeNonAppCreatedData=False
        ).execute()

        response_albums = response.get('albums')
        nextPageToken = response.get('nextPageToken')

        for album in response_albums:
            GoogLibrary.cache_album(album, google_album_ids, google_album_titles, shared=False)

        # Loop through rest of the pages of unshared albums
        while nextPageToken:
            response = service.albums().list(
                pageSize=pageSize,
                excludeNonAppCreatedData=False,
                pageToken=nextPageToken
            ).execute()
            response_albums = response.get('albums')
            nextPageToken = response.get('nextPageToken')

            for album in response_albums:
                GoogLibrary.cache_album(album, google_album_ids, google_album_titles, shared=False)


        # Get SHARED albums, first page
        response = service.sharedAlbums().list(
            pageSize=pageSize
        ).execute()
        response_albums = response.get('sharedAlbums')
        nextPageToken = response.get('nextPageToken')

        for album in response_albums:
            GoogLibrary.cache_album(album, google_album_ids, google_album_titles, shared=True)

        # Loop through rest of the pages of albums
        while nextPageToken:
            response = service.sharedAlbums().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            response_albums = response.get('sharedAlbums')
            nextPageToken = response.get('nextPageToken')

            for album in response_albums:
                GoogLibrary.cache_album(album, google_album_ids, google_album_titles, shared=True)

    # -----------------------------------------------------
    # Cache images only
    # -----------------------------------------------------
    @staticmethod
    def cache_album_images():

        cache = GoogLibrary.cache()
        pass



    # -----------------------------------------------------
    # Cache Google library by using API
    # -----------------------------------------------------
    @staticmethod
    def cache_library():
        GoogLibrary.cache_albums()
        GoogLibrary.cache_images()
        GoogLibrary.cache_album_images()

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
