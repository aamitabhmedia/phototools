import context; context.set_context()
import os
from pathlib import Path
import logging
import sys
import json

import gphoto

from googleapi.google_service import GoogleService

def main():
    gphoto.init()

    service = GoogleService.service()
    if not service:
        logging.error("GoogleAlbums.cache_albums: GoogleService.service() is not initialized")
        return

    # Album name used
    albumName = "2060 API Album"

    imageid01 = 'ALE2QTBp8OkubJCEMGMr4GTsThO3qMLWTit1_5DRyyQOD4IBUu5LJ8qFGwEb8AFy2yrlNlFTgtKt'
    imageid02 = 'ALE2QTBGNjlDhWc7Y3gwpGtIKvba849RolzOtcQ8xFgz1dh8J-Jmwa8vX80cYAGxJDjUu9m58gUu'
    image_ids = [imageid01, imageid02]

    # Create album
    request_body = {
        'album': {
            'title': albumName
        }
    }
    response_google_album = service.albums().create(body=request_body).execute()
    album_id = response_google_album['id']

    request_body = {
        'mediaItemIds': image_ids
    }
    response = service.albums().batchAddMediaItems(
        albumId=album_id,
        body=request_body
    ).execute()

    print(response)

if __name__ == '__main__':
  main()