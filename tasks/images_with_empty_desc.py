import context; context.set_context()
import os
from pathlib import Path
import logging
import sys

import util
import gphoto
from gphoto.local_library import LocalLibrary

class ImagesWithEmptyDesc(object):

    def find():
      """
      This method expects that the folder has been scanned and cached
      Reference: https://akrabat.com/setting-title-and-caption-with-exiftool/
      """

      # Scan all the images and load the metadata with just comments
      gphoto.init()
      LocalLibrary.cache_raw_library("p:\\pics")
      LocalLibrary.save_raw_library()