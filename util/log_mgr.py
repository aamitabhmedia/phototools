import os.path
from pathlib import Path
import sys
import colorlog
import logging
from logging.handlers import TimedRotatingFileHandler

"""
Package dependencies:
    conda install -c conda-forge colorlog
"""

class LogMgr:

    DEFAULT_LOGNAME = "phototools.log"

    _log_path = None

    # @staticmethod
    # def set_Log_level(int level):

    #     if level and level == 3:
    #         logging.getLogger().setLevel(logging.DEBUG)
    #     elif level and level == 2:
    #         logging.getLogger().setLevel(logging.INFO)
    #     else:
    #         logging.getLogger().setLevel(logging.WARNING)

    @staticmethod
    def log_path():
        return LogMgr._log_path

    @staticmethod
    def init(appdata_name, log_name, log_level=logging.INFO):

        log_dir = os.path.join(Path.home(), appdata_name, "logs")
        p = Path(log_dir)
        if (not p.exists()):
            p.mkdir(parents=True, exist_ok=True)

        LogMgr._log_path = os.path.join(log_dir, log_name)

        try:
            logging.basicConfig(
                level=log_level,
                format="%(asctime)s [%(levelname)-5.5s] %(message)s",
                handlers=[
                    TimedRotatingFileHandler(LogMgr._log_path, when="midnight", interval=1, encoding='utf8'),
                    logging.StreamHandler(sys.stdout)
                ]
            )
        except Exception as e:
            msg=f"CRITICAL ERROR: Unable to initialize logging: {e}"
            print(msg)
            sys.exit(msg)

    @staticmethod
    def set_level(level):
        if level == 1:
            logging.getLogger().setLevel(logging.INFO)
        elif level == 2:
            logging.getLogger().setLevel(logging.DEBUG)

    @staticmethod
    def title(message):
        logging.info("#########################################################")
        logging.info("   " + message)
        logging.info("#########################################################")
    
    @staticmethod
    def subtitle(message):
        logging.info("##-------------------------------------------")
        logging.info("      " + message)
        logging.info("##-------------------------------------------")

