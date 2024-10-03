import os
from config                             import CONFIGS
from lib.ark                            import export_ark
from lib.cat                            import export_cat
from lib.cat_resource                   import export_cat_resource
from lib.viv                            import export_viv
from lib.txt.level_static_geometry      import export_level_static_geometry_txt
from lib.txt.beta.level_static_geometry import export_beta_level_static_geometry_txt
from lib.txt.level                      import export_level_txt
from lib.txt.beta.level                 import export_beta_level_txt
from lib.brs.mesh_descriptor            import export_mesh_descriptor
from lib.lnd.ps2                        import export_ps2_lnd
from lib.blend.lnd                      import export_lnd_2_blend
from lib.blend.static_model             import export_static_model_2_blend
from lib.blend.scene                    import export_scene
from lib.sgf                            import export_sgf, export_sgf_beta

def main():
	for config in CONFIGS:
		## Create directories if they are missing
		os.makedirs(config["output_directory"], exist_ok=True)
		os.makedirs("{}/Levels/".format(config["output_directory"]), exist_ok=True)
		
		## Export iso file
		os.system("7z x \"{}\" -o{}iso".format(config["iso"], config["output_directory"]))
		
		## Export ARK files
		input_ark_file = "{}/iso/{}/DATA.ARK".format(config["output_directory"], config["data_ark_directory"])
		output_ark_directory = "{}/DATA.ARK/".format(config["output_directory"])
		
		print("Export \"{}\"".format(input_ark_file))
		export_ark(input_ark_file, output_ark_directory)
		print("Done!")

		## Iterate through all cat files
		for level_name, file_names in config["cat_files"].items():
			input_level_path = "{}/DATA.ARK/Border/Levels/{}/".format(config["output_directory"], level_name)
			output_level_path = "{}/Levels/{}/".format(config["output_directory"], level_name)
			
			## Level Static Geometry .txt
			input_static_geometry = "{}/level_client_static_geometry.txt".format(input_level_path)
				
			print("Export \"{}\"".format(input_static_geometry))
			if(config["is_beta"]):
				export_beta_level_static_geometry_txt(input_static_geometry, input_static_geometry + ".json")
			else:
				export_level_static_geometry_txt(input_static_geometry, input_static_geometry + ".json")
			print("Done!")
				
			## Level .txt
			input_level_txt = "{}/level_client.txt".format(input_level_path)
				
			print("Export \"{}\"".format(input_level_txt))
			if(config["is_beta"]):
				export_beta_level_txt(input_level_txt, input_level_txt + ".json")
			else:
				export_level_txt(input_level_txt, input_level_txt + ".json")
			print("Done!")
			
			## Extract cat files
			for file_name in file_names:
				input_file_path = "{}/{}".format(input_level_path, file_name)
				output_files_path = "{}/{}/".format(output_level_path, file_name)
				
				print("Export \"{}\"".format(input_file_path))
				if "resource" not in file_name:
					
					has_audio_header = ("audio" in file_name)
					
					export_cat(input_file_path, output_files_path, has_audio_header)
				else:
					export_cat_resource(input_file_path, output_files_path)
				print("Done!")
		
		## Export landscape files
		for root, dirs, files in os.walk("{}/DATA.ARK/".format(config["output_directory"])):
			for file in files:
				if file.endswith('.lnd'):
					input_file_path = os.path.join(root, file)
					
					print("Export \"{}\"".format(input_file_path))
					export_ps2_lnd(input_file_path, input_file_path + ".json")
					export_lnd_2_blend(input_file_path + ".json", input_file_path + ".blend")
					print("Done!")
		
		## export .brs and .sgf files
		for root, dirs, files in os.walk("{}/Levels/".format(config["output_directory"])):
			for file in files:
				if file.endswith('.brs'):
					input_file_path = os.path.join(root, file)
					
					print("Export \"{}\"".format(input_file_path))
					export_mesh_descriptor(input_file_path, input_file_path + ".json")
					print("Done!")

				if file.endswith('.sgf'):
					input_file_path = os.path.join(root, file)
					output_file_path = f"{input_file_path}.json"
					output_file_path2 = f"{input_file_path}.blend"
					
					print(f"Export \"{input_file_path}\"")
					if(config["is_beta"]):
						export_sgf_beta(input_file_path, output_file_path)
					else:
						export_sgf(input_file_path, output_file_path)
					
					try:
						export_static_model_2_blend(output_file_path, output_file_path2)
					except:
						pass
					
					print("Done!")
		
		## Combine objects and export scene
		for level_name, file_names in config["cat_files"].items():
			export_scene(config["output_directory"], level_name)
		
		## Export viv
		if(config["extract_viv"]):
			print("Export \"output/iso/SINGLE/8.VIV\"")
			export_viv("output/iso/SINGLE/8.VIV", "output/8.VIV/")
			print("Done!")
			
			print("Export \"output/iso/SINGLE/DATA.VIV\"")
			export_viv("output/iso/SINGLE/DATA.VIV", "output/DATA.VIV/")
			print("Done!")
			
			print("Export \"output/iso/SINGLE/DATA2.VIV\"")
			export_viv("output/iso/SINGLE/DATA2.VIV", "output/DATA2.VIV/")
			print("Done!")

main()
