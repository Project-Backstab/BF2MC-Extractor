#!/bin/env python3

import os
from lib.ark import export_ark
from lib.cat import export_cat, export_cat_resource
from lib.viv import export_viv
from battlefield.files import CAT_LEVEL_FILES

def main():
	## Export iso file
	os.system("7z x \"files/Battlefield 2 - Modern Combat (USA).iso\" -ooutput/iso")
	
	## Export ARK files
	print("Export \"output/iso/BF2MC_MP/DATA.ARK\"")
	export_ark("output/iso/BF2MC_MP/DATA.ARK", "output/DATA.ARK/")
	print("Done!")
	
	"""
	## Extract level cat files
	for level_name, file_names in CAT_LEVEL_FILES.items():
		for file_name in file_names:
			if "resource" not in file_name:
				input_file_path = "output/DATA.ARK/Border/Levels/{}/{}".format(level_name, file_name)
				output_files_path = "output/Levels/{}/{}/".format(level_name, file_name)
				
				print("Export \"{}\"".format(input_file_path))
				export_cat(input_file_path, output_files_path)
				print("Done!")
	
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
	"""
	export_cat_resource("output/DATA.ARK/Border/Levels/BackStab/resources.cat",
			"output/DATA.ARK/Border/Levels/BackStab/resources.cat.json")
	export_cat_resource("output/DATA.ARK/Border/Levels/BackStab/resourcesCaptureTheFlag.cat",
			"output/DATA.ARK/Border/Levels/BackStab/resourcesCaptureTheFlag.cat.json")
	export_cat_resource("output/DATA.ARK/Border/Levels/BackStab/resourcesconquest.cat",
			"output/DATA.ARK/Border/Levels/BackStab/resourcesconquest.cat.json")
	"""
main()
