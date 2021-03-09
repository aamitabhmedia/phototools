"""
Manages cache of local raw and jpg cache
"""
from gphoto.imageutils import ImageUtils
import os
import pathlib
import logging
import json
import subprocess
import tempfile
import subprocess
import csv

import gphoto
from gphoto import core

_METADATA_TAGS = [
    '-DateTimeOriginal',
    '-CreateDate',
    '-Description',
    '-Title',
    '-FileTypeExtension',
    '-MimeType',
    '-Model'
]

_JSON_RAW_FILEPATH = os.path.join(tempfile.gettempdir(), 'image_library_metadata_raw.json')
_JSON_JPG_FILEPATH = os.path.join(tempfile.gettempdir(), 'image_library_metadata_jpg.json')

class LocalLibraryMetadata(object):

    _CACHE_RAW_FILE_NAME = 'local_library_metadata_raw.json'
    _CACHE_JPG_FILE_NAME = 'local_library_metadata_jpg.json'

    _cache_raw = None
    _cache_jpg = None

    # -------------------------------------------------
    # -------------------------------------------------
    @staticmethod
    def cache(library_type):
        return LocalLibraryMetadata._cache_raw if library_type == 'raw' else LocalLibraryMetadata._cache_jpg

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
    def cache_any_library_metadata(root_folder, library_type):

        # Build the exiftool batch json command
        cmd = ['exiftool', '-q', '-json', '-r']
        for tag in _METADATA_TAGS:
            cmd.append(tag)
        for ext in core.MEDIA_EXTENSIONS:
            cmd.append('-ext')
            cmd.append(ext[1:])
        cmd.append(root_folder)

        filepath = _JSON_RAW_FILEPATH if library_type == 'raw' else _JSON_JPG_FILEPATH

        logging.info(f"cmd: {cmd}")
        logging.info(f"csv: {filepath}")

        # Execute the command and redirect to a json file
        with open(filepath, "w") as writer:
            subprocess.run(cmd, stdout=writer)

        cache = {}

        # Load the json file into a cache format
        with open(filepath) as reader:
            json_data = json.load(reader)
            for image in json_data:
                image_path = image.get('SourceFile')
                cache[image_path] = image

        return cache

    @staticmethod
    def cache_library_metadata(root_folder, library_type):
        if library_type == 'raw':
            LocalLibraryMetadata._cache_raw = LocalLibraryMetadata.cache_any_library_metadata(root_folder, library_type)
        elif library_type == 'jpg':
            LocalLibraryMetadata._cache_jpg = LocalLibraryMetadata.cache_any_library_metadata(root_folder, library_type)

    @staticmethod
    def save_library_metadata(library_type=None):
        if library_type == None or library_type == 'raw':
            cache_filepath = LocalLibraryMetadata.getif_cache_filepath('raw')
            with open(cache_filepath, "w") as writer:
                json.dump(LocalLibraryMetadata._cache_raw, writer, indent=4)
        if library_type == None or library_type == 'jpg':
            cache_filepath = LocalLibraryMetadata.getif_cache_filepath('jpg')
            with open(cache_filepath, "w") as writer:
                json.dump(LocalLibraryMetadata._cache_jpg, writer, indent=4)

    @staticmethod
    def load_library_metadata(library_type=None):
        if library_type == None or library_type == 'raw':
            cache_filepath = LocalLibraryMetadata.getif_cache_filepath('raw')
            with open(cache_filepath, "r") as reader:
                LocalLibraryMetadata._cache_raw = json.load(reader)

        if library_type == None or library_type == 'jpg':
            cache_filepath = LocalLibraryMetadata.getif_cache_filepath('jpg')
            with open(cache_filepath, "r") as reader:
                LocalLibraryMetadata._cache_jpg = json.load(reader)