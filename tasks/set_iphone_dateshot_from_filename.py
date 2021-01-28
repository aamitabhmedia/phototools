import context; context.set_context()
import os
import subprocess
from pathlib import Path
import logging
import sys
import json

import exiftool

import util
import gphoto
from gphoto.local_library import LocalLibrary
from gphoto.exiftutils import ExifUtils


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

        file_date_splits = file_date.split('-')
        if len(file_date_splits) < 3:
            continue

        file_time_splits = file_time.split('.')
        if len(file_time_splits) < 4:
            continue

        dateshot = ':'.join(file_date_splits) + ' ' + ':'.join(file_time_splits[0:3])

        # cmd = "\"-" + ExifUtils._TAGIPTCObjectName + '=' + dateshot + '"'
        # cmd += "\" -" + ExifUtils._TAGIPTCCaptionAbstract + '=' + dateshot + '"'
        # cmd += "\" -" + ExifUtils._TAGExifImageDescription + '=' + dateshot + '"'
        # cmd += "\" -" + ExifUtils._TAGXmpDescription + '=' + dateshot + '"'

        # ret = subprocess.run(["exiftool", f"-EXIF:DateTimeOriginal={dateshot}", "-EXIF:CreateDate={dateshot}", "-overwrite_original", "-P", image_path])
        ret = subprocess.run(["exiftool", f"-EXIF:DateTimeOriginal={dateshot}", "-overwrite_original", "-P", image_path])
        print(f"retcode: {ret.returncode}, {dateshot}, {image_path}")

def main():
    file_filter_pattern = None
    with exiftool.ExifTool() as et:
        main_with_exiftool(et, file_filter_pattern)

if __name__ == '__main__':
  main()