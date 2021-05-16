import argparse

import os
import sys

def parse_args():
    # Create the parser
    my_parser = argparse.ArgumentParser(prog='gphoto', description='Gphoto Command Line Interface')

    # Add the arguments
    # Add module
    my_parser.add_argument('Module',
                        metavar='module',
                        type=str,
                        help='Name of the module')

    # Add module commands
    my_parser.add_argument('ModuleCommand',
                        metavar='module_command',
                        type=str,
                        help='Name of the module sub-command')

    # Add genera purpose switches
    my_parser.add_argument('-v', action='count', help='make output more verbose')

    # Execute the parse_args() method
    args = my_parser.parse_args()
    return args

def gphoto_cli():
    args = parse_args()
    print(args)

# -----------------------------------------------------
# Main
# -----------------------------------------------------
def main():
    gphoto_cli()

if __name__ == '__main__':
  main()