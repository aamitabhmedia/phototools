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
def find(
    et,
    album_path_filter,
    file_filter_include, file_filter_exclude,
    test_missing_date_shot, test_bad_date_shot,
    test_filename_FMT,
    test_Tag_mismatch,
    test_missing_caption):
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
    print(f"-------------------- find --------------------------")
    print(f"album_path_filter = {album_path_filter}")
    print(f"file_filter_include = {file_filter_include}")
    print(f"file_filter_exclude = {file_filter_exclude}")
    print(f"test_missing_date_shot = {test_missing_date_shot}")
    print(f"test_bad_date_shot = {test_bad_date_shot}")
    print(f"test_filename_FMT = {test_filename_FMT}")
    print(f"test_Tag_mismatch = {test_Tag_mismatch}")
    print(f"test_missing_caption = {test_missing_caption}")
    print(f"----------------------------------------------------")

    LocalLibrary.load_library('raw')()

    result = {}

    album_path_filter_leaf = None
    if album_path_filter:
        album_path_filter_leaf = os.path.basename(album_path_filter)
    print(f"album_path_filter_leaf = {album_path_filter_leaf}")

    # Walk through each file, split its file name for
    # comparison, and get date shot metadata
    cache = LocalLibrary.cache_raw()
    images = cache['images']
    albums = cache['albums']

    for image in images:
        image_name = image['name']
        image_path = image['path']

        if file_filter_exclude and image_name.find(file_filter_exclude) > -1:
            continue
        if file_filter_include and image_path.find(file_filter_include) < 0:
            continue
        if album_path_filter and not image_path.startswith(album_path_filter):
            continue

        image_ext = ImageUtils.get_file_extension(image_name)
        is_video = ImageUtils.is_ext_video(image_ext)

        # Need to rerun local library caching
        if not os.path.exists(image_path):
            msg="Local library not updated.  Please rerun download_local_library again"
            print(msg)
            sys.exit(msg)

        # Nothing is mismatched yet
        mismatched = False
        mismatch_reason = None
        mismatch_desc = None

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
                        mismatch_reason = "missing-date-shot"

        tagsplit = None
        if test_missing_date_shot and test_bad_date_shot and not mismatched:
            tagsplit = tag.split(' ')
            if len(tagsplit) < 2:
                mismatched = True
                mismatch_reason = f"bad-date-shot"
                mismatch_desc = tag

        # If image does not follow correct pattern
        # Then add it to album list
        if test_filename_FMT:
            if len(image_name) < _IMAGE_PATTERN_LEN:
                mismatched = True
                mismatch_reason = "filename-FMT"

        filedatetime = None
        if test_filename_FMT and not mismatched:
            filedatetime = image_name.split('_')
            if len(filedatetime) < 2:
                mismatched = True
                mismatch_reason = "filename-FMT"

        if test_Tag_mismatch and not mismatched:
            file_date = filedatetime[0]
            file_time = filedatetime[1][0:3]
            tag_date = ''.join(tagsplit[0].split(':'))
            tag_time = ''.join(tagsplit[1].split(':'))[0:3]

            if tag_date != file_date or tag_time != file_time:
                mismatched = True
                mismatch_reason = f"tag-mismatch"
                mismatch_desc = tag

        # Check missing Caption: check if any of the tags have any value
        if test_missing_caption and not mismatched:
            comments = et.get_tags(ImageUtils._IMAGE_COMMENT_TAG_NAMES, image_path)
            if comments is None or len(comments) <= 0:
                mismatched = True
                mismatch_reason = f"missing-caption"
            else:
                comment = ImageUtils.get_any_caption(comments, is_video)
                if comment is None:
                    mismatched = True
                    mismatch_reason = f"missing-caption"

        # result structure
        # {
        #     "album_path": {
        #         "reason value": [list of image paths],
        #                ...
        #     },
        #         ...
        # }
        if mismatched:
            parent_index = image['parent']
            album = albums[parent_index]
            album_path = album['path']

            print(f"{album['name']}, {mismatch_reason}, {image_path}")

            mismatched_result = None
            if album_path not in result:
                mismatched_result = {}
                result[album_path] = mismatched_result
            else:
                mismatched_result = result[album_path]

            reason_result = None
            if mismatch_reason not in mismatched_result:
                reason_result = []
                mismatched_result[mismatch_reason] = reason_result
            else:
                reason_result = mismatched_result[mismatch_reason]

            image_result = image_path
            if mismatch_desc is not None:
                image_result = [mismatch_desc, image_path]

            reason_result.append(image_result)

    # The format is:
    #     result2 = {
    #         "reason": [
    #             {
    #                 "album_path": <...path...>,
    #                 "images": [list of images]
    #             },
    #                 ...
    #         ]
    #     }
    result2 = {}
    for album_path in result:
        reasons_set = result[album_path]
        for reason in reasons_set:
            image_list = reasons_set[reason]

            album_set = None
            if reason not in result2:
                album_set = {}
                result2[reason] = album_set
            else:
                album_set = result2[reason]

            album_set[album_path] = image_list

    saveto_filename = "check_album_readiness"
    if album_path_filter_leaf:
        saveto_filename += '_d' + album_path_filter_leaf
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

    saveto_filename += '.json'
    saveto = os.path.join(gphoto.cache_dir(), saveto_filename)
    print(f"Saving to: '{saveto}'")

    with open(saveto, "w") as cache_file:
        json.dump(result2, cache_file, indent=2)

# -----------------------------------------------------
# TODO: how to run all test.  right now the algorithm
# ignore subsequent tests if previous was satisfied
# Also mismatched_desc is only for date mismatch
# -----------------------------------------------------
def main():

    album_path_filter = "p:\\pics\\2012"

    if len(sys.argv) > 1:
        album_path_filter = sys.argv[1]

    print("--------------------------------------------")
    print(f"filter: {album_path_filter}")
    print("--------------------------------------------")

    start_time = datetime.now()

    file_filter_include = None
    file_filter_exclude = "PFILM"
    
    with exiftool.ExifTool() as et:
        find(et,
            album_path_filter,
            file_filter_include, file_filter_exclude,
            test_missing_date_shot=True, test_bad_date_shot=True,
            test_filename_FMT=True, test_Tag_mismatch=True,
            test_missing_caption=True
        )
    
    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

if __name__ == '__main__':
  main()