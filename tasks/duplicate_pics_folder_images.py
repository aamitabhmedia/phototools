

import os
from pathlib import Path
import logging

class DuplicatePicsFolderImages:

    @staticmethod
    def dup_recursive(root_path, cache, dircache):

        for root, directories, files in os.walk(root_path, topdown=True):

            # ignore directory if already seen
            if root in dircache:
                continue
            else:
                dircache[root] = True

            # if dirname in one of these then ignore it
            dirsplits = os.path.split(root)
            if dirsplits in ['undelete', 'misc', 'orig', 'uncataloged', 'iphone', 'praw']:
                continue

            # Loop through files in this folder
            for filename in files:

                fileext = Path(filename).suffix.lower()

                if fileext in [".jpg", ".jpeg", ".png", ".gif", ".nef", ".cr2"]:

                    filepath = os.path.join(root, filename)

                    if filename in cache:
                        cache[filename].append(filepath)
                    else:
                        cache[filename] = [filepath]

            for dirname in directories:
                dirpath = os.path.join(root, dirname)
                DuplicatePicsFolderImages.dup_recursive(dirpath, cache, dircache)

    @staticmethod
    def find(pics_folder):

        cache = {}
        dircache = {}
        DuplicatePicsFolderImages.dup_recursive(pics_folder, cache, dircache)

        dups = []
        for filename in cache:
            filelist = cache[filename]
            if len(filelist) > 1:
                dups.append({
                    'name': filename,
                    'files': filelist

                })

        return dups

