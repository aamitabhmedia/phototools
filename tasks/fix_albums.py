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
def fix_albums(et, album_path_filter, test_only):

    LocalLibrary.load_raw_library()

    album_path_filter_leaf = None
    if album_path_filter:
        album_path_filter_leaf = os.path.basename(album_path_filter)


# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    """
    The script will rename the images under a folder,
    and will add comments to images that are missing
    Parameters: All mandatory
        album_folder:
            This can be a parent folder containing
            other albums.  The folder should exists

        image_acronym:
            Exaple: YYYYMMDD_hhmmss_<acronym>.jpg
        
        -test_only | -t: only test but not execute
    
    Pre-requisites:  Please see Tasks.md for details
    """
    start_time = datetime.now()

    album_path_filter = "p:\\pics\\2040"
    
    with exiftool.ExifTool() as et:
        execute(et,
            album_path_filter,
            file_filter_include, file_filter_include, test_only=False
        )
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

# -----------------------------------------------------
# -----------------------------------------------------
if __name__ == '__main__':
  main()