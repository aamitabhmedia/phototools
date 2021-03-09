import context; context.set_context()

import sys
import os

import gphoto
from gphoto.local_library_metadata import LocalLibraryMetadata


def main():

    gphoto.init()

    LocalLibraryMetadata.load_library_metadata('raw')
    cache = LocalLibraryMetadata.cache_raw()

    for image_id, image in cache.items():
        datetimeoriginal = image.get('DateTimeOriginal')
        createdate = image.get('CreateDate')

        filename = os.path.basename(image_id)
        if filename.startswith("PFILM"):
            continue

        ext = image.get('FileTypeExtension')
        if ext and ext == 'mov':
            continue

        if datetimeoriginal is None and createdate is not None:
            print(image_id)
            print(f"    CreateDate='{createdate}'")


if __name__ == '__main__':
  main()