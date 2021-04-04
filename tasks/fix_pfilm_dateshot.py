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

import util
import gphoto
from gphoto.imageutils import ImageUtils

# -----------------------------------------------------
# Convert stae time spec into epoch timestamp
# -----------------------------------------------------
def str_to_epoch(str_time):

    splits = str_time.split(' ')
    dt = splits[0]
    dt_splits = dt.split(':')
    year = int(dt_splits[0]) if len(dt_splits) > 0 else 1900
    month = int(dt_splits[1]) if len(dt_splits) > 1 else 1
    day = int(dt_splits[2]) if len(dt_splits) > 2 else 1

    tm = splits[1] if len(splits) > 0 else "10:00:00"
    tm_splits = tm.split(':')
    hour = int(tm_splits[0]) if len(tm_splits) > 0 else 10
    min = int(tm_splits[1]) if len(tm_splits) > 1 else 0
    sec = int(tm_splits[2]) if len(tm_splits) > 2 else 0

    epoch = datetime(year, month, day, hour, min, sec)
    return epoch

# -----------------------------------------------------
# Convert from datetime to exifdate "YYYYMMDD hh:mm:ss"
# -----------------------------------------------------
def to_exifdate(dt):
    dtstr = f"{dt.year:04}:{dt.month:02}:{dt.day:02} {dt.hour:02}:{dt.minute:02}:{dt.second:02}"
    return dtstr

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
    arg_listOnly = False
    arg_files_pattern = None
    arg_iter = enumerate(sys.argv)
    for arg_index, arg in arg_iter:
        if arg == '-s':
            arg_startTime = sys.argv[arg_index+1]
            next(arg_iter)
        elif arg == '-e':
            arg_endTime = sys.argv[arg_index+1]
            next(arg_iter)
        elif arg == '-l':
            arg_listOnly = True
        elif arg.startswith('-'):
            print(f"[ERROR]: Unrecognized switch {arg}")
            return
        else:
            arg_files_pattern = arg

    print("--------------------------------------------")
    print(f"   start: {arg_startTime}")
    print(f"     end: {arg_endTime}")
    print(f"listOnly: {arg_listOnly}")
    print(f"  folder: {arg_files_pattern}")
    print("--------------------------------------------")

    # Get total number of minutes between start and stop times
    startEpoch = str_to_epoch(arg_startTime)
    endEpoch = str_to_epoch(arg_endTime)
    diff = endEpoch - startEpoch
    diff_sec = (diff.days * 24 * 60 * 60) + diff.seconds

    # Get the list of jpg files with the pattern
    filenames = []
    for filename in glob.glob(arg_files_pattern):
        filenames.append(filename)

    # Calculate the time interval based on the number of images
    image_count = len(filenames)
    if image_count == 0:
        print(f"[WARN]: No images found with patten '{arg_files_pattern}'")
        return

    interval_sec = diff_sec//image_count
    print(f"[INFO]: interval_sec = '{interval_sec}', interval_minutes = '{interval_sec//60}'")

    # Loop through each image and set its date time stamp
    print(f"[INFO]: Setting file dateshot")
    increment = 0
    with exiftool.ExifTool() as et:
        for filename in filenames:
            dt = startEpoch + timedelta(seconds=increment)
            exiftool_date = to_exifdate(dt)

            print(f"  '{exiftool_date}': '{filename}'")

            if not arg_listOnly:
                et.execute(
                    b'-AllDates=' + exiftool_date.encode(),
                    b'-overwrite_original',
                    exiftool.fsencode(filename)
                )

            increment += interval_sec

if __name__ == '__main__':
  main()