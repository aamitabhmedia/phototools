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
            Description             > XMP:Description (Populates the description in Capture NX UI)
            Title                   > XMP:Title (Populates IPTC Object Name in Capture NX UI)
            Subject                 > XMP:Subject
            IPTC:ObjectName         > IPTC:ObjectName
            IPTC:Caption-Abstract   > IPTC:Caption-Abstract
            EXIF:ImageDescription   > EXIF:ImageDescription
            XMP:Description         > XMP:Description   (Redundant, same as -Description)

    PNG:
        Capture NX2 UI:     CANNOT CHANGE
        Windows Folder UI:  DON'T SEE THE TAGS IN UI
        Command Line:       ALL Set independently - Same as NEF

    MOV:
        ffmpeg can help: https://stackoverflow.com/questions/24637282/update-value-of-rotation-in-mov-file-using-exiftool

        Capture NX2 UI: MOV DOES NOT SHOW UP

        Windows Folder UI:
            QuickTime:Title     > XMP:Description
                                > QuickTime:Title
            QuickTime:Subtitle  > QuickTime:Subtitle

        Command Line:
            Description         > XMP:Description
            Title               > XMP:Title
            Subject             > XMP:Subject
            3 Image tags do nothing
            QuickTime:Title     > XMP:Description
                                > QuickTime:Title (FAILED for SOME REASON)
            XMP:Description     > XMP:Description (But can't see on Windows UI)
            XMP:Title           > XMP:Title


"""
import os
from os.path import split
from pathlib import Path
import logging
import json
import subprocess

import exiftool

import util
from util.appdata import AppData
from util.log_mgr import LogMgr
from gphoto import core

# ------------------------------------------
# class ImageUtils
# ------------------------------------------
class ImageUtils(object):

    _TagDescription = "Description"
    _TagTitle = "Title"
    _TagSubject = "Subject"
    _TagIPTCHeadline = "IPTC:Headline"

    _TagIPTCCaptionAbstract = "IPTC:Caption-Abstract"
    _TagIPTCObjectName = "IPTC:ObjectName"

    _TagExifImageDescription = "Exif:ImageDescription"

    _TagXMPDescription = "XMP:Description"
    _TagXMPTitle = "XMP:Title"
    _TagXMPSubject = "XMP:Subject"

    _TagQuickTimeTitle = "QuickTime:Title"
    _TagQuicktimeSubtitle = "Quicktime:Subtitle"

    _IMAGE_COMMENT_TAG_NAMES = [
        _TagDescription,
        _TagTitle,
        _TagSubject,
        _TagIPTCHeadline,
        _TagIPTCCaptionAbstract,
        _TagIPTCObjectName,
        _TagExifImageDescription,
        _TagXMPDescription,
        _TagXMPTitle,
        _TagXMPSubject
    ]

    _VIDEO_COMMENT_TAG_NAMES = [
        _TagDescription,
        _TagTitle,
        _TagSubject,
        _TagXMPDescription,
        _TagQuickTimeTitle,
        _TagQuicktimeSubtitle,
        _TagXMPDescription,
        _TagXMPTitle,
        _TagXMPSubject
    ]

    # ------------------------------------------
    # ------------------------------------------
    def get_file_extension(filename):
        file_ext = os.path.splitext(filename)[1]
        if file_ext:
            file_ext = file_ext.lower()
        return file_ext

    # ------------------------------------------
    # ------------------------------------------
    def is_ext_video(image_ext):
        return image_ext in core.VIDEO_EXTENSIONS
    
    # ------------------------------------------
    # ------------------------------------------
    def is_ext_image(image_ext):
        return not ImageUtils.is_ext_video(image_ext)
    
    # ------------------------------------------
    # ------------------------------------------
    @staticmethod
    def get_date_shot(et, image_path, is_video):
        tag = None
        if is_video:
            tag = et.get_tag("QuickTime:CreateDate", image_path)
            if tag is None or len(tag) <= 0:
                tag = et.get_tag("Exif:CreateDate", image_path)
        else:
            tag = et.get_tag("Exif:DateTimeOriginal", image_path)
        return tag

    # ------------------------------------------
    # ------------------------------------------
    @staticmethod
    def get_caption(et, image_path, is_video):
        comments = None
        tag_names = ImageUtils._VIDEO_COMMENT_TAG_NAMES if is_video else ImageUtils._IMAGE_COMMENT_TAG_NAMES

        comments = et.get_tags(tag_names, image_path)
        if comments:
            return ImageUtils.get_any_caption(comments, is_video)

        return None

    # ------------------------------------------
    # ------------------------------------------
    @staticmethod
    def get_any_caption(comments, is_video):
        tag_names = ImageUtils._VIDEO_COMMENT_TAG_NAMES if is_video else ImageUtils._IMAGE_COMMENT_TAG_NAMES
        for tag in tag_names:
            if tag in comments:
                value = comments[tag]
                if value:
                    value = value.strip()
                    if len(value) > 0:
                        return value
        return None

    # ------------------------------------------
    # ------------------------------------------
    def set_caption(et, image_path, caption, is_video):
        if not is_video:
            return subprocess.run(["exiftool",
                f"-{ImageUtils._TagDescription}={caption}",
                f"-{ImageUtils._TagTitle}={caption}",
                f"-{ImageUtils._TagSubject}={caption}",
                f"-{ImageUtils._TagIPTCHeadline}={caption}",
                f"-{ImageUtils._TagExifImageDescription}={caption}",
                f"-{ImageUtils._TagIPTCCaptionAbstract}={caption}",
                f"-{ImageUtils._TagIPTCObjectName}={caption}",
                # f"-{ImageUtils._TagExifImageDescription}={caption}",
                # f"-{ImageUtils._TagXMPDescription}={caption}",
                "-overwrite_original",
                image_path])
        else:
            return subprocess.run(["exiftool",
                f"-{ImageUtils._TagQuickTimeTitle}={caption}",
                "-overwrite_original",
                "-ext", "mov", "-ext", "mp4",
                image_path])

    # ------------------------------------------
    # ------------------------------------------
    def split_caption_desc(caption):
        """
        Caption should follow the following syntax:
            YYYY-MM-DD <description>

        This function will return a tuple of year, month, day, and description
        If the syntax is not followed then return None tuple
        """

        splits = caption.split(' ')
        dt = splits[0]

        dt_splits = dt.split('-')
        year = dt_splits[0]
        month = dt_splits[1]
        day = dt_splits[2]

        if len(dt) != 10:
            return None
        desc = ' '.join(splits[1:])

        return year, month, day, desc
