"""
High-Level Tasks that can be executed 
"""

from tasks.missing_albums_in_google import MissingAlbumsInGoogle
from tasks.find_duplicate_image_name import FindDuplicateImageNames

from tasks.find_duplicate_pics_folder_images import FindDuplicatePicsFolderImages

def missing_google_albums(pics_folder):
    """
    The function compares the images in pics_folder and
    Google media item cache and returns out albums that
    do not exist on Google Photos.
    And if the images also do not exist then that is noted as well

    The return structure is of the form:

    {
        "<album_name>": {
            'name': ....               # name of the album
            'path': ...                # full path of the album
            'missing': True | False    # True if album missing in Google
            'image_count': <n>         # list of images in this folder that
                                       # are uploaded to Google Photos
        }
    }
    """
    return MissingGoogleAlbums.find(pics_folder)    

def find_duplicate_pics_folder_images(pics_folder):
    """
    Parameters:

        pics_folder: Name of the root picture folder

    Returns a list of duplicate objects which show
    image names same in different folders:

    [
        "...image file name 1...": ["image_path_1a", "image_path_1b", ...],
        "...image file name 2...": ["image_path_2a", "image_path_2b", ...],
        ...
    ]

    You can pretty print this object as follows:
    import pprint
    pp = pprint.PrettyPrinter(indent=2, width=120, sort_dicts=False)
    pp.pprint(return_list)
    """
    return FindDuplicatePicsFolderImages.find(pics_folder)

def missing_albums_in_google(pics_folder):
    """
    Scans all the local album folders and checks if those
    albums are missing in Google photos.  This requires 
    caching the Google images and album data locally
    """
    return MissingAlbumsInGoogle.find(pics_folder)