import context; context.set_context()

import os
from pathlib import Path
import logging
import sys
import json

from datetime import datetime

import exiftool

import util
import gphoto
from gphoto.local_library import LocalLibrary
from gphoto.google_library import GoogleLibrary
from gphoto.google_images import GoogleImages
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# do_work
# -----------------------------------------------------
def do_work(et, google_image_filter, album_folder_path, list_only):

    # Find folder album in the database
    LocalLibrary.load_raw_library()
    local_library_cache = LocalLibrary.cache_raw()
    images = local_library_cache['images']
    albums = local_library_cache['albums']
    album_ids = local_library_cache['album_ids']

    album_idx = album_ids[album_folder_path]
    album = albums[album_idx]
    local_album_path = album['path']

    print(f"[INFO]: Found album '{local_album_path}'")

    # Collect list of local album files
    local_files_results = []
    local_album_images = album['images']
    for image_idx in local_album_images:
        image = images[image_idx]
        image_name = image['name']
        image_path = image['path']
        local_files_results.append(image_path)

    sorted(local_files_results)
    util.pprint(local_files_results)
    print(f"[INFO] Local files count '{len(local_files_results)}'")

    # Collect a list of images from google photos
    # Each element in this list will be an object:
    #     {'path': 'image path', 'caption': 'images caption...'}
    google_images_results = []
    gphoto.init()
    GoogleImages.load_images()
    google_image_cache = GoogleImages.cache()
    google_images = google_image_cache['list']
    for google_image in google_images:
        image_name = google_image['filename']
        if image_name.find(google_image_filter) < 0:
            continue
        image_desc = google_image['description']

        google_images_results.append(
            (image_name, image_desc)
        )

    google_images_results = sorted(google_images_results, key=lambda record: record[0])
    util.pprint(google_images_results)
    print(f"[INFO] Google files count '{len(google_images_results)}'")

    # Perform basic validations
    # If counts are not the same then error out
    if len(local_files_results) != len(google_images_results):
        print(f"[ERROR]: Count mismatch local: '{len(local_files_results)}', google: '{len(google_images_results)}'.  Aborting")

    # Now loop through the list of folder images, get its
    # equivalent caption from the corresponding google image
    if list_only:
        return

    for image_idx, local_image_path in enumerate(local_files_results):
        desc = google_images_results[image_idx][1]

        # Get image extension and identify it as an image or video
        image_name = os.path.basename(local_image_path)
        image_ext = ImageUtils.get_file_extension(image_name)
        is_video = ImageUtils.is_ext_video(image_ext)

        # Set the caption now
        ImageUtils.set_caption(et, local_image_path, desc, is_video)


# -----------------------------------------------------
# main
# -----------------------------------------------------
def main():

    google_image_filter = "_ORKH"
    album_folder_path = "p:\\pics\\2010\\2010-07-02 Oregon Trip with Khadloyas"
    list_only = False

    print("--------------------------------------------")
    print(f"filter: {google_image_filter}")
    print(f"folder: {album_folder_path}")
    print("--------------------------------------------")

    start_time = datetime.now()
    
    with exiftool.ExifTool() as et:
        do_work(et, google_image_filter, album_folder_path, list_only)
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

if __name__ == '__main__':
  main()