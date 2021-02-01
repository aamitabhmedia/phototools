import os
from pathlib import Path
import logging
import json
import subprocess

import exiftool

import util
from util.appdata import AppData
from util.log_mgr import LogMgr
from gphoto import core

class ImageUtils(object):

    _TAGIPTCObjectName = "IPTC:ObjectName"
    _TAGIPTCCaptionAbstract = "IPTC:Caption-Abstract"
    _TAGExifImageDescription = "Exif:ImageDescription"
    _TAGXmpDescription = "Xmp:Description"
    _TAGQuickTimeTitle = "QuickTime:Title"


    _COMMENT_TAG_NAMES = [
        _TAGIPTCObjectName,
        _TAGIPTCCaptionAbstract,
        _TAGExifImageDescription,
        _TAGXmpDescription,
        _TAGQuickTimeTitle
    ]

    @staticmethod
    def get_any_comment(comments, is_video):
        """
        We look for 4 image tag names to return value.  If any
        tag returns the value then that is returned
        For video tags we look for quicktime value
        """
        if not is_video:
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
        else:
            if ImageUtils._TAGQuickTimeTitle in comments:
                value = comments[ImageUtils._TAGQuickTimeTitle]
                if value is not None:
                    value = value.strip()
                if len(value) > 0:
                    return value

        return None

    def get_file_extension(filename):
        file_ext = os.path.splitext(filename)[1]
        if file_ext:
            file_ext = file_ext.lower()
        return file_ext

    def is_ext_video(image_ext):
        return image_ext in core.VIDEO_EXTENSIONS
    
    def set_caption(et, image_path, caption, is_video):
        if not is_video:
            return subprocess.run("exiftool",
                f"-{_TAGIPTCObjectName}={caption}",
                f"-{_TAGIPTCCaptionAbstract}={caption}",
                f"-{_TAGExifImageDescription}={caption}",
                f"-{_TAGXmpDescription}={caption}",
                "-overwrite_original",
                image_path)
        else:
                f"-{_TAGQuickTimeTitle}={caption}",
                "-overwrite_original",
                image_path)
