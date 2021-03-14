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

    return (None, "UNKNOWN-PATTERN")

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    """
    Collect all the images with the date shot of the given year.
    Check if they follow the YYYYMMDD_HHMMDD_.... format
    If all follow this format then images of the whole year can be deleted
        in one shot.
    Otherwise list out the odd image months from the date shot as culprits.
    For each of these images see in the local folder album what to do.
    """
    if len(sys.argv) < 2:
        logging.error("Too few arguments.  Specify date shot year")
        return

    # Get arguments
    args_year = sys.argv[1]

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

    google_images_with_arg_year = []
    google_images_by_datetime = {}
    google_images_with_missing_dateshot = []
    google_images_with_non_standandard_filename = []
    local_images_by_datetime = {}
    local_images_with_non_standandard_filename = []
    google_images_missing_locally = []
    google_images_missing_locally = []
    result = {
        'google_images_with_arg_year': google_images_with_arg_year,
        'google_images_by_datetime': google_images_by_datetime,
        'google_images_with_missing_dateshot': google_images_with_missing_dateshot,
        'google_images_with_non_standandard_filename': google_images_with_non_standandard_filename,
        'local_images_by_datetime': local_images_by_datetime,
        'local_images_with_non_standandard_filename': local_images_with_non_standandard_filename,
        'google_images_missing_locally': google_images_missing_locally,
        'google_images_missing_locally': google_images_missing_locally
    }

    for google_image_id, google_image in google_image_ids.items():
        mediaMetadata = google_image.get('mediaMetadata')
        if mediaMetadata is None:
            google_images_with_missing_dateshot.append(google_image)

        else:
            creationTime = mediaMetadata.get('creationTime')
            if creationTime is None:
                google_images_with_missing_dateshot.append(google_image)

            else:
                # Date shot is of the format "2021-02-15T20:29:52Z
                # Extract the year from it
                image_year = creationTime.split('-')[0]
                if image_year == args_year:
                    google_images_with_arg_year.append(google_image)

    # If the images does not have format YYYYMMDD_HHMMSS_...
    # then there is an issue
    for google_image in google_images_with_arg_year:
        filename = google_image.get('filename')
        splits = filename.split('_')
        if len(splits) < 3:
            google_images_with_non_standandard_filename.append(google_image)
        else:
            image_date = splits[0]
            image_time = splits[1]
            if len(image_date) < 8 or not image_date.isdecimal():
                google_images_with_non_standandard_filename.append(google_image)
            elif len(image_time) < 6 or not image_time.isdecimal():
                google_images_with_non_standandard_filename.append(google_image)
            else:
                image_datetime = image_date + '_' + image_time
                google_images_by_datetime[image_datetime] = {
                    'filename': google_image.get('filename'),
                    'productUrl': google_image.get('productUrl')
                }

    # now make a list of all the local images in the year specified
    # and add them to the local_images_by_dateshot.
    pattern = f"\\{args_year}\\"
    for local_album_idx, local_album in enumerate(local_albums):
        album_path = local_album.get('path')
        if pattern not in album_path:
            continue

        album_image_idxs = local_album.get('images')
        for album_image_idx in album_image_idxs:
            local_image = local_images[album_image_idx]
            local_image_name = local_image.get('name')
            splits = local_image_name.split('_')
            if len(splits) < 3:
                local_images_with_non_standandard_filename.append(local_image.get('path'))

        image_date = splits[0]
        image_time = splits[1]
        if len(image_date) < 8 or not image_date.isdecimal():
            local_images_with_non_standandard_filename.append(local_image.get('path'))
        elif len(image_time) < 6 or not image_time.isdecimal():
            local_images_with_non_standandard_filename.append(local_image.get('path'))
        else:
            image_datetime = image_date + '_' + image_time
            local_images_by_datetime[image_datetime] = {
                'filename': local_image.get('name'),
                'path': local_image.get('path')
            }


    # Now traverse through all the google images with date shot
    # and locate them in local images
    # If not found then error
    for datetime, google_image in google_images_by_datetime.items():
        local_image = local_images_by_datetime.get(datetime)
        if local_image is None:
            google_images_missing_locally.append(google_image)

    bn = os.path.basename(args_year)
    gphoto.save_to_file(result, f"can_google_images_be_deleted_by_year_{bn}.json")


if __name__ == '__main__':
  main()