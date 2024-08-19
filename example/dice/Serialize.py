#!/bin/env python3

import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from lib.dice.serialize import Dice_UnSerializeFile

def main():
	Dice_UnSerializeFile("files/InputNodeMap.txt", "output/InputNodeMap.txt.json")
	Dice_UnSerializeFile("files/physicssettings.txt", "output/physicssettings.txt.json")

main()
