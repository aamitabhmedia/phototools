import context; context.set_context()

import os
import sys
import logging

import util
import gphoto
from gphoto.goog_library import GoogLibrary
from gphoto.imageutils import ImageUtils


# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    """
    Specify the year in which to narrow the search of images belonging to an album
    """
    if len(sys.argv) < 2:
        logging.error("Too few arguments.  See help")
        return

    # Get arguments
    arg_year = sys.argv[1]

    GoogLibrary.load_library()
    google_cache = GoogLibrary.cache()
    google_album_ids = google_cache['album_ids']
    google_album_titles = google_cache['album_titles']
    google_image_ids = google_cache['image_ids']
    google_image_filenames = google_cache['image_filenames']
    google_album_images = google_cache['album_images']
    google_image_albums = google_cache['image_albums']

    result_no_dateshot = []
    result_albums = {}
    result = {
        'no-dateshot': result_no_dateshot,
        'albums': result_albums
    }

    # Get dateshot.  If not there then report it
    for google_image_id, google_image in google_image_ids.items():
        dateShot = None
        image_metadata = google_image.get('mediaMetadata')
        if image_metadata:
            dateShot = image_metadata.get('creationTime')
        if dateShot is None:
            result_no_dateshot.append({
                'id': google_image_id,
                'productUrl': google_image.get('productUrl')
            })
            continue

        # We have a dateshot.  parse it and get the year
        # If year does not math then ignore the image
        image_year = dateShot.split('-')[0]
        if arg_year != image_year:
            continue

        # Get its google album and add it to the result
        google_image_album_object = google_image_albums.get(google_image_id)
        if google_image_album_object is None or len(google_image_album_object) <= 0:
            continue
    
        # This image has albums.  Add the albums to the results
        # and add the image to the albums
        for google_album_id in google_image_album_object:

            result_album = result_albums.get(google_album_id)
            result_album_images = None
            if result_album is None:
                google_album = google_album_ids.get(google_album_id)
                result_album_images = []
                result_album = {
                    'id': google_album_id,
                    'title': google_album.get('title'),
                    'productUrl': google_album.get('productUrl'),
                    'shared': google_album.get('shared'),
                    'images': result_album_images
                }
                result_albums[google_album_id] = result_album
            else:
                result_album_images = result_album.get('images')

            result_album_images.append((google_image_id, google_image.get('productUrl')))
            # result_album_images.append({
            #     'id': google_image_id,
            #     'productUrl': google_image.get('productUrl')
            # })

    gphoto.save_to_file(result, f"google_images_belonging_to_album_in_year_{arg_year}.json")

if __name__ == '__main__':
  main()