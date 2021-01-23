"""
Manages cache of local raw and jpg cache
"""
import os
import pathlib
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
        'album_dict': {
            {<album_path>: <albums[index]>},
                ...
        },
        'images': [array of images],
        'image_dict': {
            {<image_name>: <image[index]>},
        }
    }

    Each album object structure is as follows:
    album = {
        'name': <album folder leaf name>,
        'path': <full path of the album folder>
        'images': [array of index into the image list]
    }

    Each image object is as follows
    image = {
        'name': <name of the image, file name>,
        'path': <full path of the image>,
        'metadata': {dict of metadata as seen by exiftool}
    }
    """

    _cache_raw = None
    _cache_jpg = None

    @staticmethod
    def cache_library_recurse(root_folder, library_type, cache):

        # hold sections of cache as local variables
        albums = cache['albums']
        album_dict = cache['album_dict']
        images = cache['images']
        image_dict = cache['image_dict']

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
            if album is None:
                album = {
                    'name': os.path.basename(root_folder),
                    'path': root_folder,
                    'images': []
                }
            album_images = album['images']

            # add album to the list and get its index
            albums.append(album)
            album_index = len(albums) - 1

            # Add album index to album dictionary
            album_dict[root_folder] = album_index

            # We require 3 operations for images:
            # 1. Add image to image list, get its index
            # 2. Add image index to image_dict
            # 3. Add image index to album image list
            # 4. Optionally load image metadata
            for file in folder_files:

                # Create image object
                image = {
                    'name': file.name,
                    'path': file.path,
                    'metadata': []
                }

                # 1. Add image to image list, get its index
                images.append(image)
                image_index = len(images) - 1

                # 2. Add image index to image_dict
                image_dict[file.path] = image_index

                # 3. Add image index to album image list
                album_images.append(image_index)

                # 4. Optionally load image metadata
                # TODO: load metadata using exiftool

        # Recurse to subdirs
        for subdir in os.scandir(root_folder):
            if subdir.is_dir():
                if subdir.name not in core.IGNORE_FOLDERS:
                    LocalLibrary.cache_library_recurse(subdir.path, cache)







    @staticmethod
    def cache_library(root_folder, library_type):
        """
        Read the root folder and load it as album/image cache
        """
        # from the type find what cache to create
        cache = None
        if library_type == 'raw':
            LocalLibrary._cache_raw = {
                'cache_type': 'raw',
                'root_folder': root_folder,
                'albums': [],
                'album_dict': {},
                'images': [],
                'image_dict': {}
            }

        LocalLibrary.cache_library_recurse(root_folder, LocalLibrary._cache_raw)