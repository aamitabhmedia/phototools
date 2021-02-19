"""
given a file name and caption text the code finds the
imageID in local cache, makes a google api call to update
the caption.
"""
import context; context.set_context()
from googleapi.google_service import GoogleService

from datetime import datetime

import gphoto
from googleapi.google_service import GoogleService
from gphoto.google_images import GoogleImages


def main():
    """
    Test code to se if image caption can updated if the images
    was uploaded using Google Photos UI.

    This is not working at this time.  You will see the following
    error:

        "code": 403,
        "message: "Request had insufficient authentication scopes"
        "status": "PERMISSION_DENIED"
    """
    gphoto.init()

    cache = GoogleImages.load_images()
    filenames = cache['filenames']

    image_name = "20050101_000436_OSWA_D70.jpg"
    image_idx = filenames[image_name]
    image = cache['list'][image_idx]
    
    # "ALE2QTAJEnDlApTBWwq-U5n0pg6ulXVp5wdAkqwXVj0knHwrKGcyqFoCt5x5CzeXd_1FUD4VEvrkAZzGaqOxiJIcrsuZmHgJYw"
    image_id = image['id']

    request_body = {
        "description": f"{datetime.now()}: new-media-item-description"
    }

    service = GoogleService.service()
    response = service.mediaItems().patch(
        id=image_id,
        body=request_body
    ).execute()

    print(response)

if __name__ == '__main__':
  main()