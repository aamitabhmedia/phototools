"""
High-Level Tasks that can be executed 
"""

from tasks.missing_google_albums import MissingGoogleAlbums

def missing_google_albums(pics_folder):
    """
    the function compares the images in pics_folder and
    Google media item cache and prints out albums that
    do not exist on Google Photos.
    And if the images also do not exist then that is noted as well
    """
    MissingGoogleAlbums.run(pics_folder)    
