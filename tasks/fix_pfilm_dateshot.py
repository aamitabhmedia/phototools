import context; context.set_context()
import os
from pathlib import Path
import logging
import sys
import json

from datetime import datetime

import exiftool

import util
import gphoto
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# The goal of this script is 
# -----------------------------------------------------
def main():
    """
    Arguments:
        -s start datetime "YYY:MM:DD HH:MM:SS"
        -e end datetime
        -p pattern
        <folder>
    """

    # Parse arguments
    argc = len(sys.argv)
    if argc < 5:
        print("Too few arguments. Please see help")
        return

    arg_startTime = None
    arg_endTime = None
    arg_pattern = None
    arg_folder = None
    arg_iter = enumerate(sys.argv)
    for arg_index, arg in arg_iter:
        if arg == '-s':
            arg_startTime = sys.argv[arg_index+1]
            next(arg_iter)
        elif arg == '-e':
            arg_endTime = sys.argv[arg_index+1]
            next(arg_iter)
        elif arg == '-p':
            arg_pattern = sys.argv[arg_index+1]
            next(arg_iter)
        elif arg.startswith('-'):
            print(f"Unrecognized switch {arg}")
            return
        else:
            arg_folder = arg




    print("--------------------------------------------")
    print(f"  start: {arg_startTime}")
    print(f"    end: {arg_endTime}")
    print(f"pattern: {arg_pattern}")
    print(f" folder: {arg_folder}")
    print("--------------------------------------------")


if __name__ == '__main__':
  main()