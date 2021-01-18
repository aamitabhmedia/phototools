import os
from pathlib import Path
import json
import logging

from util.appdata import AppData
from util.log_mgr import LogMgr
from googleapi.google_service import GoogleService

_mediaItem_cache = None
_mediaItem_cache_path = None

def get_MediaItems(service)