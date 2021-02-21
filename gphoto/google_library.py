import os
from pathlib import Path
import logging

import gphoto

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

from gphoto.google_images import GoogleImages
from gphoto.google_albums import GoogleAlbums
from gphoto.google_album_images import GoogleAlbumImages

class GoogleLibrary:
    """
    The class enables loading albums, their images
    and all images from Google Photos. It coordinates
    between GoogleAlbum and GoogleImages classes to make
    sure that they are cached, saved, and loaded in syc.

    The class needs to ensure that the operations on 
    Google images is done before Google albums
    """

    @staticmethod
    def cache_library():
        """
        Cache all images, albums, and album to image relations
        """
        GoogleImages.cache_images()
        GoogleAlbums.cache_albums()
        GoogleAlbumImages.cache_album_images()

    @staticmethod
    def save_library():
        """
        Save all images, albums to local cache file
        """
        GoogleImages.save_images()
        GoogleAlbums.save_albums()
        GoogleAlbumImages.save_album_images()

    @staticmethod
    def download_library():
        """
        Download all images, albums in-memory cache, and save to local cache file
        """
        GoogleLibrary.cache_library()
        GoogleLibrary.save_library()

    @staticmethod
    def load_library():
        """
        load all images, albums from local cache file
        """
        GoogleImages.load_images()
        GoogleAlbums.load_albums()
        GoogleAlbumImages.load_album_images()

