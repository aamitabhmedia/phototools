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

    google_album_cache = GoogleAlbums.cache()
    google_album_ids = google_album_cache['ids']
    google_album_titles = google_album_cache['titles']

    google_image_cache = GoogleImages.cache()
    google_image_ids = google_image_cache['ids']
    google_image_filenames = google_image_cache['filenames']

    google_album_image_cache = GoogleAlbumImages.cache()
    google_album_images = google_album_image_cache['album_images']
    google_image_albums = google_album_image_cache['image_albums']

    # Initialize the result
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

    # Walk through each images that begins with PFILMmmm_nnn.jpg
    # If the image belongs to an album then add the album to the result
    for google_image_id in google_image_ids:
        google_image = google_image_ids[google_image_id]

        image_name = google_image['filename']
        if not image_name.startswith("PFILM"):
            continue

        # if no parent album then PFILM can be deleted
        if google_image_id not in google_image_albums or google_image_albums[google_image_id] is None:
            missing_parent_album_images.append({
                'id': google_image_id,
                'filename': image_name,
                'productUrl': google_image['productUrl']
            })

        # PFILM image has parent albums.  Walk through the list and add them to the result
        else:
            google_albums_of_this_image = google_image_albums[google_image_id]
            for google_album_id in google_albums_of_this_image:

                # This is the first time the album is seen 
                if google_album_id not in result:
                    google_album = google_album_ids[google_album_id]
                    title = "NONE"
                    if 'title' in google_album:
                        title = google_album['title']
                    
                    result_album = {
                        'title': title,
                        'shared': google_album['shared'],
                        'images': [{
                            'id': google_image_id,
                            'filename': image_name,
                            'productUrl': google_image['productUrl']
                        }]
                    }

                    result[google_album_id] = result_album

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