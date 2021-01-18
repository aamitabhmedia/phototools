import os
from pathlib import Path
import json
import logging

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

_mediaItem_cache = None
_mediaItem_cache_path = None

def cache():
    return _mediaItem_cache

# -----------------------------------------------------
# load media items from google api
# -----------------------------------------------------
def get_mediaItems():
    service = GoogleService.service()
    if not service:
        logging.error("GoogleService.service() is not initialized")
        return
    
    # Get the first page of mediaItems
    pageSize=100
    response = service.mediaItems().list(
        pageSize=pageSize
    ).execute()

    _mediaItem_cache = response.get('mediaItems')
    nextPageToken = response.get('nextPageToken')

    # Loop through rest of the pages of mediaItems
    while nextPageToken:
        response = service.mediaItems().list(
            pageSize=pageSize,
            pageToken=nextPageToken
        ).execute()
        _mediaItem_cache.extend(response.get('mediaItems'))
        nextPageToken = response.get('nextPageToken')

    return _mediaItem_cache

# -----------------------------------------------------
# Cache media items to in-memory buffer from google api
# -----------------------------------------------------
def cache_mediaItems():
    _mediaItem_cache = get_mediaItems()

# --------------------------------------
# Get path to local cache file
# --------------------------------------
def cache_filepath():

    if not _mediaItem_cache_path:
        cache_dir = os.path.join(Path.home(), AppData.APPDATA_NAME, "cache")
        p = Path(cache_dir)
        if (not p.exists()):
            try:
                p.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logging.critical(f"media_mgr:cache_filepath: Unable to create cache dir '{cache_dir}'.  Aborting")
                exit

        _mediaItem_cache_path = os.path.join(cache_dir, "mediaItem_cache.json")

    return _mediaItem_cache_path

# --------------------------------------
# Save media items to local file
# --------------------------------------
def save_mediaItems_to_local_cache():

    cache_filepath = cache_filepath()

    try:
        cache_file = open(cache_filepath, "w")
        json.dump(_mediaItem_cache, cache_file, indent=2)
        cache_file.close()
        logging.info(f"media_mgr:save_mediaItems_to_local_cache: Successfully saved mediaItems to cache '{cache_filepath}'")
    except Exception as e:
        logging.critical(f"media_mgr:save_mediaItems_to_local_cache: unable to save mediaItems cache locally")
        raise

    return False