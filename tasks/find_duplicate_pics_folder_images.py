
import os
from pathlib import Path
import logging

class FindDuplicatePicsFolderImages:

    @staticmethod
    def dup_recursive(root_path, cache, dircache):

        # Get all files under this folder
        for file in os.scandir(root_path):
            if file.is_file():
                fileext = Path(file.name).suffix.lower()

                if fileext in [".jpg", ".jpeg", ".png", ".gif", ".nef", ".cr2"]:

                    if file.name in cache:
                        cache[file.name].append(file.path)
                    else:
                        cache[file.name] = [file.path]

        # Get all dirs under this folder
        for subdir in os.scandir(root_path):
            if subdir.is_dir():
                if subdir.name not in ['raw', 'undelete', 'misc', 'orig', 'uncataloged', 'ipPhone', 'praw', 'craw', 'cr2']:
                    FindDuplicatePicsFolderImages.dup_recursive(subdir.path, cache, dircache)

    @staticmethod
    def find(pics_folder):

        cache = {}
        dircache = {}
        FindDuplicatePicsFolderImages.dup_recursive(pics_folder, cache, dircache)

        dups = []
        for filename in cache:
            filelist = cache[filename]
            if len(filelist) > 1:
                dups.append({
                    'name': filename,
                    'files': filelist

                })

        return dups

