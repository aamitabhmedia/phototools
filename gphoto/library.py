import os
from pathlib import Path
import json
import logging

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

_library_cache = None
_library_cache_path = None

def cache():
    return _library_cache

# -----------------------------------------------------
# load media items from google api
# -----------------------------------------------------
def fetch_library_from_google():
    service = GoogleService.service()
    if not service:
        logging.error("GoogleService.service() is not initialized")
        return
    
    # Get the first page of mediaItems
    pageSize=100
    response = service.mediaItems().list(
        pageSize=pageSize
    ).execute()

    _library_cache = response.get('mediaItems')
    nextPageToken = response.get('nextPageToken')

    # Loop through rest of the pages of mediaItems
    while nextPageToken:
        response = service.mediaItems().list(
            pageSize=pageSize,
            pageToken=nextPageToken
        ).execute()
        _library_cache.extend(response.get('mediaItems'))
        nextPageToken = response.get('nextPageToken')

    return _library_cache

# -----------------------------------------------------
# Cache media items to in-memory buffer from google api
# -----------------------------------------------------
def cache_library():
    fetch_library_from_google()
    return _library_cache

# --------------------------------------
# Get path to local cache file
# --------------------------------------
def get_cache_filepath():

    cache_dir = os.path.join(Path.home(), AppData.APPDATA_NAME, "cache")
    p = Path(cache_dir)
    if (not p.exists()):
        try:
            p.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logging.critical(f"media_mgr:cache_filepath: Unable to create cache dir '{cache_dir}'.  Aborting")
            exit

    _library_cache_path = os.path.join(cache_dir, "mediaItem_cache.json")
    return _library_cache_path

# --------------------------------------
# Save media items to local file
# --------------------------------------
def save_library():

    cache_filepath = get_cache_filepath()

    try:
        cache_file = open(cache_filepath, "w")
        json.dump(_library_cache, cache_file, indent=2)
        cache_file.close()
        logging.info(f"media_mgr:save_mediaItems_to_local_cache: Successfully saved mediaItems to cache '{cache_filepath}'")
    except Exception as e:
        logging.critical(f"media_mgr:save_mediaItems_to_local_cache: unable to save mediaItems cache locally")
        raise

    return False

# --------------------------------------
# Load library cache from local file 
# --------------------------------------
def load_library():
    """
    Loads in-memory cache from local cache file
        Return: cache object
    You can also get the cache object later
    by calling cache() defined in this file
    """

    # We will reload the cache from local file
    _library_cache = None

    cache_filepath = get_cache_filepath()
    if not os.path.exists(cache_filepath):
        logging.warning(f"load_library: No mediaItem cache file available.  Ignored")
        return

    try:
        cache_file = open(cache_filepath)
    except Exception as e:
        logging.critical(f"load_library: Unable top open mediaItems cache file")
        raise

    try:
        _library_cache = json.load(cache_file)
        logging.info(f"load_library: Successfully loaded mediaItems from cache '{cache_filepath}'")
    except Exception as e:
        _library_cache = None
        logging.error(f"load_library: Error occurred while loading mediaItem cache")
        raise

    return _library_cache

# -------------------------------------------
# cache from google api and save it locally
# -------------------------------------------
def download_library():
    cache_library()
    save_library()
    return _library_cache
