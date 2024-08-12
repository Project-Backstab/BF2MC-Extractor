#!/bin/env python3

import os
import json
import re
import binascii

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

"""
def find_new_line_positions(data):
	positions = []
	start = 0
	
	while True:
		position = data.find(b'\x0D\x0A', start)
		if position == -1:
			break
		positions.append(position)
		start = position + len(b'\x0D\x0A')
	
	return positions

def find_objects(data):
	objects = []

	## Find and iterate through 0x0d0a bytes
	new_line_positions = find_new_line_positions(data)
	for new_line_pos in new_line_positions:
		value = ""
		
		## Read ascii characters
		offset = new_line_pos - 1
		while(offset >= 0 and (data[offset] >= 0x20 and data[offset] <= 0x7E)):
			value = chr(data[offset]) + value
			offset -= 1
		
		## remove spaces on begin en ending and split it appart
		obj_prop = value.strip().split(" ")
		
		## Find known object types and patch
		for resource_object in RESOURCE_OBJECT_TYPES:
			if(obj_prop[0].endswith(resource_object)):
				obj_prop[0] = resource_object
				continue
		
		## check object properties
		if(len(obj_prop) != 2 or obj_prop[0] not in RESOURCE_OBJECT_TYPES):
			continue
		
		space = len(value) - len(value.rstrip())
		position = new_line_pos - len(obj_prop[0]) - 1 - len(obj_prop[1]) - space
		
		## Save object found
		objects.append({
			"position": position,
			"object_type": obj_prop[0],
			"file_path": obj_prop[1],
			"space": space,
			"ref": [],
			"strings": [],
			"sux": []
		})

	return objects

def find_objects_data(objects, data):
	for i in range(len(objects)):
		## Get object data 
		begin = objects[i]["position"] + len(objects[i]["object_type"]) + 1 + len(objects[i]["file_path"]) + objects[i]["space"] + 2
		
		if(i != len(objects) - 1):
			end = objects[i+1]["position"]
			objects[i]["data"] = data[begin:end]
		else:
			objects[i]["data"] = data[begin:]
	
	return objects

def find_reference(objects):
	for i in range(len(objects)):
		for j in range(len(objects)):
			object_type = objects[j]["object_type"]
			file_path = objects[j]["file_path"]
			
			find_object = len(object_type).to_bytes(4, byteorder='little') + object_type.encode('ascii') + len(file_path).to_bytes(4, byteorder='little') + file_path.encode('ascii')
			position = objects[i]["data"].find(find_object, 0)
			
			if(position != -1):
				objects[i]["ref"].append({
					"object_type": object_type,
					"file_path": file_path,
				})
			else:
				find_object = len(file_path).to_bytes(4, byteorder='little') + file_path.encode('ascii')
				position = objects[i]["data"].find(find_object, 0)
				
				if(position != -1):
					objects[i]["ref"].append({
						"file_path": file_path,
					})
	
	return objects

def find_strings(objects):
	for i in range(len(objects)):
		obj_data = objects[i]["data"]
		
		for j in range(len(obj_data) - 4):
			length = int.from_bytes(obj_data[j:j+4], byteorder='little')
			string = ""
			
			if(length > 3 and j + 4 + length < len(obj_data)):
				for k in range(length):
					offset = j + 4 + k
					
					if(obj_data[offset] >= 0x20 and obj_data[offset] <= 0x7E):
						string += chr(obj_data[offset])
						
						if(k + 1 == length):
							objects[i]["strings"].append(string)
							j += 4 + length
					else:
						break
	return objects

def find_sux(objects):
	for i in range(len(objects)):
		obj_data = objects[i]["data"]
		start = 0
		
		while True:
			position = obj_data.find(b'\x2E\x73\x75\x78', start)
			
			if position == -1:
				break
			
			filename = ".sux"
			
			offset = position - 1
			while(offset >= 0 and (obj_data[offset] >= 0x20 and obj_data[offset] <= 0x7E)):
				filename = chr(obj_data[offset]) + filename
				offset -= 1
			
			objects[i]["sux"].append(filename)
			
			start = position + len(b'\x2E\x73\x75\x78')
			
	return objects

def scan_cat_resource(input_cat_filepath, output_files_path):
	## Create directories if they are missing
	os.makedirs(output_files_path, exist_ok=True)
	
	## Read cat file
	with open(input_cat_filepath, "rb") as f_cat:
		with open(output_files_path + "files.txt", "w") as f_files:
			data = f_cat.read()
			objects = []
			
			## Find and iterate through 0x0d0a bytes
			new_line_positions = find_new_line_positions(data)
			for new_line_pos in new_line_positions:
				value = ""
				
				## Read ascii characters
				j = new_line_pos - 1
				while(j >= 0 and (data[j] >= 0x20 and data[j] <= 0x7E)):
					value = chr(data[j]) + value
					j -= 1
				
				## remove spaces on begin en ending and split it appart
				obj_prop = value.strip().split(" ")
				
				## Find known object types and patch
				for resource_object in RESOURCE_OBJECT_TYPES:
					if(obj_prop[0].endswith(resource_object)):
						obj_prop[0] = resource_object
						continue
				
				## check values found has missing properties
				if(	len(obj_prop) != 2 or
					len(obj_prop[0]) < 5 or
					len(obj_prop[1]) < 5 or
					obj_prop[0] in RESOURCE_OBJECT_TYPES or
					obj_prop[0] == "beginElement" or
					obj_prop[0] == "relativePosition"):
					continue
				
				## Save object properties
				objects.append(obj_prop)
			
			## Display objects that has not been declaired yet in the RESOURCE_OBJECT_TYPES
			for option in objects:
				print(option)


def export_cat_resource(input_cat_filepath, output_json_filepath):
	## Read cat file
	with open(input_cat_filepath, "rb") as f_cat:
		with open(output_json_filepath, "w") as f_json:
			data = f_cat.read()
			
			objects = find_objects(data)
			objects = find_objects_data(objects, data)
			objects = find_reference(objects)
			objects = find_strings(objects)
			objects = find_sux(objects)
			
			## Convert data
			for i in range(len(objects)):
				## Save data in array
				obj_data = objects[i]["data"]
				
				objects[i]["data"] = []
				#for j in range(0, len(obj_data), 16):
				#	objects[i]["data"].append(' '.join(f'{byte:02X}' for byte in obj_data[j:j+16]))
				objects[i]["position"] = hex(objects[i]["position"])
			
			f_json.write(json.dumps(objects, indent=4))
"""

