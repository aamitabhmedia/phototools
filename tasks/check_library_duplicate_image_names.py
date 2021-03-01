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

    # The dups dict holds
    #   key: image name
    #   list: list of image paths
    name_to_paths = {}

    # traverse the images list. For each image add its name
    cache = LocalLibrary.cache_raw()
    cache_images = cache['images']
    cache_image_ids = cache['image_ids']

    for image in cache_images:
      imagename = image['name']
      imagepath = image['path']

      if imagename not in name_to_paths:
        name_to_paths[imagename] = [imagepath]
      else:
        name_to_paths[imagename].append(imagepath)

    # review the dups where imagename is holding multiple image paths
    dups = []
    for imagename, imagelist in name_to_paths.items():
      if len(imagelist) > 1:
        dup = {
          'name': imagename,
          'paths': []
        }

        paths = dup['paths']
        for imagepath in imagelist:
          paths.append(imagepath)
        
        dups.append(dup)
    
    return dups

def main():
  """
  """
  dups = FindDuplicateImageNames.find()
  gphoto.save_to_file(dups, "find_duplicate_image_names.json")
  # util.pprint(dups)

if __name__ == '__main__':
  main()