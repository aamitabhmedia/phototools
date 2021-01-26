import context; context.set_context()

import sys

import util
from util.appdata import AppData
from util.log_mgr import LogMgr
from gphoto.exifutils import ExifUtils

def main():
    filename = sys.argv[1]
    metadata = ExifUtils.get_file_comments(filename)
    util.pprint(metadata)

if __name__ == '__main__':
  main()