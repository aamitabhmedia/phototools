import context; context.set_context()

import sys

import util
from util.appdata import AppData
from util.log_mgr import LogMgr
from gphoto.exifutils import ExifUtils

def main():
<<<<<<< HEAD
    filenames = sys.argv[1:]
    metadata = ExifToolsUtil.get_comments(filename)
=======
    filename = sys.argv[1]
    metadata = ExifUtils.get_file_comments(filename)
>>>>>>> 0f90976ca25ce6af4fcffb277a2c86e45762e81e
    util.pprint(metadata)

if __name__ == '__main__':
  main()