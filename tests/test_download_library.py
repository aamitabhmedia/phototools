import context; context.set_context()
import pprint
import gphoto
from gphoto.library import Library

def main():
    gphoto.init()
    Library.download_library()

if __name__ == '__main__':
  main()