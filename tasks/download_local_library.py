import context; context.set_context()

import gphoto
from gphoto.local_library import LocalLibrary

def main():
    gphoto.init()
    LocalLibrary.cache_library("p:\\pics", 'raw')
    LocalLibrary.save_library('raw')

    LocalLibrary.cache_library("d:\\picsHres", 'jpg')
    LocalLibrary.save_library('jpg')

if __name__ == '__main__':
  main()