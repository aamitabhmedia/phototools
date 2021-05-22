import context; context.set_context()

import os

import logging
import fire

from tasks.gphotocli_image_tasks import GphotoCLIImageTasks
class GphotoImageCLI(object):
    """Google Image Command Module"""

    def __init__(self):
        self._gphotocli_image_tasks = GphotoCLIImageTasks()

    def upload(self, folder, recursive=True, test=False):
        """Upload images in a folder, --recursive (default == True) will recurse the folder, return success"""
        return self._gphotocli_image_tasks.upload(folder, recursive, test)


    def upload_single(self, filepath, test=False):
        """Upload an image, and it will return google image id"""
        return self._gphotocli_image_tasks.upload_single(filepath, test)

