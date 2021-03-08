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

class LocalLibrary(object):
    """
    Class is responsible for building in-memory cache of the root
    folder containing all the images, saving to a local cache file,
    and loading from it.  The class holds cache for two target
    folders: 'raw' and 'jpg'.  These are defined as properties.
    So you can access them as follows:
        LocalLibray.cache_raw
        LocalLibray.cache_jpg
    Here is the structure of these  caches:

    _cache = {
        'cache_type': 'one of raw|jpg for now'
        'root_folder': <root pictures folder>,
        'albums': [list of albums],
        'album_paths': {
            {<album_path>: <album index into the list>},
                ...
        },
        'album_names': {
            {<album_path>: <album index into the list>},
                ...
        },
        'images': [array of images],
        'image_ids': {
            {<image_name>: <image[index]>},
        }
    }

    Each album object structure is as follows:
    album = {
        'name': <album folder leaf name>,
        'path': <full path of the album folder>,
        'parent': <parent album index>
        'images': [array of index into the image list]
    }

    Each image object is as follows
    image = {
        'name': <name of the image, file name>,
        'path': <full path of the image>,
        'metadata': {dict of metadata as seen by exiftool}
    }
    """

    _CACHE_RAW_FILE_NAME = 'local_library_raw.json'
    _CACHE_JPG_FILE_NAME = 'local_library_jpg.json'

    _cache_raw = None
    _cache_jpg = None

    # -------------------------------------------------
    # -------------------------------------------------
    @staticmethod
    def cache(library_type):
        return LocalLibrary._cache_raw if library_type == 'raw' else LocalLibrary._cache_jpg

    # -------------------------------------------------
    # -------------------------------------------------
    @staticmethod
    def cache_raw():
        return LocalLibrary._cache_raw

    # -------------------------------------------------
    # -------------------------------------------------
    @staticmethod
    def cache_jpg():
        return LocalLibrary._cache_jpg

    # -------------------------------------------------
    # -------------------------------------------------
    @staticmethod
    def getif_cache_filepath(library_type):
        filename = LocalLibrary._CACHE_RAW_FILE_NAME if library_type == 'raw' else LocalLibrary._CACHE_JPG_FILE_NAME
        return os.path.join(gphoto.cache_dir(), filename)

    # -------------------------------------------------
    # -------------------------------------------------
    @staticmethod
    def cache_library_recursive(root_folder, library_type, cache):

        # hold sections of cache as local variables
        albums = cache['albums']
        album_paths = cache['album_paths']
        album_names = cache['album_names']
        images = cache['images']
        image_ids = cache['image_ids']

        # Album will be added to library only if there are images in it
        album = None

        # Get all images under this folder
        folder_files = None
        for file in os.scandir(root_folder):
            if file.is_file():
                fileext = pathlib.Path(file.name).suffix.lower()
                if fileext in core.IMAGE_EXTENSIONS:
                    if not folder_files:
                        folder_files = []
                    folder_files.append(file)
                    # if file.name in cache:
                    #     cache[file.name].append(file.path)
                    # else:
                    #     cache[file.name] = [file.path]

        # if at least one image file found then add the images to the album
        # and then finally add the album to the album cache
        if folder_files is not None:

            # Create a new album object
            print(f"Working on album '{root_folder}'")
            album_name = os.path.basename(root_folder)
            album_images = []
            if album is None:
                album = {
                    'name': album_name,
                    'path': root_folder,
                    'images': album_images
                }

            # add album to the list and get its index
            albums.append(album)
            album_index = len(albums) - 1

            # Add album index to album dictionaries
            album_paths[root_folder] = album_index
            if album_name in album_names:
                logging.critical(f"DUPLICATE ALBUM NAME: '{album_name}', path: '{root_folder}'")
            album_names[album_name] = album_index

            # We require 3 operations for images:
            # 1. Add image to image list, get its index
            # 2. Add image index to image_ids
            # 3. Add image index to album image list
            # 4. Optionally load image metadata
            for file in folder_files:

                # Create image object
                metadata = {}
                image = {
                    'name': file.name,
                    'path': file.path,
                    'parent': album_index,
                    'mime': core.get_image_mime(file.name),
                    'metadata': metadata
                }

                # 1. Add image to image list, get its index
                images.append(image)
                image_index = len(images) - 1

                # 2. Add image index to image_ids
                image_ids[file.path] = image_index

                # 3. Add image index to album image list
                album_images.append(image_index)

        # Recurse to subdirs
        for subdir in os.scandir(root_folder):
            if subdir.is_dir():
                if subdir.name not in core.IGNORE_FOLDERS:
                    LocalLibrary.cache_library_recursive(subdir.path, library_type, cache)

    # -------------------------------------------------
    # -------------------------------------------------
    @staticmethod
    def cache_library(root_folder, library_type):
        cache = {
            'cache_type': library_type,
            'root_folder': root_folder,
            'albums': [],
            'album_paths': {},
            'album_names': {},
            'images': [],
            'image_ids': {}
        }
        if library_type == "raw":
            LocalLibrary._cache_raw = cache
            LocalLibrary.cache_library_recursive(root_folder, library_type, cache)

        elif library_type == "jpg":
            LocalLibrary._cache_jpg = cache
            LocalLibrary.cache_library_recursive(root_folder, library_type, cache)

    # -------------------------------------------------
    # -------------------------------------------------
    @staticmethod
    def save_library(library_type=None):
        if library_type == None or library_type == "raw":
            cache_filepath = LocalLibrary.getif_cache_filepath('raw')
            with open(cache_filepath, "w") as writer:
                json.dump(LocalLibrary._cache_raw, writer, indent=2)

        if library_type == None or library_type == "jpg":
            cache_filepath = LocalLibrary.getif_cache_filepath('jpg')
            with open(cache_filepath, "w") as writer:
                json.dump(LocalLibrary._cache_jpg, writer, indent=2)

    # -------------------------------------------------
    # -------------------------------------------------
    @staticmethod
    def load_library(library_type=None):
        if library_type == None or library_type == "raw":
            cache_filepath = LocalLibrary.getif_cache_filepath('raw')
            with open(cache_filepath, "r") as reader:
                LocalLibrary._cache_raw = json.load(reader)

        if library_type == None or library_type == "jpg":
            cache_filepath = LocalLibrary.getif_cache_filepath('jpg')
            with open(cache_filepath, "r") as reader:
                LocalLibrary._cache_jpg = json.load(reader)

