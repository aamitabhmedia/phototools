import context; context.set_context()
import os
import sys
from pathlib import Path
import logging
import sys
import json

import gphoto
from googleapi.google_service import GoogleService
from googleapi.album_api import AlbumAPI
from gphoto.local_library import LocalLibrary

# ---------------------------------------------------------
# upload_folder
# ---------------------------------------------------------
def upload_folder(folder):
    print(f"--- Uploading Folder: '{folder}'")

    # Here is the process:
    # 1. Upload all the images first
    # 2. Create the album, make is sharable
    # 3. add images to the album

# ---------------------------------------------------------
# upload_folder_tree
# ---------------------------------------------------------
def upload_folder_tree(root):
    print(f"Uploading Tree: '{root}'")

# ---------------------------------------------------------
# main
# ---------------------------------------------------------
def main():
    """
    Uploads a folder and add its name as Google album

        -t Folder specific considered a tree of album folder
    """
    if len(sys.argv) < 2:
        logging.critical(f"Too few arguments.  Please see help")
        return

    # Parse the arguments
    arg_tree = False
    arg_folder = None

    for arg in sys.argv[1:]:
        if arg[0] == '-':
            if arg == '-t':
                arg_tree = True
            else:
                logging.critical(f"Bad switch '{arg}'")
                return
        else:
            arg_folder = arg

    # Validate arguments
    if arg_folder is None:
        logging.critical(f"[ERROR]: No folder is specified")
        return

    # Call upload functions now
    if arg_tree:
        upload_folder_tree(arg_folder)
    else:
        upload_folder(arg_folder)


if __name__ == '__main__':
  main()