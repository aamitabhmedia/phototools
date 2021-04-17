import context; context.set_context()
from gphoto import google_albums

import os
import json
import logging

import gphoto
from gphoto.google_library import GoogleLibrary
from gphoto.local_library import LocalLibrary

def main():
    gphoto.init()

    # Load Google Library
    GoogleLibrary.load_library()
    google_cache = GoogleLibrary.cache()
    google_album_ids = google_cache['album_ids']
    google_album_titles = google_cache['album_titles']

    google_image_ids = google_cache['image_ids']
    google_image_filenames = google_cache['image_filenames']

    google_album_images = google_cache['album_images']
    google_image_albums = google_cache['image_albums']

    # Load Local picsHres jpg Library
    LocalLibrary.load_library('jpg')
    local_cache = LocalLibrary.cache_jpg()
    local_albums = local_cache.get('albums')
    local_album_paths = local_cache.get('album_paths')
    local_album_names = local_cache.get('album_names')
    local_images = local_cache.get('images')
    local_image_ids = local_cache.get('image_ids')

    # Initialize the result
    missing_images_with_album_reason = "MISSING_IMAGES_WITH_ALBUM"
    missing_images_with_no_album_reason = "MISSING_IMAGES_WITH_NO_ALBUM"
    image_exist_locally_reason = "IMAGE_EXIST_LOCALLY"

    result_missing_images_with_album = {}
    result_missing_images_with_no_album = []
    result_image_exist_locally = []
    result = {
        missing_images_with_album_reason: result_missing_images_with_album,
        missing_images_with_no_album_reason: result_missing_images_with_no_album,
        image_exist_locally_reason: result_image_exist_locally
    }

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

    # Walk through each Google images that begins with PFILMmmm_nnn.jpg
    for google_image_id in google_image_ids:
        google_image = google_image_ids[google_image_id]

        # Ignore images not begining with "PFILM"
        image_name = google_image.get('filename')
        if image_name is not None and not image_name.startswith("PFILM"):
            continue

        # Check for image exist locally
        local_image_id = local_image_ids.get(image_name)
        if local_image_id is not None:
            result_image_exist_locally.append(image_name)
            continue

        # We now know that the image is missing locally
        # No figure out if this images does not have an album parent
        if google_image_id in google_image_albums:

            # add first album to the result first if not already done
            google_albums_of_this_image = google_image_albums.get(google_image_id)
            google_album_id = None
            for id in google_albums_of_this_image:
                google_album_id = id
                break

            google_album = google_album_ids.get(google_album_id)
            missing_images_of_album = None
            if google_album_id not in result_missing_images_with_album:
                missing_images_of_album = []
                album = {
                    'id': google_album_id,
                    'title': google_album.get('title'),
                    'images': missing_images_of_album
                }
                result_missing_images_with_album[google_album_id] = album
            else:
                album = result_missing_images_with_album.get(google_album_id)
                missing_images_of_album = album.get('images')

            # Add the missing to parent album result
            missing_images_of_album.append({
                'id': google_image_id,
                'filename': image_name,
                'productUrl': google_image['productUrl']
            })

        # Google image is missing locally and has no parent album
        result_missing_images_with_no_album.append({
                'id': google_image_id,
                'filename': image_name,
                'productUrl': google_image['productUrl']
            })

    # Save to cache file also
    gphoto.save_to_file(result, "can_PFILMs_be_deleted.json")


if __name__ == '__main__':
  main()