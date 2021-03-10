import context; context.set_context()
import os
import sys
from pathlib import Path
import logging
import sys
import json

import gphoto
from googleapi.google_service import GoogleService
from googleapi.album_api import AlbumAPI
from gphoto.local_library import LocalLibrary

# ---------------------------------------------------------
# Uploader class has methods to upload local albums
# and its images
# ---------------------------------------------------------
class Uploader:

    # -------------------------------------
    # Upload album for a given folder name
    # -------------------------------------
    @staticmethod
    def upload_album(service, local_album):

        logging.info("------------------------------------------------------------------")
        logging.info(f"  album: '{local_album['path']}'")
        logging.info("------------------------------------------------------------------")

        # Create the album and make it sharable
        # --------------------------------------
        google_album = None
        share_info = None
        try:
            google_album = AlbumAPI.create_album(service, local_album['name'])
            share_info = AlbumAPI.make_album_sharable(service, google_album['id'], share=True)
        except Exception as e:
            raise

        google_album_id = google_album['id']

        # Loop through all images under the album and upload them
        # --------------------------------------------------------
        local_album_image_idxs = local_album['images']

        local_library_cache = LocalLibrary.cache_jpg()
        local_images = local_library_cache['images']

        for local_image_idx in local_album_image_idxs:

            local_image = local_images[local_image_idx]
            local_image_name = local_image['name']
            local_image_path = local_image['path']

    # -------------------------------------
    # Upload album for a given folder name
    # -------------------------------------
    @staticmethod
    def upload_album_name(service, album_name):

        # Get album in local library by name
        album_cache_jpg = LocalLibrary.cache_jpg()
        album_names = album_cache_jpg['album_names']

        if album_name not in album_names:
            logging.error(f"No local album found by name '{album_name}'")
            return
        
        local_album_idx = album_names[album_name]
        local_albums = album_cache_jpg['albums']
        local_album = local_albums[local_album_idx]

        # Call common upload method
        Uploader.upload_album(service, local_album)

    # -------------------------------------
    # Upload album for a given folder name
    # -------------------------------------
    @staticmethod
    def upload_album_names(album_names):

        gphoto.init()
        service = GoogleService.service()

        LocalLibrary.load_library('jpg')

        for album_name in album_names:
            Uploader.upload_album_name(service, album_name)

# ---------------------------------------------------------
# main
# ---------------------------------------------------------
def main():
    """
    Uploads albums from 'd:picsHres' and takes following parameters

        -a <array of album names>
        -p <array of album paths>
        -t <a tree folder with all the album paths
    """
    if len(sys.argv) < 3:
        logging.critical(f"Too few arguments.  Please see help")
        return

    # get the first argument switch
    argv_has_dash_a = False
    argv_has_dash_p = False
    argv_has_dash_t = False

    if sys.argv[1] == '-a':
        argv_has_dash_a = True
    elif sys.argv[1] == '-p':
        argv_has_dash_p = True
    elif sys.argv[1] == '-t':
        argv_has_dash_t = True
    else:
        logging.critical(f"Bad switch '{sys.argv[1]}'")
        return

    arg_list = []
    for arg in sys.argv[2:]:
        arg_list.append(arg)

    if argv_has_dash_a:
        Uploader.upload_album_names(arg_list)

if __name__ == '__main__':
  main()