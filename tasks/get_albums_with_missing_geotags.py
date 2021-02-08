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

    LocalLibrary.load_raw_library()

    # Result structure is of the form:
        # result {
        #     "album path": {
        #       "total": <total number of images in this folder>,
        #       "count": <number of images missing geotag info>,
        #       "is_missing": true|false
        #     }
        #         ...
        # }
    result = {}

    album_path_filter_leaf = None
    if album_path_filter:
        album_path_filter_leaf = os.path.basename(album_path_filter)

    # Walk through each file, split its file name for
    # comparison, and get date shot metadata
    cache = LocalLibrary.cache_raw()
    albums = cache['albums']
    images = cache['images']

    for album in albums:

        album_name = album['name']
        album_path = album['path']
        album_images = album['images']
        album_image_count = len(album_images)

        # filter out albums
        if album_path_filter and not album_path.startswith(album_path_filter):
            continue

        for image_idx in album_images:
            image = images[image_idx]
            image_name = image['name']
            image_path = image['path']

            if file_filter_exclude and image_name.find(file_filter_exclude) > -1:
                continue
            if file_filter_include and image_path.find(file_filter_include) < 0:
                continue
            if album_path_filter and not image_path.startswith(album_path_filter):
                continue

            # [Composite]     GPSLatitude                     : 37 deg 39' 2.42" N
            # [Composite]     GPSLongitude                    : 121 deg 52' 14.23" W

            # Get GPS tag values
            value = None
            try:
                value = et.get_tags(["GPSLatitude", "GPSLongitude", "GPSLatitudeRef", "GPSLongitudeRef"], image_path)
            except Exception as e:
                value = None
            
            if value is None or len(value) < 4:
                result_album = None                
                if album_path not in result:
                    result_album = {
                        "total": album_image_count,
                        "count": 1,
                    }
                    result[album_path] = result_album
                else:
                    result_album = result[album_path]
                    result_album['count'] = result_album['count'] + 1

    # Generate a list where all/partial images are missing in an album
    # The format of the resout value is:
    #     result2 = {
    #         "all": [list of albums],
    #         "partial": [list of albums where some inages dont have geotag info]
    #     }

    # For the case of all the format of return is:
    #     [
    #         "album_path",
    #             ...
    #     ]

    # For partial the result is:
    #     [
    #         {album object},
    #             ...
    #     ]

    result2 = {
        'all': [],
        'partial': []
    }
    result2_all = result2['all']
    result2_partial = result2['partial']

    for result_album_path, result_album in result.items():
        total = result_album['total']
        count = result_album['count']
        if total == count:
            result2_all.append(result_album_path)
        else:
            result2_partial.append(result_album)

    saveto_filename = "get_albums_with_missing_geotags"
    if album_path_filter_leaf:
        saveto_filename += '_d' + album_path_filter_leaf
    if file_filter_include is not None:
        saveto_filename += '_' + file_filter_include

    saveto_filename += '.json'
    saveto = os.path.join(gphoto.cache_dir(), saveto_filename)
    print(f"Saving to: '{saveto}'")

    with open(saveto, "w") as cache_file:
        json.dump(result2, cache_file, indent=2)


# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    start_time = datetime.now()

    album_path_filter = "p:\\pics\\2012"
    # album_path_filter = None

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