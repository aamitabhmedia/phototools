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

    _comment_tag_names = [
            "IPTC:ObjectName",
            "IPTC:Caption-Abstract",
            "Exif:ImageDescription",
            "Xmp:Description"
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
    def get_comments(filename):
        return ExifUtils.get_metadata(filename, ExifUtils._comment_tag_names)
