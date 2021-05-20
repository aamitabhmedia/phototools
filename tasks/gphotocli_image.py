import logging
import fire
import context
context.set_context()


class GphotoImageCLI(object):
    """Google Image Command Module"""

    def upload_folder(self, folder, recursive=True):
        """Upload images in a folder, --recursive (default == True) will recurse the folder"""

        logging.info(f"uploading images in folder: ({folder})")

        # Get all media types in the folder

    def upload(self, filename, album_id=None):
        """Upload an image, and it will return google image id"""

        return f"Uploading file '{filename}', album_id='{album_id}'"

