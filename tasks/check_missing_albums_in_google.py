from gphoto.google_images import GoogleImages
from gphoto import google_images
from gphoto.pics_folder import PicsFolder
from gphoto.google_library import GoogleLibrary


class MissingAlbumsInGoogle(object):
    """
    The class assumes that the Google library cache is loaded
    Run the following to load the cache if not already done:

    import gphoto
    from gphoto.google_library import GoogleLibrary
    gphoto.init()
    GoogleLibrary.load_library()
    """

    @staticmethod
    def find(local_cache, google_cache):
        """
        Given a local pics folder
        """
        pics_folder_cache = PicsFolder.cache()
        google_image_cache = GoogleImages.cache()

        if not pics_folder_cache or not google_image_cache:
            GoogleLibrary.load_library()
            pics_folder_cache = PicsFolder.cache()
            google_image_cache = GoogleImages.cache()

        