#!/bin/env python3

import os
from lib.level_txt import extract_level_txt, import_level_txt

def main():
	extract_level_txt("files/BackStab/level_client.txt", "output/BackStab/level_client.txt.json")
	extract_level_txt("files/BackStab/level_server.txt", "output/BackStab/level_server.txt.json")
	
	import_level_txt("output/BackStab/level_client.txt.json", "output/BackStab/level_client.txt")
	import_level_txt("output/BackStab/level_server.txt.json", "output/BackStab/level_server.txt")
	
	os.system("sha256sum files/BackStab/level_client.txt")
	os.system("sha256sum output/BackStab/level_client.txt")
	
	os.system("sha256sum files/BackStab/level_server.txt")
	os.system("sha256sum output/BackStab/level_server.txt")

main()