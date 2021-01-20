from gphoto.google_images import GoogleImages
from gphoto import google_images
from gphoto.pics_folder import PicsFolder


class MissingGoogleAlbums(object):

    @staticmethod
    def find(pics_folder):
        pics_folder_cache = PicsFolder.cache()
        google_image_cache = GoogleImages.cache()

        if not pics_folder_cache:
            pics_folder_cache = PicsFolder.load_cache()
