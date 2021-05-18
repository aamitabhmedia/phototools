import context; context.set_context()

import os
import logging
import json
import fire

import gphoto
from googleapi.google_service import GoogleService
from gphoto.google_library import GoogleLibrary

class GphotoAlbumCLI(object):
    """Module to handle Google album specific commands"""

    def __init__(self):
        """GphotoAlbumCLI init function"""
        GoogleLibrary.load_library()        

    # -------------------------------------------------
    def create(self, folder, share: bool = True):
        """Create album given 'local folder path', '--share' (default) to make it shareable"""

        # Argument validation
        if not os.path.exists(folder):
            logging.error(f"Folder does not exist: ({folder})")
            return

        # Get the leaf dir name from the album path
        album_name = os.path.basename(folder)
        logging.info(f"Using album name: ({album_name})")

        # Initialize/Get Google Service
        service = GoogleService.service()

        # Check if album already exist in Google Photos
        album_exists = False


        # Create the album
        # The example response will be of the format
        # {
        #     'id': 'ALE2QTDMyDXRLF65-tBPb7ikKamvkMrpMi43FKCRtQ0uB2Yjab7SvoZ9sjTwVywxpHnaGtw_yVQd',
        #     'title': "1950-01-01 Baba's Family Early Life",
        #     'productUrl': 'https: //photos.google.com/lr/album/ALE2QTDMyDXRLF65-tBPb7ikKamvkMrpMi43FKCRtQ0uB2Yjab7SvoZ9sjTwVywxpHnaGtw_yVQd', 'isWriteable': True
        # }
        request_body = {
            'album': {
                'title': album_name
            }
        }
        album_create_response = None
        try:
            album_create_response = service.albums().create(body=request_body).execute()
            logging.info(f"Album Created: {album_create_response}")
        except Exception as e:
            logging.error(f"Error while creating album ({album_name}): {str(e)}")
            return

        # Make album sharable
        if share:
            request_body = {
                'sharedAlbumOptions': {
                    'isCollaborative': True,
                    'isCommentable': True
                }
            }
            album_share_response = service.albums().share(
                albumId=album_create_response['id'],
                body=request_body
            ).execute()
            logging.info(f"Album Shared: {album_share_response}")

    # -------------------------------------------------
    def get(self, title=None, id=None):
        """Return 'album' object given the 'title' or 'id'"""
        return None