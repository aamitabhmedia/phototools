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
        desc = image.get('Description')
        title = image.get('Title')

        # filename = os.path.basename(image_id)
        # if filename.startswith("PFILM"):
        #     continue

        # ext = image.get('FileTypeExtension')
        # if ext and ext == 'mov':
        #     continue

        if '2009-10-31 Haloween party at Gambhir' in image_id:
            continue

        if "2011-07-04 Amitabh's 50th Birthday Post Celeberation" in image_id:
            continue

        if "2017 04 16 Vocal Performance M.A." in image_id:
            continue

        if "2009-08-06 Italy Trip" in image_id:
            continue

        if desc is not None and title is not None and desc != title:
            print(image_id)
            print(f"     desc='{desc}'")
            print(f"    title='{title}'")


if __name__ == '__main__':
  main()