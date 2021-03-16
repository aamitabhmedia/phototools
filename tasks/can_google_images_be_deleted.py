import context; context.set_context()

import os
import sys
import logging

import util
import gphoto
from gphoto.local_library import LocalLibrary
from gphoto.google_library import GoogleLibrary
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# -----------------------------------------------------
def find_google_image(local_image, google_image_ids, google_image_filenames):

    # First find by filename.  We may get lucky
    google_image_id = google_image_filenames.get(local_image.get('name'))
    if google_image_id is not None:
        return (google_image_id, "MATCH-BY-NAME")
    
    # Tests if pattern is of the form
    #  YYYYMMDD_hhmmss_nn_AAAA_D800.jpeg
    #  YYYYMMDD_hhmmss_AAAA_D800.jpeg
    #  YYYYMMDD_hhmmss_AAAA.jpeg
    local_image_filename = local_image.get('name')
    local_image_filename_splits = local_image_filename.split('_')
    if len(local_image_filename_splits) < 2:
        return (None, "BAD-FILENAME")
    
    image_date = local_image_filename_splits[0]
    image_time = local_image_filename_splits[1]

    if not image_date.isdecimal() or not image_time.isdecimal():
        return (None, "NOT-DECIMAL")

    image_startswith_pattern = image_date + '_' + image_time
    for google_image_filename in google_image_filenames:
        if google_image_filename.startswith(image_startswith_pattern):
            return(google_image_filenames[google_image_filename], "MATCH-BY-TIMESTAMP")

    image_startswith_pattern = image_date + image_time
    for google_image_filename in google_image_filenames:
        if google_image_filename.startswith(image_startswith_pattern):
            return(google_image_filenames[google_image_filename], "MATCH-BY-TIMESTAMP")

    return (None, "UNKNOWN-PATTERN")

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    """
    Given a folder tree root like p:\\pics\\2014 loop through
    each album and find its images in Google photos.
    if the images do not have albums then they can be deleted.
    if the images have an album then
        and if the album have more images that the local album images
        and the albums is not shared then the images can be deleted
    """
    if len(sys.argv) < 2:
        logging.error("Too few arguments.  Specify folder pattern")
        return

    # Get arguments
    arg_album_year = sys.argv[1]
    arg_album_pattern = f"\\{arg_album_year}\\"

    LocalLibrary.load_library('jpg')
    local_cache = LocalLibrary.cache_jpg()
    local_albums = local_cache.get('albums')
    local_album_paths = local_cache.get('album_paths')
    local_images = local_cache.get('images')


    GoogleLibrary.load_library()
    google_cache = GoogleLibrary.cache()
    google_album_ids = google_cache['album_ids']
    google_album_titles = google_cache['album_titles']
    google_image_ids = google_cache['image_ids']
    google_image_filenames = google_cache['image_filenames']
    google_album_images = google_cache['album_images']
    google_image_albums = google_cache['image_albums']

    result = []

    # Loop through each local folder under the root tree
    for local_album in local_albums:
        local_album_path = local_album.get('path')

        # filter out the ones that are not under the tree
        if local_album_path.find(arg_album_pattern) == -1:
            continue
        # if not local_album_path.startswith(arg_album_pattern):
        #     continue

        # Add this album to the list
        result_album = {
            'path': local_album.get('path')
        }
        result.append(result_album)

        # Get first jpeg image of the local album
        first_local_image = None
        local_album_image_idxs = local_album.get('images')
        for local_album_image_idx in local_album_image_idxs:

            local_image = local_images[local_album_image_idx]
            if local_image.get('mime') == 'image/jpeg':
                first_local_image = local_image
                break

        if first_local_image is None:
            result_album['ERROR'] = f"No jpeg images in local album '{local_album.get('path')}'"
            continue

        result_album['first_image'] = first_local_image['name']

        # Locate this image in Google photos.  Identify the pattern
        # If the image is of the form
        #       YYYYMMDD_hhmmss_nn_AAAA_D800.jpeg
        # or just the actual name
        # First look for the images with actual name, if not found then
        # Look by date time in the filename

        first_google_image_id, pattern_found = find_google_image(
            first_local_image, google_image_ids, google_image_filenames)

        if first_google_image_id is None:
            result_album['WARNING'] = f"First album image not in Google {first_local_image.get('name')}"
            continue

        first_google_image = google_image_ids.get(first_google_image_id)
        result_album['first_google_image'] = {
            'id': first_google_image.get('id'),
            'filename': first_google_image.get('filename'),
            'mine': first_google_image.get('mine'),
            'productUrl': first_google_image.get('productUrl')
        }

        # if the first image part of google album then
        # we need to know if the image is part of a shared album
        google_image_album_list = google_image_albums.get(first_google_image_id)
        if google_image_album_list is None or len(google_image_album_list) <= 0:
            result_album['NO-GOOGLE-ALBUM'] = True
        else:
            result_image_albums = []
            result_album['HAS-ALBUMS'] = result_image_albums
            for google_image_album_id in google_image_album_list:
                google_album = google_album_ids.get(google_image_album_id)
                result_image_albums.append({
                    'id': google_album.get('id'),
                    'title': google_album.get('title'),
                    'productUrl': google_album.get('productUrl'),
                    'shared': google_album.get('shared')
                })

    gphoto.save_to_file(result, f"can_google_images_be_deleted_{arg_album_year}.json")


if __name__ == '__main__':
  main()