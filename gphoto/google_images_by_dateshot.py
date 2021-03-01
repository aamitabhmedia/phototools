"""
It is expected that Google library has been downloaded.
The cache has the syntax:
    {
        "year": {dictionary of months}
    }
Dict of months has the syntax
    {
        "month": {dict of days}
    }    
Dict of days has the syntax
    {
        "day": [list of images]
    }    
"""

import logging

import gphoto
from util.appdata import AppData
from util.log_mgr import LogMgr
from gphoto.google_library import GoogleLibrary
from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages

class GoogleImagesByDateShot:

    _CACHE_FILE_NAME = "google_images_by_dateshot.json"
    _cache = None

    # -----------------------------------------------------
    # Return local in-memory cache
    # -----------------------------------------------------
    @staticmethod
    def cache():
        return GoogleImagesByDateShot._cache

    # -----------------------------------------------------
    # Cache media items to in-memory buffer from google api
    # -----------------------------------------------------
    @staticmethod
    def cache_images():

        GoogleImagesByDateShot._cache = {}

        GoogleLibrary.load_library()

        image_list = GoogleImages._cache['list']

        for image_idx, image in enumerate(image_list):

            metadata = None
            if "mediaMetadata" in image:
                metadata = image["mediaMetadata"]
                if "creationTime" in metadata:
                    dateshot = metadata["creationTime"]

                    # split the date shot into year, month, day, hhmmss
                    # Google stores this in the format "2010-07-05T04:33:14Z"
                else:
                    print(f"NO DateShot: '{image["filename"]}")
                    continue
            else:
                print(f"NO Metadata: '{image["filename"]}")
                continue
