#!/bin/env python3

from lib.static_geometry import extract_static_geometry, import_static_geometry

def main():
	extract_static_geometry("files/level_client_static_geometry.txt", "output/level_client_static_geometry.txt.json")
	extract_static_geometry("files/level_server_static_geometry.txt", "output/level_server_static_geometry.txt.json", False)
	
	import_static_geometry("output/level_client_static_geometry.txt.json", "output/level_client_static_geometry.txt")
	import_static_geometry("output/level_server_static_geometry.txt.json", "output/level_server_static_geometry.txt")

main()