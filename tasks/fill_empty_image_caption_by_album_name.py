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
# Execute
# -----------------------------------------------------
def execute(
    et,
    album_path_filter,
    file_filter_include, file_filter_exclude,
    test_only):
    """
    """
    LocalLibrary.load_raw_library()

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

        image_ext = ImageUtils.get_file_extension(image_name)
        is_video = ImageUtils.is_ext_video(image_ext)

        # Need to rerun local library caching
        if not os.path.exists(image_path):
            print("Local library not updated.  Please rerun download_local_library again")
            exit

        caption_missing = False

        # Check if caption is empty
        tag = None
        if not is_video:
            tag = et.get_tag("Exif:DateTimeOriginal", image_path)
            if tag is None or len(tag) <= 0:
                tag = et.get_tag("Exif:CreateDate", image_path)
                if tag is None or len(tag) <= 0:
                    caption_missing = True
        else:
            tag = et.get_tag("QuickTime:CreateDate", image_path)
            if tag is None or len(tag) <= 0:
                caption_missing = True

        # Caption is missing.  If it is test only then capture
        # the result and it will be printed

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