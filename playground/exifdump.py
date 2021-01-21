import sys
import subprocess
from subprocess import check_output

import exiftool
import pprint

def main():
  """
  """
  files = sys.argv[1:]

  with exiftool.ExifTool() as et:
      metadata = et.get_metadata_batch(files)
      pp = pprint.PrettyPrinter(indent=2, width=120, sort_dicts=False)
      pp.pprint(metadata)

if __name__ == '__main__':
  main()