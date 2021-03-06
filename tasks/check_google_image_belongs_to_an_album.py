import context; context.set_context()

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
    Given an image pattern find the image and does it have a
    parent album.  Also find other related images
    Arguments:
        <patterns>: List of Image pattern
    """
    if len(sys.argv) < 2:
        logging.error("Too few arguments.  See help")
        return

    # Get arguments
    patterns = sys.argv[1:]
    print(patterns)

    # Load cache
    GoogLibrary.load_library()
    cache = GoogLibrary.cache()
    google_album_ids = cache['album_ids']
    google_album_titles = cache['album_titles']
    google_image_ids = cache['image_ids']
    google_image_filenames = cache['image_filenames']
    google_album_images = cache['album_images']
    google_image_albums = cache['image_albums']

    # Define the result
      result = {
          'album': {
              'id': ....,
              'title': ...
          }
      }

    # Find images with the give patterns
    for google_image_id, google_image in google_album_ids.items():
        google_image_filename = google_image['filename']
        if patterns in google_image_filename:

if __name__ == '__main__':
  main()