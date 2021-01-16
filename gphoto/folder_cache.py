import logging
import os
import pathlib


def load_cache(root_folder, folder_cache):
    """
    Called itself recursively initiated by load_cache function 
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

                filepath = os.path.join(root, filename)

                if not album:
                    album = {
                        'name': folder_name,
                        'path': root,
                        'images': []
                    }

                image = {
                    'name': filename,
                    'path': filepath
                }

                album['images'].append(image)

        # Add the new found album to the overall cache
        if album:
            folder_cache.append(album)

        for dirname in directories:
            dirpath = os.path.join(root, dirname)
            load(dirpath, folder_cache)

def load(root_folder):
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

    cache = []
    load_cache(root_folder, cache)
    return cache