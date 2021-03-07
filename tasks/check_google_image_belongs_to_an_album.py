from typing import Pattern
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
    #   result = {
    #       'seed_image': {         #  first Images that matched the pattern
    #           'id': ...,
    #           'filename': ...,
    #           'creationTime'
    #       },
    #       'albums': [
    #           "album id": {
    #               'title': ....,
    #               'images': [
    #                   {
    #                       'id': ...,
    #                       'filename': ...,
    #                       'creationTime'
    #                   },
    #                       .....more imahes...
    #               ]
    #           },
    #               .... more albums ...
    #       ]
    #   }

    result_albums = []
    result = {
        'albums': result_albums
    }

    # Find images with the give patterns
    for google_image_id, google_image in google_image_ids.items():
        google_image_filename = google_image['filename']
        result_pattern = [p for p in patterns if p in google_image_filename]
        if result_pattern:

            # Add image to the result
            result['seed_image'] = {
                'id': google_image_id,
                'filename': google_image.get('filename'),
                'creationTime': google_image.get('mediaMetadata').get('creationTime')
            }

            # Get list of parent albums
            result_image_albums = google_image_albums.get(google_image_id)
            if result_image_albums is not None and len(result_image_albums) > 0:

                # For each album id in image parent list add it to the result
                for result_image_album_id in result_image_albums:
                    google_album = google_album_ids.get(result_image_album_id)

                    image_list = []
                    result_album = {
                        'id': result_image_album_id,
                        'title': google_album.get('title'),
                        'images': image_list
                    }

                    result_albums.append(result_album)

                    # Get the list of all images for this album and add to the result
                    result_album_image_ids = google_album_images.get(result_image_album_id)
                    for result_album_image_id in result_album_image_ids:
                        image = google_image_ids.get(result_album_image_id)
                        image_list.append(image.get('filename'))
                    image_list.sort()

            break

    util.pprint(result)


if __name__ == '__main__':
  main()