from genericpath import exists
import os
from pathlib import Path
import logging
import json
import sys

from util.appdata import AppData
from util.log_mgr import LogMgr
import gphoto

class CacheUtil:

    _cache_path = None

    # ---------------------------------------------------------
    # Get Cache Dir
    # ---------------------------------------------------------
    @staticmethod
    def cache_dir():
        if not CacheUtil._cache_path:
            CacheUtil._cache_path = os.path.join(Path.home(), AppData.APPDATA_NAME, "cache")
            p = Path(CacheUtil._cache_path)
            if (not p.exists()):
                try:
                    p.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    msg=f"CacheUtil.cache_dir: Unable to create cache dir '{CacheUtil._cache_path}'.  Aborting"
                    logging.critical(msg)
                    sys.exit(msg)

        return CacheUtil._cache_path

    # ---------------------------------------------------------
    # Save Cache to file
    # ---------------------------------------------------------
    @staticmethod
    def save_to_file(cache, filename):
        cache_filepath = os.path.join(gphoto.cache_dir(), filename)

        with open(cache_filepath, 'w') as writer:
            json.dump(cache, writer, indent=2)
            logging.info(f"CacheUtil.save_to_file: Successfully saved '{cache_filepath}'")

    # ---------------------------------------------------------
    # Load Cache from file
    # ---------------------------------------------------------
    @staticmethod
    def load_from_file(filename):
        cache_dir = CacheUtil.cache_dir()
        if not exists(cache_dir):
            logging.error(f"CacheUtil.load_from_file: Folder does not exist '{cache_dir}'")
            return None

        cache_filepath = os.path.join(cache_dir, filename)
        if not exists(cache_filepath):
            logging.error(f"CacheUtil.load_from_file: File does not exist '{cache_filepath}'")
            return None

        cache = None
        with open(cache_filepath, 'r') as reader:
            cache = json.load(reader)
            logging.info(f"CacheUtil.load_from_file: Successfully loaded '{cache_filepath}'")

        return cache