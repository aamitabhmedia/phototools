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

_CSV_FILEPATH = os.path.join(tempfile.gettempdir(), 'image_library_metadata.csv')

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
    def cache_any_library_metadata(root_folder, library_type, cache):

        # Build the exiftool batch csv command
        cmd = ['exiftool', '-q', '-csv', '-r']
        for tag in _METADATA_TAGS:
            cmd.append(tag)
        for ext in core.MEDIA_EXTENSIONS:
            cmd.append('-ext')
            cmd.append(ext)
        cmd.append(root_folder)

        logging.info(f"cmd: {cmd}")
        logging.info(f"csv: {_CSV_FILEPATH}")

        # Execute the command and redirect to a csv file
        with open(_CSV_FILEPATH, "w") as writer:
            subprocess.run(cmd, stdout=writer)

        cache = {}

        # Load the csv file into a cache format
        with open(_CSV_FILEPATH) as reader:
            csv_reader = csv.reader(reader, delimiter=',')

            first_row = True
            columns = None
            num_columns = 0
            for row in csv_reader:
                if first_row:
                    first_row = False
                    columns = row
                    num_columns = len(columns)
                else:
                    metadata = {}
                    cache[row[0]] = metadata
                    
                    for idx, column in enumerate(columns):
                        if idx == 0:
                            continue
                        metadata[column] = row[idx]
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
            LocalLibraryMetadata.save_any_cache(cache_filepath, LocalLibraryMetadata._cache_raw)
        if library_type == None or library_type == 'jpg':
            cache_filepath = LocalLibraryMetadata.getif_cache_filepath('jpg')
            LocalLibraryMetadata.save_any_cache(cache_filepath, LocalLibraryMetadata._cache_jpg)

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