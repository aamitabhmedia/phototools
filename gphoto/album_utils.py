import os
import sys

if __name__ == '__main__':
    import context
    context.set_context()

from pathlib import Path
import logging
import json
import subprocess

import exiftool

import util
from util.appdata import AppData
from util.log_mgr import LogMgr
from gphoto import core

class AlbumUtils(object):

    def abbrev(album_name):
        """
        Album should be of the form
            2013-01-01 Music in the Park
        """
        splits = album_name.split(' ')
        album_date = splits[0]
        date_split = album_date.split('-')
        if len(date_split) < 3:
            raise Exception(f"Album '{album_name}' has wrong date format")
        date_year = date_split[0]
        date_month = date_split[1]
        date_day = date_split[2]
        if len(date_year) < 4:
            raise Exception(f"Album '{album_name}' has wrong YEAR format")
        if len(date_month) < 2:
            raise Exception(f"Album '{album_name}' has wrong MONTH format")
        if len(date_day) < 2:
            raise Exception(f"Album '{album_name}' has wrong DAY format")

        date_year_two_digit =date_year[2:4]

        accum = ""
        for word in splits[1:]:
            word = word.capitalize()[0:3]
            accum += word
        
        accum += date_year_two_digit

        return accum

def main():
    if len(sys.argv) < 2:
        print("Missing arguments")
        sys.exit()
    
    cmd = sys.argv[1]
    values = sys.argv[2:]

    try:
        if cmd == 'abbrev':
            sys.stdout.write(AlbumUtils.abbrev(values[0]))
            sys.stdout.flush()
            sys.exit(0)

        else:
            print(f"command '{cmd}' is not supported")
            sys.exit(1)
    except Exception as e:
        sys.stderr.write(str(e))
        sys.stderr.flush()
        sys.stdout.write(None)
        sys.stdout.flush()
        sys.exit(1)

if __name__ == '__main__':
  main()