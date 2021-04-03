import context; context.set_context()
import os
from pathlib import Path
import logging
import sys
import json

from datetime import datetime
import glob

import exiftool

import util
import gphoto
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# Convert stae time spec into epoch timestamp
# -----------------------------------------------------
def str_to_epoch(str_time):

    splits = str_time.split(' ')
    dt = splits[0]
    tm = splits[1]

    dt_splits = dt.split(':')
    year = int(dt_splits[0])
    month = int(dt_splits[1])
    day = int(dt_splits[2])

    tm_splits = tm.split(':')
    hour = int(tm_splits[0])
    min = int(tm_splits[1])
    sec = int(tm_splits[2])

    epoch = datetime(year, month, day, hour, min, sec)
    return epoch


# -----------------------------------------------------
# The goal of this script is 
# -----------------------------------------------------
def main():
    """
    Arguments:
        -s start datetime "YYY:MM:DD HH:MM:SS"
        -e end datetime
        <file specification>
    """

    # Parse arguments
    argc = len(sys.argv)
    if argc < 5:
        print("Too few arguments. Please see help")
        return

    arg_startTime = None
    arg_endTime = None
    # arg_pattern = None
    arg_files_pattern = None
    arg_iter = enumerate(sys.argv)
    for arg_index, arg in arg_iter:
        if arg == '-s':
            arg_startTime = sys.argv[arg_index+1]
            next(arg_iter)
        elif arg == '-e':
            arg_endTime = sys.argv[arg_index+1]
            next(arg_iter)
        # elif arg == '-p':
        #     arg_pattern = sys.argv[arg_index+1]
        #     next(arg_iter)
        elif arg.startswith('-'):
            print(f"Unrecognized switch {arg}")
            return
        else:
            arg_files_pattern = arg

    print("--------------------------------------------")
    print(f"  start: {arg_startTime}")
    print(f"    end: {arg_endTime}")
    # print(f"pattern: {arg_pattern}")
    print(f" folder: {arg_files_pattern}")
    print("--------------------------------------------")

    # Get total number of minutes between start and stop times
    startEpoch = str_to_epoch(arg_startTime)
    endEpoch = str_to_epoch(arg_endTime)
    diff = endEpoch - startEpoch
    diff_sec = (diff.days * 24 * 60 * 60) + diff.seconds
    diff_mins = diff_sec//60

    # Get the list of jpg files with the pattern
    for filename in glob.glob(arg_files_pattern):
        print(filename)


if __name__ == '__main__':
  main()