import context; context.set_context()
import os
from pathlib import Path
import logging
import sys

import util
import gphoto
from gphoto.local_library import LocalLibrary

class FindDuplicateImageNames:

  @staticmethod
  def find():
    """
    This method builds the cache for local raw pics folder,
    traverses it and find image name duplicates
    """
    gphoto.init()
    LocalLibrary.cache_raw_library("p:\\pics")
    LocalLibrary.save_raw_library()

    # TODO: implement the dup finding logic

def main():
  """
  """
  dups = FindDuplicateImageNames.find()
  util.pprint(dups)

if __name__ == '__main__':
  main()