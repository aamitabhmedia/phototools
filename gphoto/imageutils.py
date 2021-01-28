import os
from pathlib import Path
import logging
import json

import exiftool

import util
from util.appdata import AppData
from util.log_mgr import LogMgr
import gphoto

class ImageUtils(object):

    _TAGIPTCObjectName = "IPTC:ObjectName"
    _TAGIPTCCaptionAbstract = "IPTC:Caption-Abstract"
    _TAGExifImageDescription = "Exif:ImageDescription"
    _TAGXmpDescription = "Xmp:Description"


    _COMMENT_TAG_NAMES = [
        _TAGIPTCObjectName,
        _TAGIPTCCaptionAbstract,
        _TAGExifImageDescription,
        _TAGXmpDescription
    ]

    @staticmethod
    def get_any_comment(comments):
        """
        We look for 4 tag names to return value.  If any
        tag returns the value then that is returned
        """
        if ImageUtils._TAGIPTCObjectName in comments:
            value = comments[ImageUtils._TAGIPTCObjectName]
            if value is not None:
                value = value.strip()
            if len(value) > 0:
                return value

        if ImageUtils._TAGIPTCCaptionAbstract in comments:
            value = comments[ImageUtils._TAGIPTCCaptionAbstract]
            if value is not None:
                value = value.strip()
            if len(value) > 0:
                return value

        if ImageUtils._TAGExifImageDescription in comments:
            value = comments[ImageUtils._TAGExifImageDescription]
            if value is not None:
                value = value.strip()
            if len(value) > 0:
                return value

        if ImageUtils._TAGXmpDescription in comments:
            value = comments[ImageUtils._TAGXmpDescription]
            if value is not None:
                value = value.strip()
            if len(value) > 0:
                return value

        return None
