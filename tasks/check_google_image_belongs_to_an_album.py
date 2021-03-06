import context; context.set_context()

import sys
import logging

import util
import gphoto
from gphoto.local_library import LocalLibrary
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    """
    Given an image pattern find the image and does it have a
    parent album.  Also find other related images
    Arguments:
        <patterns>: List of Image pattern
    """
    if len(sys.argv) < 2:
        logging.error("Too few arguments.  See help")
        return

    patterns = sys.argv[1:]
    print(patterns)


if __name__ == '__main__':
  main()