import context; context.set_context()
import os
from pathlib import Path
import logging
import sys
import json

import exiftool

import util
import gphoto
from gphoto.local_library import LocalLibrary

_IMAGE_PATTERN = "20201104_083022"
_IMAGE_PATTERN_LEN = len(_IMAGE_PATTERN)

def main_with_exiftool(et, file_filter_pattern):
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
    LocalLibrary.load_raw_library()

    result = {}

    # Walk through each file, split its file name for
    # comparison, and get date shot metadata
    cache = LocalLibrary.cache_raw()
    images = cache['images']
    albums = cache['albums']

    for image in images:
        image_name = image['name']
        image_path = image['path']

        # TODO:
        # If file has PFILM pattern then it is the negatives
        # that are scanned.  For now ignore them
        if image_name.find("PFILM") > -1:
            continue

        # if filter is specified then apply it to the file name
        if file_filter_pattern and image_path.find(file_filter_pattern) < 0:
            continue

        if not os.path.exists(image_path):
            continue

        # If image does not follow correct pattern
        # Then add it to album list
        mismatched = False
        mismatch_reason = None
        mismatch_desc = None
        if len(image_name) < _IMAGE_PATTERN_LEN:
            mismatched = True
            mismatch_reason = "file_name_fmt"

        # if image date shot does not match images name
        # then add it to the mismatched list.  For PNG use PNG:CreationTime
        tag = None
        if not mismatched:
            tag = et.get_tag("Exif:DateTimeOriginal", image_path)
            if tag is None or len(tag) <= 0:
                tag = et.get_tag("Exif:CreateDate", image_path)
                if tag is None or len(tag) <= 0:
                    mismatched = True
                    mismatch_reason = "missing date shot"

        tagsplit = None
        if not mismatched:
            tagsplit = tag.split(' ')
            if len(tagsplit) < 2:
                mismatched = True
                mismatch_reason = f"bad date shot"
                mismatch_desc = tag

        filedatetime = None
        if not mismatched:
            filedatetime = image_name.split('_')
            if len(filedatetime) < 2:
                mismatched = True
                mismatch_reason = "Filename FMT"

        if not mismatched:
            file_date = filedatetime[0]
            file_time = filedatetime[1][0:3]
            tag_date = ''.join(tagsplit[0].split(':'))
            tag_time = ''.join(tagsplit[1].split(':'))[0:3]

            if tag_date != file_date or tag_time != file_time:
                mismatched = True
                mismatch_reason = f"mismatched tag"
                mismatch_desc = tag

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

    saveto_filename = "image_dateshot_and_name_mismatched"
    if file_filter_pattern is not None:
        saveto_filename += '_' + file_filter_pattern
    saveto_filename += '.json'
    saveto = os.path.join(gphoto.cache_dir(), saveto_filename)
    print(f"Saving to: '{saveto}'")

    with open(saveto, "w") as cache_file:
        json.dump(result, cache_file, indent=2)

def main():
    file_filter_pattern = None
    with exiftool.ExifTool() as et:
        main_with_exiftool(et, file_filter_pattern)

if __name__ == '__main__':
  main()