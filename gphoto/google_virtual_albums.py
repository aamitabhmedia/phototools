"""
"""

import os
from pathlib import Path
import json
import logging

import gphoto
from gphoto.cache_util import CacheUtil

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages

#-------------------------------------------------
# class definition
#-------------------------------------------------
class GoogleVirtualAlbums:

    _CACHE_FILE_NAME = "google_virtual_albums.json"
    _cache = None

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogleVirtualAlbums._cache

    # ------------------------------------------------------
    # Cache album images to in-memory buffer from google api
    # ------------------------------------------------------
    @staticmethod
    def cache_virtual_albums():
        """
        The virtual albums can only be built for the images that are taken by me.
        The criterion for images taken by me is that they follow image 
        """

    # --------------------------------------
    # Save media items to local file
    # --------------------------------------
    @staticmethod
    def save_virtual_albums():
        gphoto.save_to_file(GoogleVirtualAlbums._cache, GoogleVirtualAlbums._CACHE_FILE_NAME)

    # --------------------------------------
    # Load library cache from local file
    # --------------------------------------
    @staticmethod
    def load_virtual_albums():
        GoogleVirtualAlbums._cache = CacheUtil.load_from_file(GoogleVirtualAlbums._CACHE_FILE_NAME)
        return GoogleVirtualAlbums._cache

    # -------------------------------------------
    # cache from google api and save it locally
    # -------------------------------------------
    @staticmethod
    def download_virtual_albums():
        GoogleVirtualAlbums.cache_virtual_albums()
        GoogleVirtualAlbums.save_virtual_albums()
