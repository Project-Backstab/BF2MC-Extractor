#!/bin/env python3

import os
import json
import re
import binascii
import zlib

from lib.functions import create_file, modify_file_path

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
		
		content = f_cat.read()
		
		if(content[0:4].decode("ascii") == "PZFB"):
			content = zlib.decompress(content[0x10:])
		
		## Read file size bytes until the end of the cat file is reached.
		offset = 0
		while(offset + 4 < len(content)):
			file_info = dict(TEMPLATE_FILE_INFO)
			
			## Get File path
			file_path_length = int.from_bytes(content[offset:offset + 4], byteorder='little')
			offset += 4
			file_path = content[offset:offset + file_path_length].decode('ascii')
			offset += file_path_length
			
			file_info["path"] = file_path.rstrip('\x00')
			file_info["path_space"] = len(file_path) - len(file_info["path"])
			
			## Get extra audio header information. Only for audio_*.cat files
			if("audio_" in input_cat_filepath):
				file_info["audio_header"] = content[offset:offset + 4].hex()
				offset += 4
			
			## Get file data
			file_data_length = int.from_bytes(content[offset:offset + 4], byteorder='little')
			offset += 4
			
			file_data = content[offset:offset + file_data_length]
			offset += file_data_length
			
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
	"ChaseCamera",
	"ComponentWeaponDescriptor",
	"DebreeDescriptor",
	"EffectDescriptor",
	"EntryInputActionMap",
	"GameplaySoundDescriptor",
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
	"SoldierDescriptor",
	"SoldierEntryDescriptor",
	"SkinTextureSwitchDescriptor",
	"SkyDescriptor",
	"TransformDescriptor",
	"TreeMeshDescriptor",
	"VehicleCamera",
	"VehicleEffectsDescriptor",
	"WeaponInputRouterDescriptor",
	
	# .ani : Animation file (Playback Data)
	"animation::Animation",
	
	# .ske : Skeleton of Soldier for Physics tasks. 
	"animation::Skeleton",
	
	# .sgf : SceneGraphFile Meshes Exported from Maya to PS2 friendly format
	"monk::collision::ICollisionBody",
	"SkinnedModel",
	"StaticModel",
	"TreeModel",
	
	# .god : 
	"PickupDescriptor",
	"StaticObjectDescriptor",
	"TeamDescriptor",
	"VehicleDescriptor",
	"LevelSettingsDescriptor",
	
	# .prj :
	"ClientBulletDescriptor",
	"ClientExplosionPackDescriptor",
	"ClientGrenadeDescriptor",
	"ClientMissileDescriptor",
	"ClientScriptFiringShotDescriptor",
	
	# .pef : 
	"ProjectileImpactEffectDescriptor",
	
	# .cam :
	"FPSCamera",
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
	"WheelEffectsDescriptor",
	
	# .wpn
	"SoldierWeaponDescriptor",
	"SoldierAimingControllerDescriptor",
	"WeaponFiringDescriptor",
	
	# Found on Game Server
	"ServerBulletDescriptor",
	"ServerCapturePointDescriptor",
	"ServerEntryDescriptor",
	"ServerMissileDescriptor",
	"ServerGrenadeDescriptor",
	"ServerEntryDescriptor",
	"ServerExplosionPackDescriptor",
	"ServerExplosionPackDetonatorDescriptor",
	"ServerObjectDescriptor",
	"ServerPickupWrapperDescriptor",
	"ServerScriptFiringShotDescriptor",
	"ServerSoldierSpawnGroupDescriptor",
	"ServerSoldierSpawnPointDescriptor",
	"ServerSpawnMarkerDescriptor",
	"ServerSpectateCameraDescriptor",
	"ServerTriggerZoneDescriptor",
	"ServerVehicleSpawnPointDescriptor",
	
	"EntryDescriptor",
	"WeaponDescriptor",
	"PhysicsBuoyancyForceDescriptor",
	"PhysicsWingForceDescriptor",
	"WaterEffectDescriptor",
	"ObjectDescriptor",
	"BulletDescriptor",
	"DamageZoneDescriptor",
	"ControllableDescriptor"
]

def export_cat_resource(input_cat_filepath, output_files_path):
	## Create directories if they are missing
	os.makedirs(output_files_path, exist_ok=True)
	
	# Create a regex pattern with all class names, including optional "@" in front
	pattern_string = rb'|'.join(
		re.escape(classname.encode('ascii')) for classname in RESOURCE_OBJECT_TYPES
	)
	
	# Full pattern
	pattern = re.compile(
		rb'@?(' + pattern_string + rb')' # Class names
		rb'\x20'                         # Space
		rb'([^\x20\r\n\x00]+)'           # File path (matches any character except space, newline, and null byte)
		rb'\x20*'                        # Zero or more spaces
		rb'\x0D\x0A'                     # \r\n
	)

	with open(input_cat_filepath, 'rb') as f_cat:
		content = f_cat.read()
		
		if(content[0:4].decode("ascii") == "PZFB"):
			content = zlib.decompress(content[0x10:])
		
		matches = list(pattern.finditer(content))
		results = []
		
		for i, match in enumerate(matches):
			classname = match.group(1).decode('ascii')
			file_path = match.group(2).decode('ascii')
			patched_file_path = modify_file_path(file_path)
			
			offset = match.start()
			next_offset = matches[i + 1].start() if i + 1 < len(matches) else len(content)
			
			## Debug
			print("===============================")
			print(f'classname = "{classname}"')
			print(f'file_path = "{file_path}"')
			print(f'patched_file_path = "{patched_file_path}"')
			print(f'offset = {offset}')
			print(f'next_offset = {next_offset}')
			
			create_file(output_files_path + "/" + patched_file_path, content[offset:next_offset])
