import pickle
import sys
import os
import logging
import tempfile
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Reference:
#   https://developers.google.com/gmail/api/quickstart/python
#   https://dev.to/davidedelpapa/manage-your-google-photo-account-with-python-p-1-9m2

# TODO - once the env is fixed after reboot
# OAUTH_PATH = os.environ.get('OAUTH_PATH')
OAUTH_PATH = "d:\\OAuth\\"
API_NAME = 'photoslibrary'
API_VERSION = 'v1'

CLIENT_SECRET_FILE = 'gphotoup_oauth.json'
CLIENT_SECRET_PATH = OAUTH_PATH + CLIENT_SECRET_FILE
SCOPES = [
    'https://www.googleapis.com/auth/photoslibrary',
    'https://www.googleapis.com/auth/photoslibrary.edit.appcreateddata',
    'https://www.googleapis.com/auth/photoslibrary.sharing'
    ]

PICKLE_FILE_NAME = f'token_gphotoup_{API_NAME}_{API_VERSION}.pickle'
PICKLE_FILE_PATH = os.path.join(tempfile.gettempdir(), PICKLE_FILE_NAME)

class GoogleService:
    """
        Tries to initialize Google API service.
        If any error is found then the program exits
        It expects client secrets file to be in "$OAUTH_PATH/gphotoup_oauth.json"
    """

    # Internal field holding the Google API Service
    _google_service = None

    @staticmethod
    def service():
        return GoogleService._google_service

    @staticmethod
    def init(client_secret_file=CLIENT_SECRET_PATH, api_name=API_NAME, api_version=API_VERSION, scopes=SCOPES):

        logging.debug(f'GoogleAPI: Spec')
        logging.debug(f'  client_secret_file = {client_secret_file}')
        logging.debug(f'  api_name, version = {api_name}, {api_version}')
        logging.debug(f'  scopes = {scopes}')

        # Make sure client OAuth 2 secret file exists.  If not then
        # go to console.developers.google.com and create credentials
        if not os.path.exists(client_secret_file):
            msg = f"GoogleAPI: client_secret_file '{client_secret_file} does not exist'.  Aborting!! Please go to console.developers.google.com and download credentials for gphotoup project"
            logging.critical(msg)
            raise Exception(msg)

        cred = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(PICKLE_FILE_PATH):
            logging.info(f"GoogleAPI: Load refresh toke pickle file '{PICKLE_FILE_PATH}'")
            with open(PICKLE_FILE_PATH, 'rb') as token:
                cred = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                logging.info(f"GoogleAPI: Refreshing auth token request")
                cred.refresh(Request())
            else:
                logging.info(f"GoogleAPI: Request user for auth token")
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
                cred = flow.run_local_server(port=0)

            # Save the credentials for the next run
            logging.info(f"GoogleAPI: Saving refreshed token to pickle file '{PICKLE_FILE_PATH}'")
            with open(PICKLE_FILE_PATH, 'wb') as token:
                pickle.dump(cred, token)

        # Now get access to the service object
        try:
            GoogleService._google_service = build(api_name, api_version, credentials=cred, cache_discovery=False)
            logging.info(f"GoogleAPI: Service '{api_name}' created successfully")
        except Exception as e:
            msg=f"GoogleAPI: Unable to create google API service '{api_name}'.  Aborting"
            logging.critical(msg)
            logging(str(e))
            sys.exit(msg)

        return None
