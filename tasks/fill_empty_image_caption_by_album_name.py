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

_ALBUM_PATTERN = "yy-mm-dd x"
_ALBUM_PATTERN_LEN = len(_ALBUM_PATTERN)

# -----------------------------------------------------
# Execute
# -----------------------------------------------------
def execute(et,
        album_path_filter,
        file_filter_include, file_filter_exclude,
        test_only):

    LocalLibrary.load_raw_library()

    # The result is going to be of the form
    #     {
    #         "bad_albums": {
    #             "...album path...": None,
    #                 ...
    #         },
    #         "good_albums": {
    #             "album_path": {
    #                 "caption": "...caption from the album folder...",
    #                 "images": [list of images that need captioning]
    #             }    
    #         }
    #     }
    result = {
        "bad_albums": {},
        "good_albums": {}
    }
    bad_albums = result["bad_albums"]
    good_albums = result["good_albums"]

    # Walk through each image
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

        image_ext = ImageUtils.get_file_extension(image_name)
        is_video = ImageUtils.is_ext_video(image_ext)

        # Need to rerun local library caching
        if not os.path.exists(image_path):
            print("Local library not updated.  Please rerun download_local_library again")
            exit

        caption_missing = False

        # Check if caption is empty
        comments = et.get_tags(ImageUtils._COMMENT_TAG_NAMES, image_path)
        if comments is None or len(comments) <= 0:
            caption_missing = True
        else:
            comment = ImageUtils.get_any_comment(comments, is_video)
            if comment is not None:
                caption_missing = True

        if not caption_missing:
            continue

        # cache parent album
        parent_index = image['parent']
        album = albums[parent_index]
        album_name = album['name']
        album_path = album['path']

        # Parse Caption from the album name
        # Album has to follow format to be used as Caption
        #       yy-mm-dd ...description
        bad_album = False
        if len(album_name) < _ALBUM_PATTERN_LEN:
            bad_album = True

        # Get the 
        if not bad_album:



# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    start_time = datetime.now()

    album_path_filter = "p:\\pics\\2012"

    file_filter_include = None
    file_filter_exclude = "PFILM"
    
    with exiftool.ExifTool() as et:
        execute(et,
            album_path_filter,
            file_filter_include, test_only=True
        )
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

# -----------------------------------------------------
# -----------------------------------------------------
if __name__ == '__main__':
  main()