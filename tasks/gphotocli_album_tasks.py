import context; context.set_context()

import os
import logging
import json
import fire
from datetime import datetime

import gphoto
from googleapi.google_service import GoogleService
from gphoto.google_library import GoogleLibrary
from gphoto.local_library import LocalLibrary

class GphotoAlbumCLITasks(object):
    """Module to handle Google album specific commands"""

    def __init__(self):
        LocalLibrary.load_library('jpg')
        GoogleLibrary.load_library()

    # -------------------------------------------------
    def upload_tree(self, root):
        """Create albums in the root folder, and make all albums shareable"""

        # Argument validation
        if not os.path.exists(root):
            logging.error(f"Folder does not exist: ({root})")
            return

        # Initialize Google API and load cache.  We will need it later in the upload fn
        google_cache = GoogleLibrary.cache()
        service = GoogleService.service()

        # Traverse all the sub folders in the cache
        local_cache = LocalLibrary.cache('jpg')
        local_albums = local_cache.get('albums')

        for local_album in local_albums:

            local_album_name = local_album['name']
            local_album_path = local_album['path']

            if not local_album_path.lower().startswith(root.lower()):
                continue

            self.upload(local_album_path)

    # -------------------------------------------------
    def upload(self, folder):
        """Create album given folder path and make it shareable"""

        logging.info(f"Uploading Album: {folder}")

        # Argument validation
        if not os.path.exists(folder):
            logging.error(f"Folder does not exist: ({folder})")
            return

        # Remove trailing slash
        slash_char = folder[len(folder) - 1]
        if slash_char == '/' or slash_char == '\\':
            folder = folder[:len(folder)-1]

        # Get Google API service
        service = GoogleService.service()

        # Get the album name by getting the leaf of the path
        arg_album_name = os.path.basename(folder)
        logging.info(f"Using album name: ({arg_album_name})")

        # Check if album already exist in Google Photos
        google_cache = GoogleLibrary.cache()
        google_albums = google_cache.get('albums')
        google_album_titles = google_cache.get('album_titles')

        # Variables holding cached or new Google Albums
        google_album_idx = google_album_titles.get(arg_album_name)
        google_album = google_albums.[google_album_idx] if google_album_idx is not None else None
        google_album_id = google_album.get('id') if google_album is not None else None

        # Album at Google Photos does not exist.  Create it
        if google_album is None:

            # Create the album
            # The example response will be of the format
            # {
            #     'id': 'ALE2QTDMyDXRLF65-tBPb7ikKamvkMrpMi43FKCRtQ0uB2Yjab7SvoZ9sjTwVywxpHnaGtw_yVQd',
            #     'title': "1950-01-01 Baba's Family Early Life",
            #     'productUrl': 'https: //photos.google.com/lr/album/ALE2QTDMyDXRLF65-tBPb7ikKamvkMrpMi43FKCRtQ0uB2Yjab7SvoZ9sjTwVywxpHnaGtw_yVQd', 'isWriteable': True
            # }
            try:
                request_body = {
                    'album': {
                        'title': arg_album_name
                    }
                }
                album_create_response = service.albums().create(body=request_body).execute()
                google_album_id = album_create_response.get('id')
                logging.info(f"Album Created: {album_create_response}")

                # Make album sharable
                request_body = {
                    'sharedAlbumOptions': {
                        'isCollaborative': True,
                        'isCommentable': True
                    }
                }
                album_share_response = service.albums().share(
                    albumId=google_album_id,
                    body=request_body
                ).execute()
                logging.info(f"Album Shared: {album_share_response}")

                # Now get the album from Google to see if it has been created as shareable
                # We will now add it to our local cache and save the cache
                album_get_response = service.albums().get(albumId=google_album_id).execute()
                if album_create_response is not None:
                    google_cache_album_ids = google_cache['album_ids']
                    google_cache_titles = google_cache['titles']
                    GoogleLibrary.cache_album(album_get_response,
                        google_cache_album_ids,
                        google_cache_titles,shared=True)
                    GoogleLibrary.save_library()

            except Exception as e:
                logging.error(f"Error while creating album ({arg_album_name}): {str(e)}")
                return


        # Now upload the images
        # First collect all the images from the local folder

        creds = GoogleService.credentials()


    # -------------------------------------------------
    def get(self, title=None, id=None):
        """Return 'album' object given the 'title' or 'id'"""
        return None