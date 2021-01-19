import context; context.set_context()
import pprint
import gphoto
from gphoto.mediaItems import MediaItems

def main():
    gphoto.init()
    MediaItems.download_mediaItems()

if __name__ == '__main__':
  main()