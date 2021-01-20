from gphoto.google_images import GoogleImages
from gphoto import mediaItems
from gphoto.pics_folder import PicsFolder


class MissingGoogleAlbums(object):

import gphoto
from gphoto.pics_folder import PicsFolder
from gphoto.google_images import GoogleImages

    @staticmethod
    def run(pics_folder):
        pics_folder_cache = PicsFolder.cache()
        google_image_cache = GoogleImages.cache()
