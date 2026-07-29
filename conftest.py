import os
import sys

# Prepend repository root directory to sys.path to guarantee 'app' module resolution
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
