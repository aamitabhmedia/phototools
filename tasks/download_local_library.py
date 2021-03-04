import context; context.set_context()

import gphoto
from gphoto.local_library import LocalLibrary

def main():
    gphoto.init()
    LocalLibrary.cache_raw_library("p:\\pics")
    LocalLibrary.save_raw_library()
    LocalLibrary.cache_jpg_library("d:\\picsHres")
    LocalLibrary.save_jpg_library()

if __name__ == '__main__':
  main()