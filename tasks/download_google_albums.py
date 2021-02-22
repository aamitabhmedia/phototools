import context; context.set_context()

import gphoto
from gphoto.google_albums import GoogleAlbums

def main():
    gphoto.init()
    GoogleAlbums.download_albums()

if __name__ == '__main__':
  main()