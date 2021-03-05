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
    # Cach Google Photos use API
    # -----------------------------------------------------
    @staticmethod
    def cache_library():

        GoogLibrary._cache = GoogleLibraryCache()
        GoogleLibraryImages.cache_images()

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
