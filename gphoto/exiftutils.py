import os
from pathlib import Path
import logging
import json

import exiftool

import util
from util.appdata import AppData
from util.log_mgr import LogMgr
import gphoto

class ExifUtils(object):

    _TAGIPTCObjectName = "IPTC:ObjectName"
    _TAGIPTCCaptionAbstract = "IPTC:Caption-Abstract"
    _TAGExifImageDescription = "Exif:ImageDescription"
    _TAGXmpDescription = "Xmp:Description"

    _COMMENT_TAG_NAMES = [
            ExifUtils._TAGIPTCObjectName,
            ExifUtils._TAGIPTCCaptionAbstract,
            ExifUtils._TAGExifImageDescription,
            ExifUtils._TAGXmpDescription
        ]

    @staticmethod
    def get_metadata(filename, tag_names):
        """
        Returns a list object with metadata values fillder in

            filename: Name of the image file
            tag_names: list of tag names
        """
        with exiftool.ExifTool() as et:
            return et.get_tags(tag_names, filename)

    @staticmethod
    def get_file_comments(filename):
        with exiftool.ExifTool() as et:
            return et.get_tags(ExifUtils._COMMENT_TAG_NAMES, filename)

    @staticmethod
    def get_files_comments(filenames):
        with exiftool.ExifTool() as et:
            return et.get_tags_batch(ExifUtils._COMMENT_TAG_NAMES, filenames)

