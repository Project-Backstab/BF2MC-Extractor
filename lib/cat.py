#!/bin/env python3

import os
import json
import re

from lib.functions import create_file

TEMPLATE_FILE_INFO = {
	"path":          "",  ## File path
	"path_space":     0,  ## Extra empty space that is been used to keep a modulo 4 file path length
	"audio_header":   0,  ## Unknown header that has 1 or 0
}

def export_cat(input_cat_filepath, output_files_path):	
	## Create directories if they are missing
	os.makedirs(output_files_path, exist_ok=True)
	
	## Read cat file
	with open(input_cat_filepath, "rb") as f_cat:
		files_info = []
		
		## Read file size bytes until the end of the cat file is reached.
		while(data := f_cat.read(4)):
			file_info = dict(TEMPLATE_FILE_INFO)
			
			## Get File path
			file_path_length = int.from_bytes(data, byteorder='little')
			file_path = f_cat.read(file_path_length).decode('ascii')
			
			file_info["path"] = file_path.rstrip('\x00')
			file_info["path_space"] = len(file_path) - len(file_info["path"])
			
			## Get extra audio header information. Only for audio_*.cat files
			if("audio_" in input_cat_filepath):
				file_info["audio_header"] = f_cat.read(4).hex()
			
			## Get file data
			file_data_length = int.from_bytes(f_cat.read(4), byteorder='little')
			file_data = f_cat.read(file_data_length)
			
			## Save file
			create_file(output_files_path + file_info["path"], file_data)
			
			## Save file information
			files_info.append(file_info)
		
		## Save file information inside files.json
		with open(output_files_path + "files.json", "w") as f_files:
			f_files.write(json.dumps(files_info))

def import_cat(input_files_path, output_cat_filename):
	## Open files.json to get the files information to pack to .cat
	with open(input_files_path + "files.json", "r") as f_files:
		## Create new *.cat file
		with open(input_files_path  + output_cat_filename, "wb") as f_cat:
			files_info = json.load(f_files)
			
			for file_info in files_info:
				file_path_length = len(file_info["path"]) + file_info["path_space"]
				
				## Write file path
				f_cat.write(file_path_length.to_bytes(4, 'little'))
				f_cat.write(bytes(file_info["path"], 'ascii'))
				f_cat.write(b'\x00' * file_info["path_space"])
				
				## Fix: write extra header value for audio_*.cat files 
				if("audio_" in output_cat_filename):
					f_cat.write(bytes.fromhex(file_info["audio_header"]))
				
				file_path = input_files_path + "/" + file_info["path"]
				## Write file data
				with open(file_path, "rb") as f_file:
					file_size = os.path.getsize(file_path)
					
					f_cat.write(file_size.to_bytes(4, 'little'))
					f_cat.write(f_file.read(file_size))

RESOURCE_FILE_TYPES = [
	".brs",
	".ani",
	".ske",
	".sgf",
	".god",
	".prj",
	".pef",
	".cam",
	".msf",
	".atr",
	".hum",
	".col",
	".wef"
]

RESOURCE_OBJECT_TYPES = [
	# .brs : Serialised C++ Classes
	"CameraDescriptor",
	"ComponentWeaponDescriptor",
	"DebreeDescriptor",
	"EffectDescriptor",
	"LocatorDescriptor",
	"LockingComponentDescriptor",
	"MeshDescriptor",
	"PlayerEntryDescriptor",
	"PhysicsBodyDescriptor",
	"PhysicsBuoyanceyForceDescriptor",
	"PhysicsChildDescriptor",
	"PhysicsEngineDescriptor",
	"PhysicsRotorDescriptor",
	"PhysicsTrackDescriptor",
	"PhysicsTrackWheelDescriptor",
	"PhysicsWheelDescriptor",
	"RigidBodyDescriptor",
	"SoldierEntryDescriptor",
	"SkinTextureSwitchDescriptor",
	"SkyDescriptor",
	"TransformDescriptor",
	"TreeMeshDescriptor",
	"WeaponInputRouterDescriptor",
	
	# .ani : Animation file (Playback Data)
	"animation::Animation",
	
	# .ske : Skeleton of Soldier for Physics tasks. 
	"animation::Skeleton",
	
	# .sgf : SceneGraphFile Meshes Exported from Maya to PS2 friendly format
	"monk::collision::ICollisionBody",
	"Objects/Weapons/Effects/FFARImpacts.pefStaticModel",
	"SkinnedModel",
	"StaticModel",
	"TreeModel",
	
	# .god : 
	"PickupDescriptor",
	"StaticObjectDescriptor",
	"VehicleDescriptor",
	
	# .prj :
	"ClientMissileDescriptor",
	
	# .pef : 
	"ProjectileImpactEffectDescriptor",
	
	# .cam :
	"TransitionCamera",
	
	# .msf : 
	"ISoundBlockTemplateWrapper",
	
	# .atr :
	"AnimationTree",
	
	# .hum :
	"HumanPhysicsDescriptor",
	
	# .col :
	"SoldierCollisionDescriptor",
	
	# .wef :
	"WheelEffectsDescriptor"
]

def export_cat_resource(input_cat_filepath):
	## Get cat filename
	_, cat_filename = os.path.split(input_cat_filepath)
	
	## Create file path to save the files
	output_cat_files_path = "output/" + cat_filename + "/"
	
	## Create directories if they are missing
	os.makedirs(output_cat_files_path, exist_ok=True)
	
	## Read cat file
	with open(input_cat_filepath, "rb") as f_cat:
		with open(output_cat_files_path + "files.txt", "w") as f_files:
			object_info = ""
			
			while(data := f_cat.read(1)):
				data_int = int.from_bytes(data, byteorder='little')
				
				if(data_int < 0x20 or data_int > 0x7E):
					matches_file_ext = [(resource_type, match.start()) for resource_type in RESOURCE_FILE_TYPES for match in re.finditer(resource_type, object_info)]
					
					#if(" " in object_info and not matches_file_ext):
					if(" " in object_info and matches_file_ext):
						matches_obj_type = [(resource_type, match.start()) for resource_type in RESOURCE_OBJECT_TYPES for match in re.finditer(resource_type, object_info)]
						
						if(matches_obj_type):
							for _, _ in matches_file_ext:
								for resource_type, start_position in matches_obj_type:
									f_files.write(object_info[start_position:] + "\n")
						
						#if(len(object_info) > 8):
						#	print(object_info)
					
					## Reset
					object_info = ""
				else:
					object_info += data.decode("ascii")

