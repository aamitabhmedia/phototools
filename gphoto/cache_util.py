import os
from pathlib import Path
import logging

from util.appdata import AppData
from util.log_mgr import LogMgr

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
                    logging.critical(f"GoogleAlbums:getif_cache_filepath: Unable to create cache dir '{CacheUtil._cache_path}'.  Aborting")
                    exit

        return CacheUtil._cache_path