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

def get_all_mediaItems():
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

def cache_all_mediaItems():
    _mediaItem_cache = get_all_mediaItems()
