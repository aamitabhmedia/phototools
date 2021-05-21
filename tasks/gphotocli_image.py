import context; context.set_context()

import os

import logging
import fire

from tasks.gphotocli_image_tasks import GphotoCLIImageTasks
class GphotoImageCLI(object):
    """Google Image Command Module"""

    def __init__(self):
        self._gphotocli_image_tasks = GphotoCLIImageTasks()

    def upload(self, folder, recursive=True):
        """Upload images in a folder, --recursive (default == True) will recurse the folder, return success"""
        return self._gphotocli_image_tasks.upload(folder, recursive)


    def upload_single(self, filepath):
        """Upload an image, and it will return google image id"""
        return self._gphotocli_image_tasks.upload_single(filepath)