"""
	Convert file path to new one to avoid strange symboles:
	
	Example:
		Objects/Weapons/AC/Bag/Bag.sgf:Render_Ac_OpsKit
		output/Objects/Weapons/AC/Bag/Bag.Render_Ac_OpsKit.sgf
"""
def modify_file_path(file_path):
	## fix: windows slashes
	new_file_path = file_path.replace("\\", "/")

	## Fix: capital letter cases that caused trouble extracting.
	new_file_path = new_file_path.replace("/vehicles/", "/Vehicles/")
	new_file_path = new_file_path.replace("/Ac/", "/AC/")
	new_file_path = new_file_path.replace("/Ac_Pickup/", "/AC_Pickup/")
	new_file_path = new_file_path.replace("/US_apache/", "/US_Apache/")
	new_file_path = new_file_path.replace("/Ch/", "/CH/")
	new_file_path = new_file_path.replace("/Eu/", "/EU/")
	new_file_path = new_file_path.replace("/SMAWrocketlauncher/", "/SMAWRocketLauncher/")
	new_file_path = new_file_path.replace("SMAWrocketlauncher", "SMAWRocketLauncher2")
	new_file_path = new_file_path.replace("/L85A2Assaultrifle/", "/L85A2AssaultRifle/")
	new_file_path = new_file_path.replace("/US_Lav/", "/US_LAV/")
	
	# Split the path on the last occurrence of ":"
	path_parts = new_file_path.rsplit(':', 1)
	
	if len(path_parts) != 2:
		# If the path doesn't contain ":", return it unchanged
		return new_file_path

	path_before_colon = path_parts[0]
	path_after_colon = path_parts[1]

	# Split the path_before_colon on the last occurrence of "."
	path_parts_before_dot = path_before_colon.rsplit('.', 1)
	if len(path_parts_before_dot) != 2:
		# If the path_before_colon doesn't contain ".", return it unchanged
		return new_file_path

	base_path = path_parts_before_dot[0]
	extension = path_parts_before_dot[1]

	# Construct the new path
	new_file_path = f"{base_path}.{path_after_colon}.{extension}"
	
	return new_file_path

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
		
		matches = list(pattern.finditer(content))
		results = []
		
		for i, match in enumerate(matches):
			classname = match.group(1).decode('ascii')
			file_path = match.group(2).decode('ascii')
			patched_file_path = modify_file_path(file_path)
			
			offset = match.start()
			next_offset = matches[i + 1].start() if i + 1 < len(matches) else len(content)
			
			## Debug
			#print("===============================")
			#print(f'classname = "{classname}"')
			#print(f'file_path = "{file_path}"')
			#print(f'patched_file_path = "{patched_file_path}"')
			#print(f'offset = {offset}')
			#print(f'next_offset = {next_offset}')
			
			create_file(output_files_path + "/" + patched_file_path, content[offset:next_offset])
