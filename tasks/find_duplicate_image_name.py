import os
from pathlib import Path
import logging

import util
import gphoto
from gphoto.local_library import LocalLibrary

class FindDuplicateImageNames:

  @staticmethod
  def find_main(root_folder):
    gphoto.init()
    LocalLibrary.cache_raw_library(root_folder)
    LocalLibrary.save_raw_library()
    util.pprint(LocalLibrary.cache_raw_library)

def main():
    root_folder = "p:\\pics"
    FindDuplicateImageNames.find(root_folder)

if __name__ == '__main__':
  main()