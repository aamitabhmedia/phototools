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
# TODO: how to run all test.  right now the algorithm
# ignore subsequent tests if previous was satisfied
# Also mismatched_desc is only for date mismatch
# -----------------------------------------------------
def main():
    start_time = datetime.now()

    album_path_filter = "p:\\pics\\2012"

    file_filter_include = None
    file_filter_exclude = "PFILM"
    
    with exiftool.ExifTool() as et:
        find(et,
            album_path_filter,
            file_filter_include, file_filter_exclude,
            test_missing_date_shot=True, test_bad_date_shot=True,
            test_filename_FMT=True, test_tag_mismatch=True,
            test_missing_caption=True
        )
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

# -----------------------------------------------------
# -----------------------------------------------------
if __name__ == '__main__':
  main()