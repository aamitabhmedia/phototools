import context; context.set_context()

import os
from pathlib import Path
import logging
import sys
import json

from datetime import datetime, timedelta
import glob

import exiftool
import subprocess

from tasks.fix_pfilm_dateshot import fix_pfilm_dateshot

# -----------------------------------------------------
# The goal of this script is 
# -----------------------------------------------------
def main():
    """
        Given a root folder, for all its subfolders:
        1.  Remove "Sxxx - " prefix form sub folder
        2.  Set dateshot to 10AM for the date from the album name
        3.  Add comments from the album name
    """

    # Parse arguments
    argc = len(sys.argv)
    if argc < 2:
        print("Too few arguments. Please see help")
        return

    root_folder = sys.argv[1]

    # Get subfolders
    for srcdir in os.scandir(root_folder):

        # 1. Remove the prefix and rename the folder
        tgtdir = srcdir
        basedir = os.path.basename(srcdir)
        if basedir[0] == 'S':
            basedir = basedir[7:]
            tgtdir = os.path.join(root_folder, basedir)
            os.rename(srcdir, tgtdir)

        # 2. Get date from the foldername and set date
        #       of images in that folder
        album_date = basedir[:10]
        fix_pfilm_dateshot(os.path.join(tgtdir, '*'), album_date, None, "8", False)

        # 3. Add folder name as caption and rename files
        ps_command = subprocess.run(["powershell", "-Command", f"-c -r '{tgtdir}'"], capture_output=True)

if __name__ == '__main__':
  main()