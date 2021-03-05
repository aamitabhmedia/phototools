import logging
from os import read
import requests
from requests.api import head

from googleapi.google_service import GoogleService

UPLOAD_URL = 'https://photoslibrary.googleapis.com/v1/uploads'

class AlbumAPI(object):

    def upload_image(google_album_id, image_path, image_name, image_mime, creds):

        headers = {
            'Authorization': 'Bearer ' + creds.token,
            'Content-type': 'application/octet-stream',
            'X-Goog-Upload-Content-Type': image_mime,
            'X-Goog-Upload-protocol': 'raw',
            'X-Goog-File-Name': image_name
        }

        # Read image into a local variable as binary
        with open(image_path, 'rb') as reader:
            img_bin = reader.read()
            response = requests.post(UPLOAD_URL, data=img_bin, headers=headers)

            request_body = {

            }