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

_FILEPREFIX_PATTERN = "yyyymmdd_hhmmss_XXXX"
_FILEPREFIX_PATTERN_LEN = len(_FILEPREFIX_PATTERN)

# -----------------------------------------------------
# Execute
# -----------------------------------------------------
def execute(file_filter_include, file_filter_exclude):

    LocalLibrary.load_library('raw')()

    # Result format is:
    # {
    #     "acronym": [list of image paths],
    #         ...
    # }
    result = {}
    albums_seen = {}

    cache = LocalLibrary.cache_raw()
    albums = cache['albums']
    images = cache['images']

    for image in images:

        image_name = image['name']
        image_path = image['path']

        if file_filter_exclude and image_name.find(file_filter_exclude) > -1:
            continue
        if file_filter_include and image_path.find(file_filter_include) < 0:
            continue

        # Need to rerun local library caching
        if not os.path.exists(image_path):
            msg="Local library not updated.  Please rerun download_local_library again"
            sys.exit(msg)

        # check if file name conforms to yyyymmdd_hhmmss_XXXX
        if len(image_name) < _FILEPREFIX_PATTERN_LEN:
            continue
        image_basename = os.path.splitext(image_name)[0]
        image_name_splits = image_basename.split('_')
        if len(image_name_splits) < 3:
            continue
        image_date = image_name_splits[0]
        image_time = image_name_splits[1]
        image_acronym = '_'.join(image_name_splits[2:])
        if len(image_date) < 8 or len(image_time) < 6:
            continue

        # Get parent album
        album_idx = image['parent']
        album = albums[album_idx]
        album_name = album['name']
        album_path = album['path']

        # if the combination of album name and acronym has already
        # been seen the ignore rest of the images in this album
        album_plus_acronym = album_name + '__' + image_acronym
        if album_plus_acronym in albums_seen:
            continue
        else:
            albums_seen[album_plus_acronym] = None

        # add image acronym and image_path to the result
        if image_acronym not in result:
            image_list = [image_path]
            result[image_acronym] = image_list
        else:
            image_list = result[image_acronym]
            image_list.append(image_path)

    # filter out acronyms where there are no duplicates
    final_result = {}
    for acronym in result.keys():

        image_list = result[acronym]
        if len(image_list) > 1:
            final_result[acronym] = image_list

    saveto_filename = "test_dup_file_acronym"
    if file_filter_include is not None:
        saveto_filename += '_' + file_filter_include

    saveto_filename += '.json'
    saveto = os.path.join(gphoto.cache_dir(), saveto_filename)
    print(f"Saving to: '{saveto}'")

    with open(saveto, "w") as cache_file:
        json.dump(final_result, cache_file, indent=2)


# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    start_time = datetime.now()

    file_filter_include = None
    file_filter_exclude = "PFILM"
    
    execute(file_filter_include, file_filter_include)
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

# -----------------------------------------------------
# -----------------------------------------------------
if __name__ == '__main__':
  main()