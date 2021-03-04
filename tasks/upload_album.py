import context; context.set_context()
import os
from pathlib import Path
import logging
import sys
import json

import gphoto
from gphoto.local_library import LocalLibrary

# ---------------------------------------------------------
# Uploader class has methods to upload local albums
# and its images
# ---------------------------------------------------------
class Uploader:

    # -------------------------------------
    # Upload album for a given folder name
    # -------------------------------------
    def uploadAlbum(album_names):


def main():
    gphoto.init()
    LocalLibrary.load_jpg_library()

if __name__ == '__main__':
  main()