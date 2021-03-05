import context; context.set_context()
import pprint

import gphoto
from gphoto.google_images import GoogleImages
from gphoto.google_albums import GoogleAlbums
from gphoto.google_album_images import GoogleAlbumImages

def main():
    gphoto.init()
    GoogleImages.load_images()
    GoogleAlbums.load_albums()
    GoogleAlbumImages.download_album_images()
    GoogleImages.save_images()

if __name__ == '__main__':
  main()