import context; context.set_context()

import sys

import gphoto
from gphoto.local_library import LocalLibrary

def main():

    gphoto.init()

    library_type = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "raw":
            library_type = sys.argv[1]
            LocalLibrary.cache_library_metadata("p:\\pics", library_type)
        elif sys.argv[1] == "jpg":
            library_type = sys.argv[1]
            LocalLibrary.cache_library_metadata("d:\\picsHres", library_type)
        else:
            print("Expecting argument 'raw' or 'jpg' or None for both type")
            return


    LocalLibrary.cache_library_metadata("p:\\pics", library_type)
    LocalLibrary.cache_raw_library()
    LocalLibrary.save_library('raw')
    LocalLibrary.cache_jpg_library("d:\\picsHres", library_type)
    LocalLibrary.save_library('jpg')

if __name__ == '__main__':
  main()