#!/bin/env python3

import os
import json
import re
import binascii
import zlib

from lib.functions import create_file, modify_file_path

from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List

@dataclass
class FileInfo:
	class_name: str = ""
	file_path: str = ""
	file_path_patch: str = ""
	file_path_space: int = 0
	data_offset: int = 0

@dataclass
class Cat:
	zlib: str = ""
	file_infos: List[FileInfo] = field(default_factory=list)

def clean_nan(obj):
    if isinstance(obj, float):
        return None if math.isnan(obj) else obj
    elif isinstance(obj, list):
        return [clean_nan(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif is_dataclass(obj):
        return clean_nan(asdict(obj))
    return obj

class CustomEncoder(json.JSONEncoder):
	def default(self, obj):
		if is_dataclass(obj):
			return clean_nan(asdict(obj))
		return super().default(obj)


FILE_EXTENSIONS = [
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

CLASS_NAMES = [
	# .brs : Serialised C++ Classes
	"CameraDescriptor",
	"ChaseCamera",
	"ComponentWeaponDescriptor",
	"DebreeDescriptor",
	"EntryInputActionMap",
	"GameplaySoundDescriptor",
	"LocatorDescriptor",
	"LockingComponentDescriptor",
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
	"ControllableDescriptor",
	
	# Fix: else he cant find ProjectileImpactEffectDescriptor in files
	"EffectDescriptor",
	"MeshDescriptor",
]

def export_cat_resource(input_cat_filepath, output_files_path):
	## Create directories if they are missing
	os.makedirs(output_files_path, exist_ok=True)
	
	pattern = re.compile(
		rb'\x20'               # One space at the beginning
		rb'([!-~]{5,})'        # File path with 5 or more non-space ASCII characters
		rb'(\x20*)'              # Zero or more spaces
		rb'\x0D\x0A'           # Ends with \r\n
	)
	
	cat = Cat()
	
	with open(input_cat_filepath, 'rb') as f_cat:
		content = f_cat.read()
		
		if(content[0:4].decode("ascii") == "PZFB"):
			cat.zlib = content[:0x10].hex()
			content = zlib.decompress(content[0x10:])
			
			## Debug
			#with open(output_files_path + "data.zlib", 'wb') as f_zlib:
			#	f_zlib.write(content)
		
		## Execute regulare expression
		matches = list(pattern.finditer(content))
		
		## Check regulaire expression results
		for i, match in enumerate(matches):
			offset = match.start()
			
			## Iterate through all class names
			for class_name in CLASS_NAMES:
				data_offset = offset - len(class_name)
				
				## Check class name is infront
				if(content[data_offset:offset] == class_name.encode('ascii')):
					file_info = FileInfo()
					
					file_info.class_name = class_name
					file_info.file_path = match.group(1).decode('ascii')
					file_info.file_path_patch = modify_file_path(file_info.file_path)
					file_info.file_path_space = len(match.group(2))
					file_info.data_offset = data_offset
					
					## Case @ infront
					if(content[data_offset-1:data_offset] == "@".encode('ascii')):
						file_info.data_offset -= 1
					
					## add file info to cat
					cat.file_infos.append(file_info)
					
					break
		
		for i, file_info in enumerate(cat.file_infos):
			end_offset = cat.file_infos[i + 1].data_offset if (i + 1 < len(cat.file_infos)) else len(content)
			
			## Get data
			data = content[file_info.data_offset:end_offset]
			
			## Create file
			create_file(output_files_path + "/" + file_info.file_path_patch, data)
		
		## Save cat file information to json
		with open(output_files_path + "cat.json", "w") as json_file:
			json.dump(cat, json_file, cls=CustomEncoder)

def import_cat_resource(input_files_path, output_cat_filepath):
	content = b''
	
	with open(input_files_path + "cat.json", 'r') as f_json:
		cat = json.load(f_json)
		
		for file_info in cat["file_infos"]:
			with open(input_files_path + file_info["file_path_patch"], 'rb') as f:
				content += f.read()
		
		## Debug
		#with open(output_cat_filepath + ".zlib", 'wb') as f_zlib:
		#	f_zlib.write(content)
		
		## Zlib compression
		if(cat["zlib"] != ""):
			content = zlib.compress(content)
			content = bytes.fromhex(cat["zlib"]) + content
		
		with open(output_cat_filepath, 'wb') as f_cat:
			f_cat.write(content)