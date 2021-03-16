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

_IMAGE_PATTERN = "20201104_083022"
_IMAGE_PATTERN_LEN = len(_IMAGE_PATTERN)

# -----------------------------------------------------
# -----------------------------------------------------
def check_album_readiness(
    et,
    album_path_filter_year,
    file_filter_include, file_filter_exclude,
    test_missing_date_shot, test_bad_date_shot,
    test_filename_FMT,
    test_Tag_mismatch,
    test_missing_caption,
    test_unique_caption,
    test_missing_caption_year,
    test_missing_geotags):
    """
    Images should follow the format:
    YYYYMMMDD_HHmmSS....

    If it does not follow this format then that is and
    indication that the file name does not match date shot

    The result is of the form
    {
        "album_path": {
            "reason value": [list of image paths],
                ...
        },
            ...
    }
    """
    print(f"-------------------- args --------------------------")
    print(f"album_path_filter_pattern = {album_path_filter_year}")
    print(f"file_filter_include = {file_filter_include}")
    print(f"file_filter_exclude = {file_filter_exclude}")
    print(f"test_missing_date_shot = {test_missing_date_shot}")
    print(f"test_bad_date_shot = {test_bad_date_shot}")
    print(f"test_filename_FMT = {test_filename_FMT}")
    print(f"test_Tag_mismatch = {test_Tag_mismatch}")
    print(f"test_missing_caption = {test_missing_caption}")
    print(f"test_unique_caption = {test_unique_caption}")
    print(f"test_missing_caption_year = {test_missing_caption_year}")
    print(f"test_missing_geotags = {test_missing_geotags}")
    print(f"----------------------------------------------------")

    unique_caption_reason = "non-unique-captions"
    mismatch_album_image_caption_reason = "mismatch-album-image-captions"
    missing_geotags_reason = "missing-geotags"

    LocalLibrary.load_library('raw')

    result = {}

    album_path_filter_pattern = f"\\{album_path_filter_year}\\"
    print(f"album_path_filter_pattern = {album_path_filter_pattern}")

    # Walk through each file, split its file name for
    # comparison, and get date shot metadata
    cache = LocalLibrary.cache_raw()
    images = cache['images']
    albums = cache['albums']

    for album in albums:

        album_name = album['name']
        album_path = album['path']

        if album_path_filter_pattern and album_path.find(album_path_filter_pattern) < 0:
            continue

        # Album level results captured here
        # Duplicate captions table.  Every caption of images
        # is hashed here
        unique_caption_dict = {}

        album_images = album['images']
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
                msg="Local library not updated.  Please rerun download_local_library again"
                print(msg)
                sys.exit(msg)

            # Nothing is mismatched yet
            # Each test returns a result as tuple with 3 values:
            #   ("name of the test", True|False if test failed, "extra info")
            mismatched = False
            test_results = []

            # if image date shot does not match images name
            # then add it to the mismatched list.  For PNG use PNG:CreationTime
            tag = None
            if test_missing_date_shot:
                tag = et.get_tag("Exif:DateTimeOriginal", image_path)
                if tag is None or len(tag) <= 0:
                    tag = et.get_tag("Exif:CreateDate", image_path)
                    if tag is None or len(tag) <= 0:
                        tag = et.get_tag("QuickTime:CreateDate", image_path)
                        if tag is None or len(tag) <= 0:
                            mismatched = True
                            test_results.append("missing-date-shot")

            tagsplit = None
            if test_missing_date_shot and test_bad_date_shot and not mismatched:
                tagsplit = tag.split(' ')
                if len(tagsplit) < 2:
                    mismatched = True
                    test_results.append(("bad-date-shot", tag))

            # If image does not follow correct pattern
            # Then add it to album list
            mismatched_filename_format = False
            if test_filename_FMT:
                if len(image_name) < _IMAGE_PATTERN_LEN:
                    mismatched = True
                    test_results.append("filename-FMT")

            filedatetime = None
            if test_filename_FMT and not mismatched_filename_format:
                filedatetime = image_name.split('_')
                if len(filedatetime) < 2:
                    mismatched = True
                    test_results.append("filename-FMT")

            if test_Tag_mismatch and not mismatched_filename_format:
                file_date = filedatetime[0]
                file_time = filedatetime[1][0:3]
                tag_date = ''.join(tagsplit[0].split(':'))
                tag_time = ''.join(tagsplit[1].split(':'))[0:3]

                if tag_date != file_date or tag_time != file_time:
                    mismatched = True
                    test_results.append(("tag-mismatch", tag))

            # Check missing Caption: check if any of the tags have any value
            caption = None
            if test_missing_caption:
                caption = ImageUtils.get_caption(et, image_path, is_video)
                if caption is None or len(caption) <= 0:
                    mismatched = True
                    test_results.append("missing-caption")
                elif test_unique_caption:
                    year = None
                    if len(caption) > 4:
                        year = caption[0:4]
                        if not year.isdecimal():
                            unique_caption_dict[caption] = None

            # Check missing Caption year
            if test_missing_caption_year and caption is not None:
                if not test_missing_caption:
                    caption = ImageUtils.get_caption(et, image_path, is_video)
                if not test_missing_caption and (caption is None or len(caption) <= 0):
                    mismatched = True
                    test_results.append("missing-caption")
                elif not test_missing_caption and len(caption) < 5:
                    mismatched = True
                    test_results.append("missing-caption")
                else:
                    caption_year = caption[0:4]
                    if not caption_year.isdecimal():
                        mismatched = True
                        test_results.append(("missing-caption-year", caption))

            # Test missing geotags
            if test_missing_geotags and not is_video:
                geotags = None
                try:
                    geotags = et.get_tags(["GPSLatitude", "GPSLongitude", "GPSLatitudeRef", "GPSLongitudeRef"], image_path)
                except Exception as e:
                    geotags = None
                
                if geotags is None or len(geotags) < 4:
                    mismatched = True
                    test_results.append(missing_geotags_reason)

            if mismatched:
                for test_result in test_results:
                    mismatch_reason = None
                    mismatch_desc = None
                    if type(test_result) is not tuple: 
                        mismatch_reason = test_result
                    else:
                        mismatch_reason = test_result[0]
                        mismatch_desc = test_result[1]

                    reason_result = None
                    if mismatch_reason not in result:
                        reason_result = {}
                        result[mismatch_reason] = reason_result
                    else:
                        reason_result = result[mismatch_reason]

                    album_result = None
                    if album_path not in reason_result:
                        album_result = []
                        reason_result[album_path] = album_result
                    else:
                        album_result = reason_result[album_path]

                    if type(test_result) is not tuple:
                        album_result.append(image_path)
                    else:
                        album_result.append((mismatch_desc, image_path))

        # add duplicate caption results
        if len(unique_caption_dict) > 1:
            unique_caption_result = None
            if unique_caption_reason not in result:
                unique_caption_result = {}
                result[unique_caption_reason] = unique_caption_result
            else:
                unique_caption_result = result[unique_caption_reason]

            unique_caption_result[album_path] = list(unique_caption_dict.keys())

        # If caption is same for all images but diff from album then report it
        if len(unique_caption_dict) > 0 and len(unique_caption_dict) < 2:
            image_caption = str(next(iter(unique_caption_dict)))
            
            # Strip the month and day from the album name
            splits = album_name.split(' ')
            album_date = splits[0]
            album_desc = splits[1:]
            album_year = album_date[0:4]
            album_caption = album_year + ' ' + ' '.join(album_desc)

            if album_caption != image_caption:
                mismatch_album_image_caption_result = None
                if mismatch_album_image_caption_reason not in result:
                    mismatch_album_image_caption_result = {}
                    result[mismatch_album_image_caption_reason] = mismatch_album_image_caption_result
                else:
                    mismatch_album_image_caption_result = result[mismatch_album_image_caption_reason]
                
                mismatch_album_image_caption_result[album_path] = {
                    'album_caption': album_caption,
                    'image_caption': image_caption
                }


    saveto_filename = "check_album_readiness"
    if album_path_filter_year:
        saveto_filename += '_d' + album_path_filter_year
    if file_filter_include is not None:
        saveto_filename += '_' + file_filter_include

    if test_missing_date_shot or test_bad_date_shot:
        saveto_filename += "_dtshot"
    if test_filename_FMT:
        saveto_filename += "_ffmt"
    if test_Tag_mismatch:
        saveto_filename += "_Tagmm"
    if test_missing_caption:
        saveto_filename += "_miscap"
    if test_unique_caption:
        saveto_filename += "_dupcap"

    saveto_filename += '.json'
    saveto = os.path.join(gphoto.cache_dir(), saveto_filename)
    print(f"Saving to: '{saveto}'")

    with open(saveto, "w") as cache_file:
        json.dump(result, cache_file, indent=2)

# -----------------------------------------------------
# TODO: how to run all test.  right now the algorithm
# ignore subsequent tests if previous was satisfied
# Also mismatched_desc is only for date mismatch
# -----------------------------------------------------
def main():

    gphoto.init()

    if len(sys.argv) < 2:
        print("Album pattern not provided.")
        return

    album_path_filter_year = sys.argv[1]

    print("--------------------------------------------")
    print(f"filter: {album_path_filter_year}")
    print("--------------------------------------------")

    start_time = datetime.now()

    file_filter_include = None
    file_filter_exclude = "PFILM"
    test_missing_date_shot = True
    test_bad_date_shot = True
    test_filename_FMT = True
    test_Tag_mismatch = True
    test_missing_caption = True
    test_unique_caption = True
    test_missing_caption_year = True
    test_missing_geotags = True
    
    with exiftool.ExifTool() as et:
        check_album_readiness(et,
            album_path_filter_year,
            file_filter_include,
            file_filter_exclude,
            test_missing_date_shot,
            test_bad_date_shot,
            test_filename_FMT,
            test_Tag_mismatch,
            test_missing_caption,
            test_unique_caption,
            test_missing_caption_year,
            test_missing_geotags
        )
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

if __name__ == '__main__':
  main()