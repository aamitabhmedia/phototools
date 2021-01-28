from pathlib import Path
import os.path

class AppData:

    APPDATA_NAME = ".phototools"

    @staticmethod
    def get_folder_path():
        return Path.home() / AppData.APPDATA_NAME

    @staticmethod
    def init():
        folder_path = Path(AppData.get_folder_path())
        if (not folder_path.exists()):
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"CRITICAL: Unable to create {folder_path}: {e}")
                exit
