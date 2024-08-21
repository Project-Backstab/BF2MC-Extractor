#!/bin/env python3

import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from lib.xma import export_xma

def main():
	export_xma("files/RC_02.xma", "output/RC_02.wav")
	export_xma("files/30mmWhizz.xma", "output/30mmWhizz.wav")

if __name__ == "__main__":
    main()