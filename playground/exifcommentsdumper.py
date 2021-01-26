import context; context.set_context()

import sys

import util
from util.appdata import AppData
from util.log_mgr import LogMgr
from gphoto.exiftools_util import ExifToolsUtil

def main():
    filenames = sys.argv[1:]
    metadata = ExifToolsUtil.get_comments(filename)
    util.pprint(metadata)

if __name__ == '__main__':
  main()