import context; context.set_context()

import sys

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

    if do_raw:
        # LocalLibraryMetadata.cache_library_metadata("p:\\pics", library_type)
        LocalLibraryMetadata.cache_library_metadata("P:\\pics", 'raw')
        LocalLibraryMetadata.save_library_metadata('raw')
    if do_jpg:
        LocalLibraryMetadata.cache_library_metadata("d:\\picsHres", 'jpg')
        LocalLibraryMetadata.save_library_metadata('jpg')

if __name__ == '__main__':
  main()