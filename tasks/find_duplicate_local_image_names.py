import context; context.set_context()
from gphoto import google_albums

import os
import json
import logging

import gphoto
from gphoto.google_library import GoogleLibrary
from gphoto.local_library import LocalLibrary

def main():
    gphoto.init()

    # Load Local picsHres jpg Library
    LocalLibrary.load_library('jpg')
    local_cache = LocalLibrary.cache_jpg()
    local_albums = local_cache.get('albums')
    local_album_paths = local_cache.get('album_paths')
    local_album_names = local_cache.get('album_names')
    local_images = local_cache.get('images')
    local_image_ids = local_cache.get('image_ids')

    # temp_result is a dict holding image name as key
    # and an array value of image paths
    temp_result = {}

    # Loop through each images, get their leaf names and see
    # if image part with this name already exists
    for local_image in local_images:

        # Add image name and path to the temp_result
        image_name = local_image.get('name')
        image_path = local_image.get('path')
        
        image_path_list = temp_result.get(image_name)
        if image_path_list is None:
            image_path_list = [image_path]
            temp_result[image_name] = image_path_list
        else:
            image_path_list.append(image_path)

    # Now remove entries for temp_result where there is only one image path
    result = {}
    found = False
    for image_name in temp_result:
        image_path_list = temp_result.get(image_name)
        if len(image_path_list) > 1:
            found = True
            result[image_name] = image_path_list

    print(f"found duplicates = {found}")

    # Save to cache file also
    if found:
        gphoto.save_to_file(result, "find_duplicate_local_image_names.json")

if __name__ == '__main__':
  main()