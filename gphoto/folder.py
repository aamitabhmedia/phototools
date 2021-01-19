import logging
import os
import pathlib

class Folder(object):

    _folder_cache = None

    # -----------------------------------------------------
    # get local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return Folder._folder_cache


    # -----------------------------------------------------
    # load recursively
    # -----------------------------------------------------
    @staticmethod
    def load_folder_recursive(root_folder):
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

                fileext = pathlib.Path(filename).suffix.lower()

                if fileext in [".jpg", ".jpeg", ".png", ".gif"]:

                    if not album:
                        album = {
                            'name': folder_name,
                            'path': root,
                            'images': []
                        }

                    filepath = os.path.join(root, filename)
                    image = {
                        'name': filename,
                        'path': filepath
                    }

                    album['images'].append(image)

            # Add the new found album to the overall cache
            if album:
                Folder._folder_cache.append(album)

            for dirname in directories:
                dirpath = os.path.join(root, dirname)
                Folder.load_folder_recursive(dirpath)

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
            List of Image objects
        Each Image object has:
            Name
            Path
            And possibly some metadata in the future
        """
        if not os.path.exists(root_folder):
            logging.error(f"folder not found: '{root_folder}'")
            return

        Folder._folder_cache = []
        load_folder_recursive(root_folder)
        return True

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
                logging.critical(f"media_mgr:cache_filepath: Unable to create cache dir '{cache_dir}'.  Aborting")
                exit

        Library._library_cache_path = os.path.join(cache_dir, "folder_cache.json")
        return Library._library_cache_path

    # --------------------------------------
    # Save cache to local file system 
    # --------------------------------------
    @staticmethod
    def save_cache():