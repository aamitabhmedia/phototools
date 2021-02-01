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

_ALBUM_PATTERN = "yyyy-mm-dd x"
_ALBUM_PATTERN_LEN = len(_ALBUM_PATTERN)

# -----------------------------------------------------
# Execute
# -----------------------------------------------------
def execute(et,
        album_path_filter,
        file_filter_include, file_filter_exclude,
        test_only):

    LocalLibrary.load_raw_library()

    album_path_filter_leaf = None
    if album_path_filter:
        album_path_filter_leaf = os.path.basename(album_path_filter)

    # The result is going to be of the form
    #     {
    #         "bad_albums": {
    #             "...album path...": None,
    #                 ...
    #         },
    #         "good_albums": {
    #             "album_path": {
    #                 "caption": "...caption from the album folder...",
    #                 "images": [list of images that need captioning]
    #             }    
    #         }
    #     }
    result = {
        "bad_albums": {},
        "good_albums": {}
    }
    bad_albums = result['bad_albums']
    good_albums = result['good_albums']

    # hold sections of cache as local variables
    cache = LocalLibrary.cache_raw()
    albums = cache['albums']
    album_dict = cache['album_dict']
    images = cache['images']
    image_dict = cache['image_dict']    


    # Loop through each album, get caption from it
    # if it follows standard naming convention
    for album in albums:

        # if folder is in the include list then continue
        # Otherwise ignore this album
        album_name = album['name']
        album_path = album['path']
        album_images = album['images']

        # filter out albums
        if album_path_filter and not album_path.startswith(album_path_filter):
            continue

        # Does album conform to correct format?
        #   yy-mm-dd ,,,description
        bad_album = False
        bad_album_reason = None
        if len(album_name) < _ALBUM_PATTERN_LEN:
            bad_album = True
            bad_album_reason = "short_len"
        
        # Get the album year and the description to build caption
        caption = None
        if not bad_album:
            caption_date_text_split = album_name.split(' ')
            if len(caption_date_text_split) < 2:
                bad_album = True
                bad_album_reason = "no_space"
            else:
                caption_date = caption_date_text_split[0]
                caption_text = ' '.join(caption_date_text_split[1:])

                # if date is not of the length yyyy-mm-dd then there is error
                if len(caption_date) != len("yyyy-mm-dd"):
                    bad_album = True
                    bad_album_reason = "bad_spacing"
                else:
                    caption_date_split = caption_date.split('-')
                    if len(caption_date_split) < 3:
                        bad_album = True
                        bad_album_reason = "date_fmt"
                    else:
                        # if date is not of the form yyyy-mm-dd then there is error
                        calculated_date = '-'.join(caption_date_split)
                        if len(calculated_date) != len("yyyy-mm-dd"):
                            bad_album = True
                            bad_album_reason = "short_date"
                        else:
                            album_year = caption_date_split[0]
                            caption = album_year + ' ' + caption_text

        if bad_album:
            bad_albums[album_path] = bad_album_reason
            continue

        # Loop through all the images in tis album
        for image_idx in album_images:
            image = images[image_idx]
            image_name = image['name']
            image_path = image['path']

            if file_filter_exclude and image_name.find(file_filter_exclude) > -1:
                continue
            if file_filter_include and image_path.find(file_filter_include) < 0:
                continue

            image_ext = ImageUtils.get_file_extension(image_name)
            is_video = ImageUtils.is_ext_video(image_ext)

            # Need to rerun local library caching
            if not os.path.exists(image_path):
                print("Local library not updated.  Please rerun download_local_library again")
                exit

            caption_missing = False

            # Check if caption is empty
            comments = et.get_tags(ImageUtils._COMMENT_TAG_NAMES, image_path)
            if comments is None:
                caption_missing = True
            else:
                comment = ImageUtils.get_any_comment(comments, is_video)
                if comment is None:
                    caption_missing = True

            if not caption_missing:
                continue

            # Caption missing.  Add it to the list of images to get album
            # name as caption
            good_images = None
            if album_path not in good_albums:
                good_images = [image_path]
                good_albums[album_path] = [caption, good_images]
            else:
                good_images = good_albums[album_path][1]
                good_images.append(image_path)

            # Update image caption now
            if not test_only:
                ImageUtils.set_caption(et, image_path, caption, is_video)

    saveto_filename = "fill_empty_image_caption_by_album_name"
    if album_path_filter_leaf:
        saveto_filename += '_d' + album_path_filter_leaf
    if file_filter_include is not None:
        saveto_filename += '_' + file_filter_include

    saveto_filename += '.json'
    saveto = os.path.join(gphoto.cache_dir(), saveto_filename)
    print(f"Saving to: '{saveto}'")

    with open(saveto, "w") as cache_file:
        json.dump(result, cache_file, indent=2)

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    start_time = datetime.now()

    album_path_filter = "p:\\pics\\2040"

    file_filter_include = None
    file_filter_exclude = "PFILM"
    
    with exiftool.ExifTool() as et:
        execute(et,
            album_path_filter,
            file_filter_include, file_filter_include, test_only=False
        )
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

# -----------------------------------------------------
# -----------------------------------------------------
if __name__ == '__main__':
  main()