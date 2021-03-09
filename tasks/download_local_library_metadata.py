import context; context.set_context()

import sys
from datetime import datetime

import gphoto
from gphoto.local_library_metadata import LocalLibraryMetadata

def main():

    gphoto.init()

    do_raw = True
    do_jpg = True

    library_type = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "raw":
            do_jpg = False
        elif sys.argv[1] == "jpg":
            do_raw = False

    start_time = datetime.now()

    if do_raw:
        # LocalLibraryMetadata.cache_library_metadata("P:\\pics\\2014\\2014-02-14 Valentine's Day Celeberation", 'raw')
        LocalLibraryMetadata.cache_library_metadata("P:\\pics", 'raw')
        LocalLibraryMetadata.save_library_metadata('raw')
    if do_jpg:
        LocalLibraryMetadata.cache_library_metadata("d:\\picsHres", 'jpg')
        LocalLibraryMetadata.save_library_metadata('jpg')

    elapsed_time = datetime.now() - start_time
    print(f"Total Time: {elapsed_time}")

if __name__ == '__main__':
  main()