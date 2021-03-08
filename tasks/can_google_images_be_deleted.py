import context; context.set_context()

import sys
import logging

import util
import gphoto
from gphoto.local_library import LocalLibrary
from gphoto.goog_library import GoogLibrary
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    """
    Given a folder tree root like p:\\pics\\2014 loop through
    each album and find its images in Google photos.
    if the images do not have albums then they can be deleted.
    if the images have an album then
        and if the album have more images that the local album images
        and the albums is not shared then the images can be deleted
    """
    if len(sys.argv) < 2:
        logging.error("Too few arguments.  See help")
        return

    # Get arguments
    album_root = sys.argv[1]

    LocalLibrary.load_jpg_library()
    local_cache = LocalLibrary.cache_jpg()
    local_albums = local_cache.get('albums')
    local_album_paths = local_cache.get('album_paths')
    local_images = local_cache.get('images')


    GoogLibrary.load_library()
    google_cache = GoogLibrary.google_cache()
    google_album_ids = google_cache['album_ids']
    google_album_titles = google_cache['album_titles']
    google_image_ids = google_cache['image_ids']
    google_image_filenames = google_cache['image_filenames']
    google_album_images = google_cache['album_images']
    google_image_albums = google_cache['image_albums']

    result = []

    # Loop through each local folder under the root tree
    for local_album in local_albums:
        local_album_path = local_album.get('path')

        # filter out the ones that are not under the tree
        if not local_album_path.startswith(album_root):
            continue

        # Add this album to the list
        result_album = {
            'path': local_album.get('path')
        }
        result.append(result_album)

        # Get first jpeg image of the local album
        first_local_image = None
        local_album_image_idxs = local_album.get('images')
        for local_album_image_idx in local_album_image_idxs:

            local_image = local_images[local_album_image_idx]
            if local_album_image.get('mime') == 'image/jpeg':
                break
            else:
                local_image = None

        # Locate this image in Google photos
        


        first_local_images_idx = local_album_image_idxs[0]


if __name__ == '__main__':
  main()