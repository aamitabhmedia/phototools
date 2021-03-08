import context; context.set_context()

import os
import sys
import logging

import util
import gphoto
from gphoto.local_library import LocalLibrary
from gphoto.goog_library import GoogLibrary
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    """
    Takes word and its replacement
    """

    if len(sys.argv) < 3:
        logging("Too few args.  See help")
        return
    word = sys.argv[1]
    replacement = sys.argv[2]

    LocalLibrary.load_jpg_library()
    local_cache = LocalLibrary.cache_jpg()
    local_albums = local_cache.get('albums')
    local_album_paths = local_cache.get('album_paths')
    local_images = local_cache.get('images')

if __name__ == '__main__':
  main()