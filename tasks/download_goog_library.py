import context; context.set_context()

import gphoto
from gphoto.goog_library import GoogLibrary

def main():
    gphoto.init()
    GoogLibrary.download_library()

if __name__ == '__main__':
  main()