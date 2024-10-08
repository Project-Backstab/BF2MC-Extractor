#!/bin/env python3

import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from lib.txt.level_static_geometry      import export_level_static_geometry_txt, import_level_static_geometry_txt
from lib.txt.beta.level_static_geometry import export_beta_level_static_geometry_txt

def main():
	export_level_static_geometry_txt("files/BackStab/level_client_static_geometry.txt", "output/BackStab/level_client_static_geometry.txt.json")
	export_level_static_geometry_txt("files/BackStab/level_server_static_geometry.txt", "output/BackStab/level_server_static_geometry.txt.json", False)
	
	import_level_static_geometry_txt("output/BackStab/level_client_static_geometry.txt.json", "output/BackStab/level_client_static_geometry.txt")
	import_level_static_geometry_txt("output/BackStab/level_server_static_geometry.txt.json", "output/BackStab/level_server_static_geometry.txt")

	export_beta_level_static_geometry_txt("files/wilderness/level_client_static_geometry.txt", "output/wilderness/level_client_static_geometry.txt.json")

	os.system("sha256sum files/BackStab/level_client_static_geometry.txt")
	os.system("sha256sum output/BackStab/level_client_static_geometry.txt")
	
	os.system("sha256sum files/BackStab/level_server_static_geometry.txt")
	os.system("sha256sum output/BackStab/level_server_static_geometry.txt")
	
main()