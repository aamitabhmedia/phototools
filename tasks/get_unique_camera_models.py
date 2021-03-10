import context; context.set_context()
import os
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
# Find
# -----------------------------------------------------
def find(et, album_path_filter, file_filter_include, file_filter_exclude):

    LocalLibrary.load_library('raw')

    # Result structure is of the form:
    #     result = {
    #         "model name": None,
    #             ...
    #     }
    result = {}

    album_path_filter_leaf = None
    if album_path_filter:
        album_path_filter_leaf = os.path.basename(album_path_filter)

    # Walk through each file, split its file name for
    # comparison, and get date shot metadata
    cache = LocalLibrary.cache_raw()
    images = cache['images']
    albums = cache['albums']

    for image in images:
        image_name = image['name']
        image_path = image['path']

        if file_filter_exclude and image_name.find(file_filter_exclude) > -1:
            continue
        if file_filter_include and image_path.find(file_filter_include) < 0:
            continue
        if album_path_filter and not image_path.startswith(album_path_filter):
            continue

        # Get model tag value
        value = None
        try:
            value = et.get_tag("Model", image_path)
        except Exception as e:
            value = None

        # Add the value to result
        result[value] = None

    saveto_filename = "get_unique_models"
    if album_path_filter_leaf:
        saveto_filename += '_d' + album_path_filter_leaf
    if file_filter_include is not None:
        saveto_filename += '_' + file_filter_include

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

    # album_path_filter = "p:\\pics\\2014"
    album_path_filter = None

    file_filter_include = None
    file_filter_exclude = "PFILM"
    
    with exiftool.ExifTool() as et:
        find(et,
            album_path_filter,
            file_filter_include, file_filter_exclude
        )
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

if __name__ == '__main__':
  main()