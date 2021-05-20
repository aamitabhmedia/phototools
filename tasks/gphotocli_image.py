import context; context.set_context()

import os

import logging
import fire

from tasks.gphotocli_image_tasks import GphotoImageCLITasks
class GphotoImageCLI(object):
    """Google Image Command Module"""

    def __init__(self):
        self._gphotocli_image_tasks = GphotoImageCLITasks()

    def upload_folder(self, folder, recursive=True):
        """Upload images in a folder, --recursive (default == True) will recurse the folder, return success"""
        return self._gphotocli_image_tasks.upload_folder(folder, recursive)


    def upload(self, filepath, album_id=None):
        """Upload an image, and it will return google image id"""
        return self._gphotocli_image_tasks.upload(filepath, album_id)

