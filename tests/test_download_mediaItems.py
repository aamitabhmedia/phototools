import context; context.set_context()
import pprint
import gphoto
from gphoto.google_images import GoogleImages

def main():
    gphoto.init()
    GoogleImages.download_images()

if __name__ == '__main__':
  main()