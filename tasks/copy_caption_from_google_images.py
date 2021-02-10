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

import gphoto
from gphoto.google_library import GoogleLibrary

def do_work(et, google_image_filter, album_folder_path):

    # Find folder album in the database
    LocalLibrary.load_raw_library()
    cache = LocalLibrary.cache_raw()
    images = cache['images']
    albums = cache['albums']

    for album in albums:
        album_path = album['path']
        if album_folder_path != album_path:
            continue

    print(f"[INFO]: Found album")

    # Collect list of folder files


# -----------------------------------------------------
# TODO: how to run all test.  right now the algorithm
# ignore subsequent tests if previous was satisfied
# Also mismatched_desc is only for date mismatch
# -----------------------------------------------------
def main():

    google_image_filter = "_ORKH"
    album_folder_path = "P:\\pics\\2010\\2010-07-02 Oregon Trip with Khadloyas"

    print("--------------------------------------------")
    print(f"filter: {google_image_filter}")
    print(f"folder: {album_folder_path}")
    print("--------------------------------------------")

    start_time = datetime.now()
    
    with exiftool.ExifTool() as et:
        do_work(et, google_image_filter, album_folder_path)
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

if __name__ == '__main__':
  main()