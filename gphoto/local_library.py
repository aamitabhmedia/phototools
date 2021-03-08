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
    _cache_raw_path = None
    _cache_jpg_path = None

    @staticmethod
    def cache_raw():
        return LocalLibrary._cache_raw

    @staticmethod
    def cache_jpg():
        return LocalLibrary._cache_jpg

    @staticmethod
    def cache_library_recursive(et, root_folder, library_type, cache):

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

                # Load image metadata
                image_ext = ImageUtils.get_file_extension(file.name)
                is_video = ImageUtils.is_ext_video(file.name)
                metadata['date_shot'] = ImageUtils.get_date_shot(et, file.path, is_video)
                metadata['caption'] = ImageUtils.get_caption(et, file.path, is_video)

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
                    LocalLibrary.cache_library_recursive(et, subdir.path, library_type, cache)

    @staticmethod
    def getif_cache_filepath(library_type):
        """
        Library type can be one of 'raw' or 'jpg'
        """
        if library_type == 'raw':
            LocalLibrary._cache_raw_path = os.path.join(gphoto.cache_dir(), LocalLibrary._CACHE_RAW_FILE_NAME)
            return LocalLibrary._cache_raw_path
        else:
            LocalLibrary._cache_jpg_path = os.path.join(gphoto.cache_dir(), LocalLibrary._CACHE_JPG_FILE_NAME)
            return LocalLibrary._cache_jpg_path

    @staticmethod
    def cache_raw_library(root_folder):
        """
        """
        # from the type find what cache to create
        LocalLibrary._cache_raw = {
            'cache_type': 'raw',
            'root_folder': root_folder,
            'albums': [],
            'album_paths': {},
            'album_names': {},
            'images': [],
            'image_ids': {}
        }
        with exiftool.ExifTool() as et:
            LocalLibrary.cache_library_recursive(et, root_folder, 'raw', LocalLibrary._cache_raw)

    @staticmethod
    def cache_jpg_library(root_folder):
        """
        """
        # from the type find what cache to create
        LocalLibrary._cache_jpg = {
            'cache_type': 'jpg',
            'root_folder': root_folder,
            'albums': [],
            'album_paths': {},
            'album_names': {},
            'images': [],
            'image_ids': {}
        }
        LocalLibrary.cache_library_recursive(et, root_folder, 'jpg', LocalLibrary._cache_jpg)


    @staticmethod
    def cache_library_metadata(cache, tag_names):
        """
        TODO: Implementation
        For each images the specific metadata will be added to the
        image objects in the images field of the cache
        """
        # Make sure cache is loaded
        if cache == None or 'images' not in cache:
          logging.error("LocalLibrary.cache_library_metadata: Cache is not loaded")
          raise Exception("LocalLibrary.cache_library_metadata: Cache is not loaded")

        # Walk through the list of images and load its metadata
        images = cache['images']
        for image in images:
          # TODO: implement
          pass

    @staticmethod
    def cache_raw_library_metadata(tag_names):
        LocalLibrary.cache_library_metadata(LocalLibrary.cache_raw, tag_names)

    @staticmethod
    def cache_jpg_library_metadata(tag_names):
        LocalLibrary.cache_library_metadata(LocalLibrary.cache_jpg, tag_names)

    @staticmethod
    def save_any_library(cache_filepath, cache):
        try:
            cache_file = open(cache_filepath, "w")
            json.dump(cache, cache_file, indent=2)
            cache_file.close()
            logging.info(f"LocalLibrary.save_any_cache: Successfully saved local library cache to '{cache_filepath}'")
            return True
        except Exception as e:
            logging.critical(f"LocalLibrary.save_any_cache: unable to savelocal library cache to '{cache_filepath}'")
            raise

    @staticmethod
    def save_raw_library():
        cache_filepath = LocalLibrary.getif_cache_filepath('raw')
        LocalLibrary.save_any_library(cache_filepath, LocalLibrary._cache_raw)

    @staticmethod
    def save_jpg_library():
        cache_filepath = LocalLibrary.getif_cache_filepath('jpg')
        LocalLibrary.save_any_library(cache_filepath, LocalLibrary._cache_jpg)

    @staticmethod
    def load_any_library(cache_filepath):

        cache_file = None
        try:
            cache_file = open(cache_filepath)
        except Exception as e:
            logging.critical(f"LocalLibrary.load_any_library: Unable top open local library cache file")
            raise

        try:
            cache = json.load(cache_file)
            logging.info(f"LocalLibrary.load_any_library: Successfully loaded local library from file '{cache_filepath}'")
            return cache
        except Exception as e:
            logging.error(f"LocalLibrary.load_any_library: Error occurred while loading local library cache")
            raise

    @staticmethod
    def load_raw_library():
        LocalLibrary._cache_raw = {}
        cache_filepath = LocalLibrary.getif_cache_filepath('raw')
        LocalLibrary._cache_raw = LocalLibrary.load_any_library(cache_filepath)

    @staticmethod
    def load_jpg_library():
        LocalLibrary._cache_jpg = {}
        cache_filepath = LocalLibrary.getif_cache_filepath('jpg')
        LocalLibrary._cache_jpg = LocalLibrary.load_any_library(cache_filepath)
