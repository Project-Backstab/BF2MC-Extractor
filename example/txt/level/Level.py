#!/bin/env python3

import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from lib.txt.level      import export_level_txt, import_level_txt
from lib.txt.beta.level import export_beta_level_txt

def main():
	export_level_txt("files/BackStab/level_client.txt", "output/BackStab/level_client.txt.json")
	export_level_txt("files/BackStab/level_server.txt", "output/BackStab/level_server.txt.json")
	
	import_level_txt("output/BackStab/level_client.txt.json", "output/BackStab/level_client.txt")
	import_level_txt("output/BackStab/level_server.txt.json", "output/BackStab/level_server.txt")
	
	export_beta_level_txt("files/wilderness/level_client.txt", "output/wilderness/level_client.txt.json")

	os.system("sha256sum files/BackStab/level_client.txt")
	os.system("sha256sum output/BackStab/level_client.txt")
	
	os.system("sha256sum files/BackStab/level_server.txt")
	os.system("sha256sum output/BackStab/level_server.txt")

main()