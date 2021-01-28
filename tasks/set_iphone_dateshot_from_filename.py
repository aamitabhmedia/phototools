import context; context.set_context()
import os
from pathlib import Path
import logging
import sys
import json

import exiftool

import util
import gphoto
from gphoto.local_library import LocalLibrary


def main_with_exiftool(et, file_filter_pattern):
    """
    If date shot is missing in iPhone file then get it from
    the filename of the format is like: "2015-02-17 19.30.28.jpg"
    then update the dateshot from the filename
    """
    LocalLibrary.load_raw_library()

    result = {}

    # Walk through each file, split its file name for
    # comparison, and get date shot metadata
    cache = LocalLibrary.cache_raw()
    images = cache['images']
    albums = cache['albums']

    for image in images:
        image_name = image['name']
        image_path = image['path']

        # if filter is specified and does not match to the file path
        # then ignore the file
        if file_filter_pattern and image_path.find(file_filter_pattern) < 0:
            continue

        if not os.path.exists(image_path):
            continue

        # If the file has dateshot then ignore it
        tag = et.get_tag("Exif:DateTimeOriginal", image_path)
        if tag is not None:
            continue

        # at this point dateshot is missing
        # parse the file and check for format as "2015-02-17 19.30.28.jpg"
        splits = image_name.split(' ')
        if len(splits) != 2:
            continue
        file_date, file_time = splits
        if file_date is None or file_time is None:
            continue

def main():
    file_filter_pattern = "2015-02"
    with exiftool.ExifTool() as et:
        main_with_exiftool(et, file_filter_pattern)

if __name__ == '__main__':
  main()