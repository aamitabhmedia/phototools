import context; context.set_context()

import os
import json
import logging

import gphoto
from gphoto.google_albums import GoogleAlbums
from gphoto.google_images import GoogleImages
from gphoto.google_album_images import GoogleAlbumImages

def main():
    gphoto.init()

    GoogleAlbums.load_albums()
    google_album_cache = GoogleAlbums.cache()
    google_albums = google_album_cache['list']

    GoogleImages.load_images()
    google_image_cache = GoogleImages.cache()
    google_images = google_image_cache['list']

    GoogleAlbumImages.load_album_images()
    google_album_image_cache = GoogleAlbumImages.cache()

    result = []

    # Loop through each google album
    for google_album in google_albums:

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