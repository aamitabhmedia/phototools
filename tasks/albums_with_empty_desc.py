import context; context.set_context()

import exiftool

from gphoto.local_library import LocalLibrary
from gphoto.imageutils import ImageUtils
import gphoto
import util
import sys
import logging

import atexit

@atexit.register
def terminate_exiftool():
    with exiftool.ExifTool() as et:
        print("exiftoo running:'{et.running}'.  Terminating the process")
        et.terminate()

class AlbumsWithEmptyDesc(object):

    def find():
        """
        This method expects that the folder has been scanned and cached
        Reference: https://akrabat.com/setting-title-and-caption-with-exiftool/
        """

        # Scan all the images and load the metadata with just comments
        gphoto.init()
        # LocalLibrary.cache_raw_library("p:\\pics")
        # LocalLibrary.save_raw_library()
        LocalLibrary.load_raw_library()

        cache = LocalLibrary.cache_raw()
        images = cache['images']
        albums = cache['albums']

        # loop through all images. If image does not have comments
        # then add its album to album dictionary
        albums_missing_comments = {}
        with exiftool.ExifTool() as et:
            if not et.running:
                et.start()
            for image in images:
                filename = image['name']
                filepath = image['path']

                # if album already in the list then no need to get
                # metadata for this image
                parent_album_idx = image['parent']
                album = albums[parent_album_idx]
                album_name = album['name']
                if album_name in albums_missing_comments:
                    continue

                # check if any of the tags have any value
                # if the images has tag value then ignore this file
                comments = et.get_tags(ImageUtils._COMMENT_TAG_NAMES, filepath)
                comment = ImageUtils.get_any_comment(comments)
                if comment is not None:
                    continue

                # Found at least one image with no comments
                # Add its album to the list
                albums_missing_comments[album_name] = album['path']
                print(album['path'])
        
        return albums_missing_comments

def main():
  albums_missing_comments = AlbumsWithEmptyDesc.find()
  util.pprint(albums_missing_comments)

if __name__ == '__main__':
  main()