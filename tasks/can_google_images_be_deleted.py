import context; context.set_context()

import os
import json
import logging

import gphoto
from gphoto.google_library import GoogleLibrary
from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages
from gphoto.google_album_images import GoogleAlbumImages

from gphoto.local_library import LocalLibrary
def main():
    gphoto.init()

    GoogleLibrary.load_library()

    google_album_cache = GoogleAlbums.cache()
    google_album_ids = google_album_cache['ids']
    google_album_titles = google_album_cache['titles']

    google_image_cache = GoogleImages.cache()
    google_image_ids = google_image_cache['ids']
    google_image_filenames = google_image_cache['filenames']

    google_album_image_cache = GoogleAlbumImages.cache()
    google_album_images = google_album_image_cache['album_images']
    google_image_albums = google_album_image_cache['image_albums']

    LocalLibrary.load_raw_library()
    local_library_cache = LocalLibrary.cache_raw()
    local_albums = local_library_cache['albums']
    local_album_ids = local_library_cache['album_ids']
    local_images = local_library_cache['images']
    local_image_ids = local_library_cache['image_ids']


    result = []

    # Loop through each google album
    for local_album in local_albums:

        google_album_id = google_album['id']

        album_images = None
        if google_album_id in google_album_image_cache:
            album_images = google_album_image_cache[google_album_id]

        count = 0
        not_mine_count = 0
        if album_images:
            count = len(album_images)

            for image_idx in album_images:

                google_image = google_images[image_idx]
                if 'mine' in google_image:
                    mine = google_image['mine']
                    if not mine:
                        not_mine_count += 1

        ownership = None
        if not_mine_count == 0:
            ownership = "All-Mine"
        elif not_mine_count == count:
            ownership = "None-Mine"
        else:
            ownership = f"{count - not_mine_count}" + " Partial"

        title = None
        if 'title' not in google_album:
            title = "[EMPTY]" + google_album_id
        else:
            title = google_album['title']

        album_result = {
            'title': title,
            'shared': google_album['shared'],
            'image_count': count,
            'ownership': ownership
        }

        result.append(album_result)

    # Save to cache file also
    gphoto.save_to_file(result, "google_albums_summary.json")

if __name__ == '__main__':
  main()