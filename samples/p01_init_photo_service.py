# Reference: https://learndataanalysis.org/getting-started-with-google-photos-api-and-python-part-1/

import os
from Google import Create_Service

API_NAME = 'photoslibrary'
API_VERSION = 'v1'
CLIENT_SECRET_FILE = 'client_secret_GoogleAPITutorials_PhotoDesktopApp.json'
SCOPES = ['https://www.googleapis.com/auth/photoslibrary',
          'https://www.googleapis.com/auth/photoslibrary.sharing']

service = Create_Service(CLIENT_SECRET_FILE,API_NAME, API_VERSION, SCOPES)