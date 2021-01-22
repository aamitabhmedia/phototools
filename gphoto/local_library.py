"""
"""

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
    def cache_library_of_type(root_folder, library_type, cache):

        # Traverse the folders

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

        LocalLibrary.cache_library_of_type(root_folder, library_type, LocalLibrary._cache_raw)