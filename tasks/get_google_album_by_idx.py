import context; context.set_context()
import pprint
import sys

import util
import gphoto
from gphoto.google_albums import GoogleAlbums

def main():

    if len(sys.argv) < 2:
        print("[ERROR]: Album index not specified")
        sys.exit()

    gphoto.init()
    GoogleAlbums.load_albums()
    cache = GoogleAlbums.cache()
    album_list = cache['list']

    idx = int(sys.argv[1])
    album = album_list[idx]
    util.pprint(album)    

if __name__ == '__main__':
  main()