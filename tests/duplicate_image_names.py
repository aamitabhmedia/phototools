import os
from pathlib import Path
import json
import logging
import pprint

class DuplicateImageNames:

    @staticmethod
    def dup_recursive(root_folder, cache, dircache):

        for root, directories, files in os.walk(root_folder):

            # print(f"--- '{root}'")

            # ignore directory if already seen
            if root in dircache:
                continue
            else:
                dircache[root] = True

            # Folder name will become album name
            folder_name = os.path.basename(root)

            for filename in files:

                fileext = Path(filename).suffix.lower()

                if fileext in [".jpg", ".jpeg", ".png", ".gif"]:

                    filepath = os.path.join(root, filename)

                    if filename in cache:
                        cache[filename].append(filepath)
                    else:
                        filelist = [filepath]
                        cache[filename] = filelist

            for dirname in directories:
                if dirname in ['undelete', 'misc']:
                    continue
                dirpath = os.path.join(root, dirname)
                DuplicateImageNames.dup_recursive(dirpath, cache, dircache)

    @staticmethod
    def main():
        cache = {}
        dircache = {}
        DuplicateImageNames.dup_recursive("d:\\picsHres\\2014", cache, dircache)

        dups = []
        for filename in cache:
            filelist = cache[filename]
            if len(filelist) > 1:
                dups.append({
                    'name': filename,
                    'files': filelist

                })
        pp = pprint.PrettyPrinter(indent=2, width=120, sort_dicts=False)
        pp.pprint(dups)

if __name__ == '__main__':
  DuplicateImageNames.main()