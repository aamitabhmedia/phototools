import os
import sys

def set_context():
    cpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    print(cpath)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
