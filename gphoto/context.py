import os
import sys

def set_context():
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
