"""
High-Level Tasks that can be executed 
"""

from tasks.missing_google_albums import MissingGoogleAlbums

def missing_google_albums(pics_folder):
    """
    The function compares the images in pics_folder and
    Google media item cache and prints out albums that
    do not exist on Google Photos.
    And if the images also do not exist then that is noted as well

    The structure that will be returned will be of the form:

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
    MissingGoogleAlbums.run(pics_folder)    
