import context; context.set_context()

import os
import sys
import logging

import util
import gphoto
from gphoto.local_library_metadata import LocalLibraryMetadata
from gphoto.google_library import GoogleLibrary
from gphoto.imageutils import ImageUtils


# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():

    if len(sys.argv) < 2:
        logging.error("Too few arguments.  Specify year")
        return

    # Get arguments
    arg_year = sys.argv[1]

    local_models = {}
    google_models = {}
    result = {
        'local_models': local_models,
        'google_models': google_models
    }

    GoogleLibrary.load_library()
    google_cache = GoogleLibrary.cache()
    google_image_ids = google_cache['image_ids']

    # Loop through google images
    for google_image_id, google_image in google_image_ids.items():

        mediaMetadata = google_image.get('mediaMetadata')
        if mediaMetadata is None:
            continue

        creationTime = mediaMetadata.get('creationTime')
        image_year = creationTime.split('-')[0]
        if image_year != arg_year:
            continue

        photo = mediaMetadata.get('photo')
        if photo is None:
            continue

        cameraMake = photo.get('cameraMake')
        cameraModel = photo.get('cameraModel')

        if cameraMake is None and cameraModel is None:
            continue

        makemodel = cameraMake + ':' + cameraModel
        google_models[makemodel] = None

    # Scan local library metadata
    LocalLibraryMetadata.load_library_metadata('raw')
    library_metadata_cache = LocalLibraryMetadata.cache('raw')

    for image_path, image_metadata in library_metadata_cache.items():

        dateTimeOriginal = image_metadata.get('DateTimeOriginal')
        if dateTimeOriginal is None:
            continue

        image_year = dateTimeOriginal.split(':')[0]
        if image_year != arg_year:
            continue

        model = image_metadata.get('Model')
        if model is None:
            continue

        local_models[model] = None

    # Save results
    bn = os.path.basename(arg_year)
    gphoto.save_to_file(result, f"camera_models_in_year_{bn}.json")


if __name__ == '__main__':
  main()