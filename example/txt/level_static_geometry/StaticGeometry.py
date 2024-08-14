#!/bin/env python3

import os
from lib.txt.static_geometry import export_level_static_geometry, import_level_static_geometry

def main():
	export_level_static_geometry("files/level_client_static_geometry.txt", "output/level_client_static_geometry.txt.json")
	export_level_static_geometry("files/level_server_static_geometry.txt", "output/level_server_static_geometry.txt.json", False)
	
	import_level_static_geometry("output/level_client_static_geometry.txt.json", "output/level_client_static_geometry.txt")
	import_level_static_geometry("output/level_server_static_geometry.txt.json", "output/level_server_static_geometry.txt")

	os.system("sha256sum files/level_client_static_geometry.txt")
	os.system("sha256sum output/level_client_static_geometry.txt")
	
	os.system("sha256sum files/level_server_static_geometry.txt")
	os.system("sha256sum output/level_server_static_geometry.txt")
	
main()