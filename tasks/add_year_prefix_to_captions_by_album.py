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
from gphoto.imageutils import ImageUtils



# -----------------------------------------------------
# add_year_prefix
# -----------------------------------------------------
def add_year_prefix(et, album_path, test_only):

    # Load library
    LocalLibrary.load_raw_library()
    cache = LocalLibrary.cache_raw()
    albums = cache['albums']
    album_dict = cache['album_dict']
    images = cache['images']

    # Get the album matching the path
    album_idx = -1
    if album_path in album_dict:
        album_idx = album_dict[album_path]
    else:
        print(f"ERROR: Album not found li library '{album_path}'")
        return
    album = albums[album_idx]

    # Get the image index list of the album, loop through it
    album_image_idxs = album['images']
    for image_idx in album_image_idxs:
        image = images[image_idx]
        image_name = image['name']
        image_path = image['path']
        
        # Get the year from the image filename
        year = image_name[0:4]

        # Get existing image caption and check if it begins with a year
        image_ext = ImageUtils.get_file_extension(image_name)
        is_video = ImageUtils.is_ext_video(image_ext)
        caption = ImageUtils.get_caption(et, image_path, is_video)
        if caption is not None:
            caption = caption.strip()

        # If no caption then build the caption from album
        if caption is None or len(caption) <= 0:
            print(f"MissingCaption: '{image_path}'")
        
        # images has existing caption.  See if it begins with year
        else:
            caption_year = caption[0:4]
            if caption_year.isdecimal():
                print(f"ExistYear: '{caption}', '{image_path}'")
                continue
            else:
                new_caption = year + ' ' + caption
                print(f"NewCaption: '{new_caption}', '{image_path}'")

# -----------------------------------------------------
# main
# -----------------------------------------------------
def main():

    album_path = None
    if len(sys.argv) > 1:
        album_path = sys.argv[1]
    else:
        print("ERROR: Missing album path.  Aborting")
        return

    # May be -t option
    test_only = False
    if len(sys.argv) > 2 and sys.argv[2] == '-t':
        test_only = True

    print("--------------------------------------------")
    print(f"album_path: {album_path}")
    print(f"test_only: {test_only}")
    print("--------------------------------------------")

    start_time = datetime.now()

    file_filter_include = None
    file_filter_exclude = "PFILM"
    
    with exiftool.ExifTool() as et:
        add_year_prefix(et, album_path, test_only)
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

if __name__ == '__main__':
  main()