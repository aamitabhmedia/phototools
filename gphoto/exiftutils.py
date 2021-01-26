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
    def get_any_comment(comments):
        """
        We look for 4 tag names to return value.  If any
        tag returns the value then that is returned
        """
        if ExifUtils._TAGIPTCObjectName in comments:
            value = comments[ExifUtils._TAGIPTCObjectName]
            if value is not None:
                value = value.strip()
            if len(value) > 0:
                return value

        if ExifUtils._TAGIPTCObjectName in comments:
            value = comments[ExifUtils._TAGIPTCObjectName]
            if value is not None:
                value = value.strip()
            if len(value) > 0:
                return value

        if ExifUtils._TAGExifImageDescription in comments:
            value = comments[ExifUtils._TAGExifImageDescription]
            if value is not None:
                value = value.strip()
            if len(value) > 0:
                return value

        if ExifUtils._TAGXmpDescription in comments:
            value = comments[ExifUtils._TAGXmpDescription]
            if value is not None:
                value = value.strip()
            if len(value) > 0:
                return value

        return None
