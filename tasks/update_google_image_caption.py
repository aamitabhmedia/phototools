"""
given a file name and caption text the code finds the
imageID in local cache, makes a google api call to update
the caption.
"""
import context; context.set_context()

from datetime import datetime

import gphoto
from gphoto.google_images import GoogleImages


def main():
    gphoto.init()

    cache = GoogleImages.load_images()
    namedict = cache['namedict']

    image_name = "20050101_000436_OSWA_D70.jpg"
    image_idx = namedict[image_name]
    image = cache['list'][image_idx]
    
    request_body = {
        "description": f"{datetime.now()}: new-media-item-description"
    }


if __name__ == '__main__':
  main()