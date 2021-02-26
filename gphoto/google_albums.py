"""
Example of calling method for interactive shell

import gphoto
from gphoto.google_albums import GoogleAlbums
gphoto.init()
GoogleAlbums.download_albums()

If the albums were saved in the previous session
then you can call load_albums() instead like this:

import gphoto
from gphoto.google_albums import GoogleAlbums
gphoto.init()
album_cache = GoogleAlbum.load_albums()
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

class GoogleAlbums:
    """
    Manages the cache that represent google photos Albums
    The cache is of the form:

    {
        'ids': {
            "album id": <album object>
            ...
        },
        'titles': {
            "album title": album id
                ...
        }
    }
    """

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
    def add_album(album, cache_ids, cache_titles, shared):

        album['shared'] = shared
        album_id = album['id']
        cache_ids[album_id] = album

        if 'title' in album:
            cache_titles[album['title']] = album_id


    # -----------------------------------------------------
    # Cache media items to in-memory buffer from google api
    # -----------------------------------------------------
    @staticmethod
    def cache_albums():
        """
        Caches both albums and shared albums from google photos
        """
        GoogleAlbums._cache = {
            'ids': {},
            'titles': {}
        }

        cache_ids = GoogleAlbums._cache['ids']
        cache_titles = GoogleAlbums._cache['titles']

        service = GoogleService.service()
        if not service:
            logging.error("GoogleAlbums.cache_albums: GoogleService.service() is not initialized")
            return
        
        pageSize=50

        # Get unshared albums
        response = service.albums().list(
            pageSize=pageSize,
            excludeNonAppCreatedData=False
        ).execute()

        response_albums = response.get('albums')
        for album in response_albums:
            GoogleAlbums.add_album(album, cache_ids, cache_titles, shared=False)

        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of albums
        while nextPageToken:
            response = service.albums().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            response_albums = response.get('albums')

            for album in response_albums:
                GoogleAlbums.add_album(album, cache_ids, cache_titles, shared=False)

            nextPageToken = response.get('nextPageToken')

        # Get SHARED albums
        response = service.sharedAlbums().list(
            pageSize=pageSize
        ).execute()
        response_albums = response.get('sharedAlbums')

        for album in response_albums:
            GoogleAlbums.add_album(album, cache_ids, cache_titles, shared=True)

        nextPageToken = response.get('nextPageToken')

        # Loop through rest of the pages of albums
        while nextPageToken:
            response = service.sharedAlbums().list(
                pageSize=pageSize,
                pageToken=nextPageToken
            ).execute()
            response_albums = response.get('sharedAlbums')

            for album in response_albums:
                GoogleAlbums.add_album(album, cache_ids, cache_titles, shared=True)

            nextPageToken = response.get('nextPageToken')

        logging.info(f"AlbumCache: Loaded albums: '{len(cache_ids)}', with title: '{len(cache_titles)}'")
        return True

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_albums():
        gphoto.save_to_file(GoogleAlbums._cache, GoogleAlbums._CACHE_FILE_NAME)

    # --------------------------------------
    # Load library cache from local file
    # --------------------------------------
    @staticmethod
    def load_albums():
        GoogleAlbums._cache = CacheUtil.load_from_file(GoogleAlbums._CACHE_FILE_NAME)
        return GoogleAlbums._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_albums():
        GoogleAlbums.cache_albums()
        GoogleAlbums.save_albums()