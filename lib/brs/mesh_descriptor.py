import os
import struct
import json
import math
from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List

@dataclass
class EffectDescriptor:
	version: int = 0
	class_name: str = ""
	file_path: str = ""
	unknown_1: str = ""

@dataclass
class CollisionDescriptor:
	class_name: str = ""
	file_path: str = ""

@dataclass
class Model:
	class_name: str = ""
	file_path: str = ""

@dataclass
class Event:
	name: str = ""
	unknown: str = ""
	sound: str = ""

@dataclass
class MeshDescriptor:
	class_name_1: str = ""
	file_path_1: str = ""
	version: int = 0
	
	effect_descriptors: List[EffectDescriptor] = field(default_factory=list)
	
	animation: str = ""
	unknown_1_3_1: int = 0
	unknown_1_3_2: str = ""
	unknown_1_4: str = ""
	
	PrimaryCollisions: List[CollisionDescriptor] = field(default_factory=list)
	SecondaryCollisions: List[CollisionDescriptor] = field(default_factory=list)
	
	unknown_1_7: int = 0
	
	models: List[Model] = field(default_factory=list)
	
	events: List[Event] = field(default_factory=list)
	
	unknown_1_9: int = 0
	unknown_1_10: str = ""
	unknown_1_11: str = ""

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

def read_cat_file_start(f_brs):
	data = ""
	
	## Keep iteration 16 bytes until we reach the end
	while(not data.endswith("\r\n")):
		data += f_brs.read(1).decode("ascii")
	
	## Remove spaces and enters at the end and split it by space.
	data = data.strip().split()
	
	return data[0], data[1]

