import context; context.set_context()

import os
import logging
import json
import fire
from datetime import datetime
import requests

import gphoto
from gphoto.imageutils import ImageUtils
from googleapi.google_service import GoogleService
from gphoto.google_library import GoogleLibrary
from gphoto.local_library import LocalLibrary

upload_url = 'https://photoslibrary.googleapis.com/v1/uploads'

class GphotoImageCLITasks(object):

    def __init__(self):
        LocalLibrary.load_library('jpg')
        GoogleLibrary.load_library()

    # ---------------------------------------------------------
    def upload_image_bytes(self, filepath, filename, creds):
        headers = {
            'Authorization': 'Bearer ' + creds.token,
            'Content-type': 'application/octet-stream',
            'X-Goog-Upload-Protocol': 'raw',
            'X-Goog-File-Name': filename
        }    

        img = open(filepath, 'rb').read()
        response = requests.post(upload_url, data=img, headers=headers)
        if response is not None and response.status_code != 200:
            logging.error(f"Unable to upload bytes for image '{filepath}'")
        # print('\nUpload token: {0}'.format(response.content.decode('utf-8')))

        return response
        
    # ---------------------------------------------------------
    def upload_image_spec(self, image_spec, creds):

        filepath = image_spec.get('filepath')
        filename = image_spec.get('filename')

        # If image already in the local cache then ignore it
        google_cache = GoogleLibrary.cache()
        google_image_ids = google_cache.get('image_ids')
        if filename not in google_image_ids:
            logging.info(f"Image already uploaded: '{filename}'")
            return

        # Upload image bytes
        response = self.upload_image_bytes(filepath, filename, creds)


    # ---------------------------------------------------------
    def upload_image_spec_list(self, image_spec_list, creds):
        
        for image_spec in image_spec_list:

    # ---------------------------------------------------------
    def upload_folder(self, folder, recursive=True):

        logging.info(f"uploading images in folder: ({folder})")

        # Get only media types in the folder
        # image spec list holds a list of objects, sample below:
        # [
        #     {
        #         'filepath': ...,
        #         'filename': ...,
        #         'upload_token': ...
        #     },
        #     {
        #         .... next image object ....
        #     }
        # ]
        creds = GoogleService.credentials()

        image_spec_list = []
        folder_items = os.listdir(folder)
        filenames = [f for f in folder_items if os.path.isfile(os.path.join(folder, f)) and is_media(f)]

        for filename in filenames:

            # Build the spec for each file
            filepath = os.path.join(folder, filename)
            image_spec = {
                'filepath': filepath,
                'filename': filename
            }
            image_spec_list.append(image_spec)

        self.upload_image_spec_list(image_spec_list, creds)

        # Traverse sub-folders if recursive is specified
        if not recursive:
            return
        dirnames = [d for d in folder_items if os.path.isdir(d)]
        for dirname in dirnames:
            self.upload_folder(os.path.join(folder, dirname), recursive)

    # ---------------------------------------------------------
    def upload(self, filepath):

        image_spec_list = [
            {
                'filepath': filepath,
                'filename': os.path.basename(filepath)
            }
        ]
        creds = GoogleService.credentials()
        self.upload_image_spec_list(image_spec_list, creds)
