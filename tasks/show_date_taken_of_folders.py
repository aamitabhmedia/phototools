import context; context.set_context()
import os
import sys
from pathlib import Path
import logging
import sys
import json

import exiftool

# ---------------------------------------------------------
# traverse
# ---------------------------------------------------------
def traverse(et, folder):

    # Find first file and list its date taken
    for file in os.listdir(folder):
        if file.endswith(".jpg"):
            file_path = os.path.join(folder, file)
            date_shot = et.get_tag("CreateDate", file_path)
            print(f"'{date_shot}'\t'{folder}',\t'{file}'")
            break

    # Go into subolders and call it recursively
    for dirname in os.scandir(folder):
        if str(os.path.basename(dirname))[0] == 'S' and dirname.is_dir():
            traverse(et, os.path.join(folder, dirname))

# ---------------------------------------------------------
# main
# ---------------------------------------------------------
def main():
    """
        Given a folder as argument.  for every first jpg image in it
        identify the date taken
    """
    if len(sys.argv) < 2:
        logging.critical(f"Too few arguments.  Please see help")
        return

    folder = sys.argv[1]

    with exiftool.ExifTool() as et:
        traverse(et, folder)    


if __name__ == '__main__':
  main()