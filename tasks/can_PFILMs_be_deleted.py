import context; context.set_context()

import os
import json
import logging

import gphoto
from gphoto.google_library import GoogleLibrary
from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages
from gphoto.google_album_images import GoogleAlbumImages
from gphoto.local_library import LocalLibrary

def main():
    gphoto.init()

    GoogleLibrary.load_library()

    cache = GoogleLibrary.cache()
    google_album_ids = cache['album_ids']
    google_album_titles = cache['album_titles']

    google_image_ids = cache['image_ids']
    google_image_filenames = cache['image_filenames']

    google_album_images = cache['album_images']
    google_image_albums = cache['image_albums']

    # Initialize the result
    error_missing_images = "MISSING_IMAGES"
    error_has_album = "HAS_ALBUM"

    missing_parent_album_id = "MISSING_PARENT_ALBUM_ID"
    missing_parent_album_title = "MISSING_PARENT_ALBUM_TITLE"
    missing_parent_album_images = []
    missing_parent_album_placeholder = {
        'title': missing_parent_album_title,
        'images': missing_parent_album_images
    }
    result = {
        missing_parent_album_id: missing_parent_album_placeholder
    }

    result_missing_images = []
    result_has_album = {}
    result = {
        error_missing_images: result_missing_images,   # list of google images not available locally 
        error_has_album: result_has_album         # list of albums that are parent to PFILM images
    }

    # Walk through each images that begins with PFILMmmm_nnn.jpg
    # If the image belongs to an album then add the album to the result
    for google_image_id in google_image_ids:
        google_image = google_image_ids[google_image_id]

        image_name = google_image.get('filename')
        if image_name is not None and not image_name.startswith("PFILM"):
            continue

        # if parent album then PFILM can not be deleted
        # Walk through the list and add them to the result
        if google_image_id in google_image_albums:



            missing_parent_album_images.append({
                'id': google_image_id,
                'filename': image_name,
                'productUrl': google_image['productUrl']
            })

            google_albums_of_this_image = google_image_albums.get(google_image_id)
            for google_album_id in google_albums_of_this_image:

                # This is the first time the album is seen 
                if google_album_id not in result_has_album:
                    google_album = google_album_ids[google_album_id]
                    title = google_album.get('title')
                    
                    result_album = {
                        'title': title,
                        'shared': google_album.get('shared'),
                        'images': [{
                            'id': google_image_id,
                            'filename': image_name,
                            'productUrl': google_image.get('productUrl')
                        }]
                    }

                    result_has_album[google_album_id] = result_album

                # Album already exist in result.  Just add the image to it
                else:
                    result_album = result[google_album_id]
                    result_album_image_list = result_album['images']
                    result_album_image_list.append({
                        'id': google_image_id,
                        'filename': image_name,
                        'productUrl': google_image['productUrl']
                    })

    # Save to cache file also
    gphoto.save_to_file(result, "can_PFILMs_be_deleted.json")


if __name__ == '__main__':
  main()