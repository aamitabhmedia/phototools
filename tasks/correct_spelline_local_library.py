import context; context.set_context()

import os
import sys
import logging

import util
import gphoto
from gphoto.local_library import LocalLibrary
from gphoto.local_library_metadata import LocalLibraryMetadata
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# -----------------------------------------------------
def main_library_type(old_word, new_word, library_type):

    LocalLibrary.load_library(library_type)
    LocalLibraryMetadata.load_library_metadata(library_type)

    library_cache = LocalLibrary.cache(library_type)
    albums = library_cache.get('albums')
    album_paths = library_cache.get('album_paths')
    album_names = library_cache.get('album_names')
    images = library_cache.get('images')
    image_ids = library_cache.get('image_ids')

    library_metadata_cache = LocalLibraryMetadata.cache(library_type)

    for image_path, image_metadata in library_metadata_cache.items():

        desc = image_metadata.get('Description')
        title = image_metadata.get('Title')
        if desc is None:
            desc = title
        
        if desc is None:
            continue

        if not type(desc) == str:
            continue

        # If misspelled word found in the images description
        # then try to correct it
        if old_word in desc:
            old_desc = desc
            new_desc = desc.replace(old_word, new_word)

            print(f"image='{image_path}'")
            print(f"    old='{old_desc}'")
            print(f"    new='{new_desc}'")

    for album in albums:
        album_path = album.get('path')
        if old_word in album_path:
            new_album_path = album_path.replace(old_word, new_word)
            print(f"album='{album_path}'")
            print(f"    old='{album_path}'")
            print(f"    new='{new_album_path}'")

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    """
    Takes word and its replacement
    """

    if len(sys.argv) < 3:
        logging("Too few args.  See help")
        return
    old_word = sys.argv[1]
    new_word = sys.argv[2]

    main_library_type(old_word, new_word, 'raw')

if __name__ == '__main__':
  main()