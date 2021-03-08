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