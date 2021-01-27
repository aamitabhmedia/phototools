import context; context.set_context()
import os
from pathlib import Path
import logging
import sys

import exiftool

import util
import gphoto
from gphoto.local_library import LocalLibrary

_IMAGE_PATTERN = "20201104_083022"
_IMAGE_PATTERN_LEN = len(_IMAGE_PATTERN)

def main():
    """
    Images should follow the format:
    YYYYMMMDD_HHmmSS....

    If it does not follow this format then that is and
    indication that the file name does not match date shot
    """
    LocalLibrary.load_raw_library()

    album_result = {}

    # Walk through each file, split its file name for
    # comparison, and get date shot metadata
    cache = LocalLibrary.cache_raw()
    images = cache['images']
    albums = cache['albums']


    with exiftool.ExifTool() as et:
        for image in images:
            image_name = image['name']
            image_path = image['path']

            # If image does not follow correct pattern
            # Then add it to album list
            mismatched = False
            mismatch_reason = None
            if len(image_name) < _IMAGE_PATTERN_LEN:
                mismatched = True
                mismatch_reason = "file_name_fmt"

            # if image date shot does not match images name
            # then add it to the mismatched list
            tag = None
            if not mismatched:
                tag = et.get_tag("Exif:DateTimeOriginal", image_path)
                if tag is None or len(tag) <= 0:
                    mismatched = True
                    mismatch_reason = "missing date shot '{tag}'"

            tagsplit = None
            if not mismatched:
                tagsplit = tag.split(' ')
                if len(tagsplit) < 2:
                    mismatched = True
                    mismatch_reason = "bad date shot '{tag}'"

            if not mismatched:
                filedatetime = image_name.split('_')
                file_date = filedatetime[0]
                file_time = filedatetime[1]

                tag_date = ''.join(tagsplit[0].split(':'))
                tag_time = ''.join(tagsplit[1].split(':'))

                if tag_date != file_date or tag_time != file_time:
                    mismatched = True
                    mismatch_reason = "mismatched tag '{tag}'"

            if mismatched:
                parent_index = image['parent']
                album = albums[parent_index]
                album_path = album['path']
                album_image_list = None
                if album_path not in album_result:
                    album_image_list = [image_path]
                    album_result[album_path] = album_image_list
                else:
                    album_image_list = album_result[album_path]
                    album_image_list.append(image_path)

    util.pprint(album_result)

if __name__ == '__main__':
  main()