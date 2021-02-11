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
# add_year_prefix
# -----------------------------------------------------
def add_year_prefix(et, album_path, test_only):


# -----------------------------------------------------
# main
# -----------------------------------------------------
def main():

    # album_path = "p:\\pics\\2012"

    if len(sys.argv) > 1:
        album_path = sys.argv[1]
    else:
        print("ERROR: Missing album path")

    print("--------------------------------------------")
    print(f"filter: {album_path_filter}")
    print("--------------------------------------------")

    start_time = datetime.now()

    file_filter_include = None
    file_filter_exclude = "PFILM"
    
    with exiftool.ExifTool() as et:
        add_year_prefix(et, album_path, test_only)
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

if __name__ == '__main__':
  main()