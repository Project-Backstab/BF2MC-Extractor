#!/bin/env python3

import os
from lib.ark import export_ark
from lib.cat import export_cat, export_cat_resource
from lib.viv import export_viv
from lib.static_geometry import extract_static_geometry, import_static_geometry
from lib.level_txt import extract_level_txt, import_level_txt
from battlefield.files import CAT_LEVEL_FILES, CAT_LEVEL_FILES_V1_0, CAT_LEVEL_FILES_V2_01, CAT_LEVEL_FILES_BETA

def main():
	## Export iso file
	os.system("7z x \"files/Battlefield 2 - Modern Combat (USA).iso\" -ooutput/iso")
	
	## Export ARK files
	print("Export \"output/iso/BF2MC_MP/DATA.ARK\"")
	export_ark("output/iso/BF2MC_MP/DATA.ARK", "output/DATA.ARK/")
	print("Done!")
	
	## Extract level cat files
	for level_name, file_names in CAT_LEVEL_FILES.items():
		input_level_path = "output/DATA.ARK/Border/Levels/{}/".format(level_name)
		output_level_path = "output/Levels/{}/".format(level_name)
		
		## Static Geometry
		input_static_geometry = input_level_path + "level_client_static_geometry.txt"
		
		print("Export \"{}\"".format(input_static_geometry))
		extract_static_geometry(input_static_geometry, input_static_geometry + ".json")
		print("Done!")
		
		## Level txt
		input_level_txt = input_level_path + "level_client.txt"
		
		print("Export \"{}\"".format(input_level_txt))
		extract_level_txt(input_level_txt, input_level_txt + ".json")
		print("Done!")
		
		for file_name in file_names:
			if "resource" not in file_name:
				input_file_path = input_level_path + file_name
				output_files_path = output_level_path + file_name + "/"
				
				print("Export \"{}\"".format(input_file_path))
				export_cat(input_file_path, output_files_path)
				print("Done!")
	
	"""
	print("Export \"output/iso/SINGLE/8.VIV\"")
	export_viv("output/iso/SINGLE/8.VIV", "output/8.VIV/")
	print("Done!")
	
	print("Export \"output/iso/SINGLE/DATA.VIV\"")
	export_viv("output/iso/SINGLE/DATA.VIV", "output/DATA.VIV/")
	print("Done!")
	
	print("Export \"output/iso/SINGLE/DATA2.VIV\"")
	export_viv("output/iso/SINGLE/DATA2.VIV", "output/DATA2.VIV/")
	print("Done!")
	
	for level_name, file_names in CAT_LEVEL_FILES.items():
		for file_name in file_names:
			if "resource" in file_name:
				input_file_path = "output/DATA.ARK/Border/Levels/{}/{}".format(level_name, file_name)
				output_json_filepath = "output/DATA.ARK/Border/Levels/{}/{}".format(level_name, file_name + ".json")
				
				print("Export \"{}\"".format(input_file_path))
				export_cat_resource(input_file_path, output_json_filepath)
				print("Done!")
	"""

main()
