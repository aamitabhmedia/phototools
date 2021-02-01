"""
Notes:
    JPG:
        Capture NX2 UI:
            Description:
                IPTC:Caption-Abstract
                XMP:Description
            Tag (Object Name)
                IPTC:ObjectName
        Windows Folder UI:
            Title:
                IPTC:Caption-Abstract
                EXIF:ImageDescription
                XMP:Description
                    IPTC:Caption-Abstract   - NOT DELETED
            Subject:
                EXIF:ImageDescription
        Command Line:
            ALL Image Tags Set independently
            QuickTime:Title         > "Warning: Sorry, QuickTime:Title doesn't exist or isn't writable"
    
    NEF:
        Capture NX2 UI:
            Description:
                IPTC:Caption-Abstract
                XMP:Description
            Tag (Object Name)
                IPTC:ObjectName
        Windows Folder UI:          CANNOT EDIT
            Title:
            Subject:
        Command Line: ALL Set independently
            IPTC:ObjectName         > IPTC:ObjectName
            IPTC:Caption-Abstract   > IPTC:Caption-Abstract
            EXIF:ImageDescription   > EXIF:ImageDescription
            XMP:Description         > XMP:Description

    PNG:
        Capture NX2 UI:     CANNOT CHANGE
        Windows Folder UI:  DON'T SEE THE TAGS IN UI
        Command Line:       ALL Set independently - Same as NEF



"""
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



    _IMAGE_COMMENT_TAG_NAMES = [
        _TAGIPTCObjectName,
        _TAGIPTCCaptionAbstract,
        _TAGExifImageDescription,
        _TAGXmpDescription
    ]

    _VIDEO_COMMENT_TAG_NAMES = [
        _TAGQuickTimeTitle
    ]

    @staticmethod
    def get_comment(et, image_path, is_video):
        comments = None
        tag_names = ImageUtils._VIDEO_COMMENT_TAG_NAMES if is_video else ImageUtils._IMAGE_COMMENT_TAG_NAMES

        comments = et.get_tags(tag_names, image_path)
        if comments:
            return ImageUtils.get_any_comment(comments, is_video)

        return None

    @staticmethod
    def get_any_comment(comments, is_video):
        tag_names = ImageUtils._VIDEO_COMMENT_TAG_NAMES if is_video else ImageUtils._IMAGE_COMMENT_TAG_NAMES
        for tag in tag_names:
            if tag in comments:
                value = comments[tag]
                if value:
                    value = value.strip()
                    if len(value) > 0:
                        return value
        return None

    # @staticmethod
    # def get_any_comment(comments, is_video):
    #     """
    #     We look for 4 image tag names to return value.  If any
    #     tag returns the value then that is returned
    #     For video tags we look for quicktime value
    #     """
    #     if not is_video:
    #         if ImageUtils._TAGIPTCObjectName in comments:
    #             value = comments[ImageUtils._TAGIPTCObjectName]
    #             if value is not None:
    #                 value = value.strip()
    #             if len(value) > 0:
    #                 return value

    #         if ImageUtils._TAGIPTCCaptionAbstract in comments:
    #             value = comments[ImageUtils._TAGIPTCCaptionAbstract]
    #             if value is not None:
    #                 value = value.strip()
    #             if len(value) > 0:
    #                 return value

    #         if ImageUtils._TAGExifImageDescription in comments:
    #             value = comments[ImageUtils._TAGExifImageDescription]
    #             if value is not None:
    #                 value = value.strip()
    #             if len(value) > 0:
    #                 return value

    #         if ImageUtils._TAGXmpDescription in comments:
    #             value = comments[ImageUtils._TAGXmpDescription]
    #             if value is not None:
    #                 value = value.strip()
    #             if len(value) > 0:
    #                 return value
    #     else:
    #         if ImageUtils._TAGQuickTimeTitle in comments:
    #             value = comments[ImageUtils._TAGQuickTimeTitle]
    #             if value is not None:
    #                 value = value.strip()
    #             if len(value) > 0:
    #                 return value

    #     return None

    def get_file_extension(filename):
        file_ext = os.path.splitext(filename)[1]
        if file_ext:
            file_ext = file_ext.lower()
        return file_ext

    def is_ext_video(image_ext):
        return image_ext in core.VIDEO_EXTENSIONS
    
    def set_caption(et, image_path, caption, is_video):
        if not is_video:
            return subprocess.run(["exiftool",
                f"-{ImageUtils._TAGIPTCObjectName}={caption}",
                f"-{ImageUtils._TAGIPTCCaptionAbstract}={caption}",
                # f"-{ImageUtils._TAGExifImageDescription}={caption}",
                # f"-{ImageUtils._TAGXmpDescription}={caption}",
                "-overwrite_original",
                image_path])
        else:
            return subprocess.run(["exiftool",
                f"-{ImageUtils._TAGQuickTimeTitle}={caption}",
                "-overwrite_original",
                "-ext", "mov", "-ext", "mp4",
                image_path])
