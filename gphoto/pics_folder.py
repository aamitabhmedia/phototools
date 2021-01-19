import os
from pathlib import Path
import json
import logging

import exiftool

from util.appdata import AppData
from util.log_mgr import LogMgr

class PicsFolder(object):

    _folder_cache = None
    _folder_cache_path = None

    _exiftool = None

    # -----------------------------------------------------
    # get local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return PicsFolder._folder_cache


    # -----------------------------------------------------
    # load recursively
    # -----------------------------------------------------
    @staticmethod
    def cache_recursive(root_folder):
        """
        Called itself recursively initiated by load function 
        """
        for root, directories, files in os.walk(root_folder, topdown=True):

            # If there are no images in this root folder then the album
            # variable will stay None
            album = None

            # Folder name will become album name
            folder_name = os.path.basename(root)

            # Loop through all files  in the current root folder
            # If a file is of ty image then add it to folder album
            # filename ==> image name
            # filepath ==> full path to image
            # fileext ==> image file type
            for filename in files:

                fileext = Path(filename).suffix.lower()

                if fileext in [".jpg", ".jpeg", ".png", ".gif"]:

                    if not album:
                        album = {
                            'name': folder_name,
                            'path': root,
                            'images': {}
                        }

                    filepath = os.path.join(root, filename)
                    image = {
                        'name': filename,
                        'path': filepath
                    }

                    # read metadata of the image
                    if PicsFolder._exiftool is None:
                        try:
                            PicsFolder._exiftool = exiftool.ExifTool()
                        except Exception as e:
                            logging.critical(f"cache_recursive: Unable to initialize exiftool")
                            raise
                    try:
                        metadata = PicsFolder._exiftool.get_metadata(filepath)
                        if metadata:
                            image['metadata'] = metadata
                    except Exception as e:
                        logging.error(f"Unable to get metadata for image '{filepath}'.  Metadata ignored")

                    album['images'][filename] = image

            # Add the new found album to the overall cache
            if album:
                PicsFolder._folder_cache.append(album)

            for dirname in directories:
                dirpath = os.path.join(root, dirname)
                PicsFolder.cache_recursive(dirpath)

    # --------------------------------------
    # Build cache of local photo folder 
    # --------------------------------------
    @staticmethod
    def cache_folder(root_folder):
        """
        Give the root folder it returns a list of folder objects
        Each folder object has:
            Folder name
            Folder Path
            Images - Dictionary of Image objects
        Each Image object has:
            Name
            Path
            Metadata - dictionary
            And possibly some metadata in the future
        """
        if not os.path.exists(root_folder):
            logging.error(f"folder not found: '{root_folder}'")
            return

        PicsFolder._folder_cache = []
        PicsFolder.cache_recursive(root_folder)
        return PicsFolder._folder_cache

    # --------------------------------------
    # Get path to local cache file
    # --------------------------------------
    @staticmethod
    def get_cache_filepath():

        cache_dir = os.path.join(Path.home(), AppData.APPDATA_NAME, "cache")
        p = Path(cache_dir)
        if (not p.exists()):
            try:
                p.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logging.critical(f"get_cache_filepath: Unable to create cache dir '{cache_dir}'.  Aborting")
                exit

        PicsFolder._folder_cache_path = os.path.join(cache_dir, "pics_folder_cache.json")
        return PicsFolder._folder_cache_path

    # --------------------------------------
    # Save cache to local file system 
    # --------------------------------------
    @staticmethod
    def save_cache():
        cache_filepath =PicsFolder.get_cache_filepath()

        try:
            cache_file = open(cache_filepath, "w")
            json.dump(PicsFolder._folder_cache, cache_file, indent=2)
            cache_file.close()
            logging.info(f"PicsFolder:save_cache: Successfully saved folder pics cache to '{cache_filepath}'")
            return True
        except Exception as e:
            logging.critical(f"PicsFolder:save_cache: unable to save folder pics cache locally")
            raise
    # --------------------------------------
    # Load cache from saved run
    # --------------------------------------
    @staticmethod
    def load_cache():
        """
        Loads in-memory cache from local cache file
            Return: cache object
        You can also get the cache object later
        by calling cache() defined in this file
        """

        # We will reload the cache from local file
        PicsFolder._folder_cache = None

        cache_filepath = PicsFolder.get_cache_filepath()
        if not os.path.exists(cache_filepath):
            logging.warning(f"PicsFolder:load_cache: No mediaItem cache file available.  Ignored")
            return

        try:
            cache_file = open(cache_filepath)
        except Exception as e:
            logging.critical(f"PicsFolder:load_cache: Unable top open mediaItems cache file")
            raise

        try:
            PicsFolder._folder_cache = json.load(cache_file)
            logging.info(f"PicsFolder:load_cache: Successfully loaded folder pics cache from '{cache_filepath}'")
        except Exception as e:
            PicsFolder._folder_cache = None
            logging.error(f"PicsFolder:load_cache: Error occurred while loading pics folder cache")
            raise

        return PicsFolder._folder_cache
