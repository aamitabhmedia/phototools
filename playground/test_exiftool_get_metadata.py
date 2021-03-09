import context; context.set_context()

import os
import subprocess
import tempfile
import csv
import json

import gphoto
import util
from gphoto import core

_METADATA_TAGS = [
    '-DateTimeOriginal',
    '-CreateDate',
    '-Description',
    '-Title',
    '-FileTypeExtension',
    '-MimeType',
    '-Model'
]

def main():

    cmd = ['exiftool', '-q', '-csv', '-r']
    for tag in _METADATA_TAGS:
        cmd.append(tag)
    for ext in core.MEDIA_EXTENSIONS:
        cmd.append('-ext')
        cmd.append(ext)
    cmd.append("D:\\picsHres\\2014\\2014-01-31 Pleasanton Karaoke Party at Home")
    print(cmd)

    csvfile = os.path.join(tempfile.gettempdir(), 'image_library_metadata.csv')
    print(csvfile)
    with open(csvfile, "w") as writer:
        subprocess.run(cmd, stdout=writer)

    result = {}

    with open(csvfile) as reader:

        csv_reader = csv.reader(reader, delimiter=',')

        first_row = True
        columns = None
        for row in csv_reader:
            if first_row:
                first_row = False
                columns = row
            else:
                metadata = {}
                result[row[0]] = metadata
                
                num_columns = len(columns)
                for idx, column in enumerate(columns):
                    if idx == 0:
                        continue
                    metadata[column] = row[idx]

    jsonfile = os.path.join(tempfile.gettempdir(), 'image_library_metadata.json')
    print(jsonfile)
    with open(jsonfile, "w") as writer:
        json.dump(result, writer, indent=2)

    # util.pprint(result)

if __name__ == '__main__':
  main()