import logging
import context; context.set_context()

import sys
import logging

import gphoto
from gphoto.goog_library import GoogLibrary

def main():
    """
    First step is to just load library from local cache.
    Then, based on the switches you update the im-memory cache.
    And then finally save the library to local cache
    Argument description:
        '-nll'  - No load library, if you don't want to load existing cache
        '-ca'   - Cache Album
        '-ci'   - Cache Images
        '-cai'   - Cache Album to Images relationship
    """
    if len(sys.argv) < 2:
        logging.critical("Too few arguments.  Please see help")
        return

    sw_no_load_library = False
    sw_cach_albums = False
    sw_cach_images = False
    sw_cache_album_images = False

    for arg in sys.argv[1:]:
        if arg == '-nll':
            sw_no_load_library = True
        elif arg == '-ca':
            sw_cach_albums = True
        elif arg == '-ci':
            sw_cach_images = True
        elif arg == '-cai':
            sw_cache_album_images = True
        else:
            logging.error(f"Unrecognized argument '{arg}'.  Please see help")
            return

    gphoto.init()

    if not sw_no_load_library:
        GoogLibrary.load_library()

    if sw_cach_albums:
        GoogLibrary.cache_albums()

    if sw_cach_images:
        GoogLibrary.cache_images()

    if sw_cache_album_images:
        GoogLibrary.cache_album_images()

    GoogLibrary.save_library()

if __name__ == '__main__':
  main()