def export_mesh_descriptor(input_file_path, output_file_path):
	mesh_descriptor = MeshDescriptor()
	
	## read Static Geometry
	with open(input_file_path, 'rb') as f_brs:
		mesh_descriptor.class_name_1, mesh_descriptor.file_path_1 = read_cat_file_start(f_brs)
		
		if(mesh_descriptor.class_name_1 != "MeshDescriptor" and mesh_descriptor.class_name_1 != "@MeshDescriptor"):
			return
		
		mesh_descriptor.version = struct.unpack('<I', f_brs.read(4))[0]
		print("version = {}".format(mesh_descriptor.version))
		
		## Effect Descriptors
		effect_descriptors_total = struct.unpack('<I', f_brs.read(4))[0]
		print("effect_descriptors_total = {}".format(effect_descriptors_total))
		for i in range(effect_descriptors_total):
			print("EffectDescriptor {}:".format(i))
			
			effect_descriptor = EffectDescriptor()
			
			effect_descriptor.version = struct.unpack('<I', f_brs.read(4))[0]
			
			print("	version = {}".format(effect_descriptor.version))
			
			class_name_length = struct.unpack('<I', f_brs.read(4))[0]
			effect_descriptor.class_name = f_brs.read(class_name_length).decode("ascii")
			
			print("	class_name_length = {}".format(class_name_length))
			print("	class_name = {}".format(effect_descriptor.class_name))
			
			file_path_length = struct.unpack('<I', f_brs.read(4))[0]
			effect_descriptor.file_path = f_brs.read(file_path_length).decode("ascii")
			
			print("	file_path_length = {}".format(file_path_length))
			print("	file_path = {}".format(effect_descriptor.file_path))
			
			effect_descriptor.unknown_1 = f_brs.read(0x30).hex()
			
			print("	unknown_1 = 0x{}".format(effect_descriptor.unknown_1))
			
			mesh_descriptor.effect_descriptors.append(effect_descriptor)
		
		animation_length = struct.unpack('<I', f_brs.read(4))[0]
		mesh_descriptor.animation = f_brs.read(animation_length).decode("ascii")
		
		print("animation_length = {}".format(animation_length))
		print("animation = {}".format(mesh_descriptor.animation))
		
		mesh_descriptor.unknown_1_3_1 = struct.unpack('<I', f_brs.read(4))[0]
		mesh_descriptor.unknown_1_3_2 = f_brs.read(mesh_descriptor.unknown_1_3_1 * 4).hex()
		mesh_descriptor.unknown_1_4 = f_brs.read(1).hex()
		
		print("unknown_1_3_1 = {}".format(mesh_descriptor.unknown_1_3_1))
		print("unknown_1_3_2 = {}".format(mesh_descriptor.unknown_1_3_2))
		print("unknown_1_4 = 0x{}".format(mesh_descriptor.unknown_1_4))
		
		## Primary Collisions
		PrimaryCollisions_total = struct.unpack('<I', f_brs.read(4))[0]
		print("PrimaryCollisions_total = {}".format(PrimaryCollisions_total))
		for i in range(PrimaryCollisions_total):
			print("CollisionDescriptor {}:".format(i))
			
			collision_descriptor = CollisionDescriptor()
			
			class_name_length = struct.unpack('<I', f_brs.read(4))[0]
			collision_descriptor.class_name = f_brs.read(class_name_length).decode("ascii")
			
			print("	class_name_length = {}".format(class_name_length))
			print("	class_name = {}".format(collision_descriptor.class_name))
			
			file_path_length = struct.unpack('<I', f_brs.read(4))[0]
			collision_descriptor.file_path = f_brs.read(file_path_length).decode("ascii")
			
			print("	file_path_length = {}".format(file_path_length))
			print("	file_path = {}".format(collision_descriptor.file_path))
			
			mesh_descriptor.PrimaryCollisions.append(collision_descriptor)
		
		## Secondary Collisions
		SecondaryCollisions_total = struct.unpack('<I', f_brs.read(4))[0]
		print("SecondaryCollisions_total = {}".format(SecondaryCollisions_total))
		for i in range(SecondaryCollisions_total):
			print("CollisionDescriptor {}:".format(i))
			
			collision_descriptor = CollisionDescriptor()
			
			class_name_length = struct.unpack('<I', f_brs.read(4))[0]
			collision_descriptor.class_name = f_brs.read(class_name_length).decode("ascii")
			
			print("	class_name_length = {}".format(class_name_length))
			print("	class_name = {}".format(collision_descriptor.class_name))
			
			file_path_length = struct.unpack('<I', f_brs.read(4))[0]
			collision_descriptor.file_path = f_brs.read(file_path_length).decode("ascii")
			
			print("	file_path_length = {}".format(file_path_length))
			print("	file_path = {}".format(collision_descriptor.file_path))
			
			mesh_descriptor.SecondaryCollisions.append(collision_descriptor)
		
		mesh_descriptor.unknown_1_7 = struct.unpack('<I', f_brs.read(4))[0]
		print("unknown_1_7 = {}".format(mesh_descriptor.unknown_1_7))
		
		## Models
		models_total = struct.unpack('<I', f_brs.read(4))[0]
		print("models_total = {}".format(models_total))
		for i in range(models_total):
			print("Model {}:".format(i))
			model = Model()
			
			class_name_length = struct.unpack('<I', f_brs.read(4))[0]
			model.class_name = f_brs.read(class_name_length).decode("ascii")
			
			print("	class_name = {}".format(model.class_name))
			
			file_path_length = struct.unpack('<I', f_brs.read(4))[0]
			model.file_path = f_brs.read(file_path_length).decode("ascii")
			
			print("	file_path = {}".format(model.file_path))
			
			mesh_descriptor.models.append(model)
		
		events_total = struct.unpack('<I', f_brs.read(4))[0]
		print("events_total = {}".format(events_total))
		for i in range(events_total):
			print("Event {}:".format(i))
			event = Event()
			
			name_length = struct.unpack('<I', f_brs.read(4))[0]
			event.name = f_brs.read(name_length).decode("ascii")
			
			print("	name = {}".format(event.name))
			
			event.unknown = f_brs.read(0xC).hex()
			
			print("	unknown = {}".format(event.unknown))
			
			sound_length = struct.unpack('<I', f_brs.read(4))[0]
			event.sound = f_brs.read(sound_length).decode("ascii")
			
			print("	sound = {}".format(event.sound))
			
			mesh_descriptor.events.append(event)
		
		mesh_descriptor.unknown_1_9 = f_brs.read(9).hex()
		
		print("unknown_1_9 = {}".format(mesh_descriptor.unknown_1_9))
		
		unknown_1_10_length = struct.unpack('<I', f_brs.read(4))[0]
		mesh_descriptor.unknown_1_10 = f_brs.read(unknown_1_10_length).decode("ascii")
		
		print("unknown_1_10 = {}".format(mesh_descriptor.unknown_1_10))
		
		## Emptry space: Can be nothing, "00" or "0D0A"
		mesh_descriptor.unknown_1_11 = f_brs.read(2).hex()
		
		print("unknown_1_11 = {}".format(mesh_descriptor.unknown_1_11))
			
		current_position = f_brs.tell()
		f_brs.seek(0, os.SEEK_END)
		file_length = f_brs.tell()
		f_brs.seek(current_position)
		
		if(current_position != file_length):
			print("current_position, file_length = {}, {}".format(current_position, file_length))
		
	## Write Static Geometry
	with open(output_file_path, 'w') as f_json:
		json.dump(mesh_descriptor, f_json, cls=CustomEncoder, indent=4)
	
