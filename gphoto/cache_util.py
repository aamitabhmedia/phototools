import os
from pathlib import Path
import logging
import json

from util.appdata import AppData
from util.log_mgr import LogMgr
import gphoto

class CacheUtil:

    _cache_path = None

    @staticmethod
    def cache_dir():
        if not CacheUtil._cache_path:
            CacheUtil._cache_path = os.path.join(Path.home(), AppData.APPDATA_NAME, "cache")
            p = Path(CacheUtil._cache_path)
            if (not p.exists()):
                try:
                    p.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    msg=f"GoogleAlbums:getif_cache_filepath: Unable to create cache dir '{CacheUtil._cache_path}'.  Aborting"
                    logging.critical(msg)
                    sys.exit(msg)

        return CacheUtil._cache_path
    

    @staticmethod
    def save_to_file(cache, filename):
        cache_filepath = os.path.join(gphoto.cache_dir(), filename)
        try:
            cache_file = open(cache_filepath, "w")
            json.dump(cache, cache_file, indent=2)
            cache_file.close()
            logging.info(f"CacheUtil.save_to_cache: Successfully saved cache to '{cache_filepath}'")
            return True
        except Exception as e:
            logging.critical(f"CacheUtil.save_to_cache: unable to save cache to '{cache_filepath}'")
            raise