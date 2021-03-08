"""
Manages cache of local raw and jpg cache
"""
from gphoto.imageutils import ImageUtils
import os
import pathlib
import logging
import json
from typing import List
import gphoto
from gphoto import core
import exiftool

_METADATA_TAGS = [
    "-DateTimeOriginal",
    "-CreateDate",
    "-Description",
    "-FileTypeExtension"
    "-MimeType",
    "-Model"
]

class LocalLibraryMetadata(object):

    _CACHE_RAW_FILE_NAME = 'local_library_metadata_raw.json'
    _CACHE_JPG_FILE_NAME = 'local_library_metadata_jpg.json'

    _cache_raw = None
    _cache_jpg = None

    @staticmethod
    def cache_raw():
        return LocalLibraryMetadata._cache_raw

    @staticmethod
    def cache_jpg():
        return LocalLibraryMetadata._cache_jpg

    @staticmethod
    def getif_cache_filepath(library_type):
        """
        Library type can be one of 'raw' or 'jpg'
        """
        if library_type == 'raw':
            return os.path.join(gphoto.cache_dir(), LocalLibraryMetadata._CACHE_RAW_FILE_NAME)
        else:
            return os.path.join(gphoto.cache_dir(), LocalLibraryMetadata._CACHE_JPG_FILE_NAME)

    @staticmethod
    def cache_any_metadata(root_folder, library_type, cache):
        pass

    @staticmethod
    def cache_library_metadata(root_folder, library_type):
        if library_type == 'raw':
            LocalLibraryMetadata.cache_any_metadata(root_folder, library_type, LocalLibraryMetadata._cache_raw)
        elif library_type == 'jpg':
            LocalLibraryMetadata.cache_any_metadata(root_folder, library_type, LocalLibraryMetadata._cache_jpg)

    @staticmethod
    def save_library_metadata(library_type=None):
        if library_type == None or library_type == "raw":
            cache_filepath = LocalLibraryMetadata.getif_cache_filepath('raw')
            LocalLibraryMetadata.save_any_cache(cache_filepath, LocalLibraryMetadata._cache_raw)
        if library_type == None or library_type == "jpg":
            cache_filepath = LocalLibraryMetadata.getif_cache_filepath('jpg')
            LocalLibraryMetadata.save_any_cache(cache_filepath, LocalLibraryMetadata._cache_jpg)