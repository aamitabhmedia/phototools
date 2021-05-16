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
    

# ---------------------------------------------------------
# upload_folder_tree
# ---------------------------------------------------------
def upload_folder_tree(folder):
    pass

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
    argv_folderIsTree = False
    argv_rootFolder = None

    for arg in sys.argv[2:]:
        if arg[0] == '-':
            if arg[0] == '-t':
                argv_folderIsTree = True
            else:
                logging.critical(f"Bad switch '{arg}'")
                return
        else:
            argv_rootFolder = arg

    # Validate arguments
    if argv_rootFolder is None:
        logging.critical(f"[ERROR]: No folder is specified")
        return

    # Call upload functions now
    if argv_folderIsTree:
        upload_folder_tree(argv_rootFolder)
    else:
        upload_folder(argv_rootFolder)


if __name__ == '__main__':
  main()