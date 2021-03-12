import context; context.set_context()

import gphoto
from gphoto.google_library import GoogleLibrary

def main():
    gphoto.init()
    GoogleLibrary.download_library()

    # GoogleLibrary.load_library()
    # GoogleLibrary.cache_albums()
    # GoogleLibrary.save_library()

if __name__ == '__main__':
  main()