import context; context.set_context()
import os
import sys
from pathlib import Path
import logging
import sys
import json

from datetime import datetime

import exiftool

import util
import gphoto
from gphoto.local_library import LocalLibrary
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# Execute
# -----------------------------------------------------
def execute(album_path_filter):

    LocalLibrary.load_library('raw')

    album_path_filter_leaf = None
    if album_path_filter:
        album_path_filter_leaf = os.path.basename(album_path_filter)

    # The result is going to be of the form
    #     {
    #         "word": none,
    #             ...
    #     }
    result = {}

    # hold sections of cache as local variables
    cache = LocalLibrary.cache_raw()
    albums = cache['albums']
    album_paths = cache['album_paths']
    images = cache['images']
    image_ids = cache['image_ids']    


    # Loop through each album, get caption from it
    # if it follows standard naming convention
    for album in albums:

        # if folder is in the include list then continue
        # Otherwise ignore this album
        album_name = album['name']
        album_path = album['path']
        album_images = album['images']

        # filter out albums
        if album_path_filter and not album_path.startswith(album_path_filter):
            continue

        # Get words from album name
        words = album_name.split(' ')
        for word in words:
            if len(word) <= 3:
                result[word.capitalize()] = None

    saveto_filename = "get_small_words_in_album_names"
    if album_path_filter_leaf:
        saveto_filename += '_d' + album_path_filter_leaf

    saveto_filename += '.json'
    saveto = os.path.join(gphoto.cache_dir(), saveto_filename)
    print(f"Saving to: '{saveto}'")

    with open(saveto, "w") as cache_file:
        json.dump(result, cache_file, indent=2)

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    start_time = datetime.now()

    album_path_filter = None
    # album_path_filter = "p:\\pics\\2040"

    file_filter_include = None
    file_filter_exclude = "PFILM"
    
    execute(album_path_filter)
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

# -----------------------------------------------------
# -----------------------------------------------------
if __name__ == '__main__':
  main()