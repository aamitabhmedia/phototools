import context; context.set_context()
import os
import json

import exiftool

from gphoto.local_library import LocalLibrary
from gphoto.imageutils import ImageUtils
import gphoto
import util
import sys
import logging
from datetime import datetime

import atexit

# -----------------------------------------------------------
# Find
# -----------------------------------------------------------
def find(et, file_filter_include, file_filter_exclude, list_only_albums):
    """
    This method expects that the folder has been scanned and cached
    Reference: https://akrabat.com/setting-title-and-caption-with-exiftool/

    The result will be saved to cache folder in the form:

        {
            "album_path": [list of image paths]
        }
    """

    LocalLibrary.load_raw_library()

    cache = LocalLibrary.cache_raw()
    images = cache['images']
    albums = cache['albums']

    result = {}
    
    # loop through all images. If image does not have comments
    # then add its album to album dictionary
    for image in images:
        image_name = image['name']
        image_path = image['path']

        # Apply file filters
        if file_filter_exclude and image_name.find(file_filter_exclude) > -1:
            continue
        if file_filter_include and image_path.find(file_filter_include) < 0:
            continue

        image_ext = ImageUtils.get_file_extension(image_name)
        is_video = ImageUtils.is_ext_video(image_ext)

        parent_album_idx = image['parent']
        album = albums[parent_album_idx]
        album_name = album['name']
        album_path = album['path']

        # if album already in the list then no need to get metadata
        # for this image, unless image names are desired as well
        result_album = None
        if album_name in result:
            result_album = result[album_path]
        else:
            result_album = []
            result[album_path] = result_album

        # check if any of the tags have any value
        # if the images has tag value then ignore this file
        comments = et.get_tags(ImageUtils._COMMENT_TAG_NAMES, image_path)
        comment = ImageUtils.get_any_comment(comments, is_video)
        if comment is not None:
            continue

        # Found at least one image with no comments
        # Add its album to the list
        result_album.append(image_path)

    saveto_filename = "albums_with_empty_caption"
    if file_filter_include is not None:
        saveto_filename += '_' + file_filter_include
    if list_only_albums:
        saveto_filename += '_' + "only_albums"

    saveto_filename += '.json'
    saveto = os.path.join(gphoto.cache_dir(), saveto_filename)
    print(f"Saving to: '{saveto}'")

    with open(saveto, "w") as cache_file:
        json.dump(result, cache_file, indent=2)

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
def main():
    start_time = datetime.now()

    file_filter_include = None
    file_filter_exclude = "PFILM"

    list_only_albums = False

    with exiftool.ExifTool() as et:
        result = find(et, file_filter_include, file_filter_exclude, list_only_albums)

    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

if __name__ == '__main__':
  main()