def import_mesh_descriptor(input_file_path, output_file_path):
	with open(input_file_path, 'r') as f_json:
		with open(output_file_path, 'wb') as f_brs:
			mesh_descriptor = json.load(f_json)
			
			f_brs.write(mesh_descriptor["class_name_1"].encode("ascii"))
			f_brs.write(b'\x20')
			f_brs.write(mesh_descriptor["file_path_1"].encode("ascii"))
			f_brs.write(b'\x0D\x0A')
			
			f_brs.write(struct.pack("<I", mesh_descriptor["unknown_1_1"]))
			f_brs.write(struct.pack("<I", mesh_descriptor["unknown_1_2"]))
			
			unknown_1_3 = mesh_descriptor["unknown_1_3"]
			f_brs.write(struct.pack("<I", len(unknown_1_3)))
			f_brs.write(unknown_1_3.encode("ascii"))
			
			f_brs.write(bytes.fromhex(mesh_descriptor["unknown_1_4"]))
			f_brs.write(struct.pack("<I", mesh_descriptor["unknown_1_5"]))
			
			class_name_3 = mesh_descriptor["class_name_3"]
			f_brs.write(struct.pack("<I", len(class_name_3)))
			f_brs.write(class_name_3.encode("ascii"))
			
			file_path_3 = mesh_descriptor["file_path_3"]
			f_brs.write(struct.pack("<I", len(file_path_3)))
			f_brs.write(file_path_3.encode("ascii"))
			
			f_brs.write(struct.pack("<I", mesh_descriptor["unknown_1_6"]))
			
			class_name_4 = mesh_descriptor["class_name_4"]
			f_brs.write(struct.pack("<I", len(class_name_4)))
			f_brs.write(class_name_4.encode("ascii"))
			
			file_path_4 = mesh_descriptor["file_path_4"]
			f_brs.write(struct.pack("<I", len(file_path_4)))
			f_brs.write(file_path_4.encode("ascii"))
			
			f_brs.write(struct.pack("<I", mesh_descriptor["unknown_1_7"]))
			f_brs.write(struct.pack("<I", mesh_descriptor["unknown_1_8"]))
			
			class_name_5 = mesh_descriptor["class_name_5"]
			f_brs.write(struct.pack("<I", len(class_name_5)))
			f_brs.write(class_name_5.encode("ascii"))
			
			file_path_5 = mesh_descriptor["file_path_5"]
			f_brs.write(struct.pack("<I", len(file_path_5)))
			f_brs.write(file_path_5.encode("ascii"))
			
			f_brs.write(bytes.fromhex(mesh_descriptor["unknown_1_9"]))
			
			unknown_1_10 = mesh_descriptor["unknown_1_10"]
			f_brs.write(struct.pack("<I", len(unknown_1_10)))
			f_brs.write(unknown_1_10.encode("ascii"))
			
			f_brs.write(bytes.fromhex(mesh_descriptor["unknown_1_11"]))