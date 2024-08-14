import os
import struct
import json
import math
from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List

@dataclass
class TransformData:
	pos: List[float] = field(default_factory=list)
	rot: List[float] = field(default_factory=list)
	unknown_2_1: str = ""

@dataclass
class Component:
	version_1: int = 1
	primaryCollision: str = ""
	secondaryCollision: str = ""
	
	version_2: int = 1
	model: str = ""
	unknown_1_1: str = ""
	unknown_1_2: str = ""
	
	instances: List[TransformData] = field(default_factory=list)

@dataclass
class StaticGeometry:
	is_client: bool = True
	components: List[Component] = field(default_factory=list)

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

def export_level_static_geometry_txt(input_file_path, output_file_path, is_client = True):
	static_geometry = StaticGeometry()
	static_geometry.is_client = is_client
	
	## read Static Geometry
	with open(input_file_path, 'rb') as f_txt:
		magic_code = f_txt.read(16)
		components_length = struct.unpack('<I', f_txt.read(4))[0]
		
		for i in range(components_length):
			component = Component()
			
			component.version_1 = struct.unpack('<I', f_txt.read(4))[0]
			
			primaryCollision_length = struct.unpack('<I', f_txt.read(4))[0]
			component.primaryCollision = f_txt.read(primaryCollision_length).decode("ascii")
			
			secondaryCollision_length = struct.unpack('<I', f_txt.read(4))[0]
			component.secondaryCollision = f_txt.read(secondaryCollision_length).decode("ascii")
			
			if(is_client):
				component.version_2 = struct.unpack('<I', f_txt.read(4))[0]
			
				model_length = struct.unpack('<I', f_txt.read(4))[0]
				component.model = f_txt.read(model_length).decode("ascii")
			
				component.unknown_1_1 = f_txt.read(4).hex()
				component.unknown_1_2 = f_txt.read(4).hex()
			
			## Instances
			instances_length = struct.unpack('<I', f_txt.read(4))[0]

			for i in range(instances_length):
				transform = TransformData()
				
				transform.pos = list(struct.unpack('<3f', f_txt.read(0xC)))
				transform.rot = list(struct.unpack('<3f', f_txt.read(0xC)))
				transform.unknown_2_1 = f_txt.read(0x4).hex()
				
				component.instances.append(transform)
		
			static_geometry.components.append(component)
				
	## Write Static Geometry
	with open(output_file_path, 'w') as f_json:
		json.dump(static_geometry, f_json, cls=CustomEncoder, indent=4)

def import_level_static_geometry_txt(input_file_path, output_file_path):
	with open(input_file_path, 'r') as f_json:
		with open(output_file_path, 'wb') as f_txt:
			static_geometry = json.load(f_json)
			
			components = static_geometry["components"]
			
			f_txt.write("Binary        \r\n".encode("ascii"))
			f_txt.write(struct.pack("<I", len(components)))
			
			for component in components:
				## Version
				f_txt.write(struct.pack("<I", component["version_1"]))
				
				primaryCollision = component["primaryCollision"]
				f_txt.write(struct.pack("<I", len(primaryCollision)))
				f_txt.write(primaryCollision.encode("ascii"))
				
				secondaryCollision = component["secondaryCollision"]
				f_txt.write(struct.pack("<I", len(secondaryCollision)))
				f_txt.write(secondaryCollision.encode("ascii"))
				
				if static_geometry["is_client"]:
					## Version
					f_txt.write(struct.pack("<I", component["version_2"]))
					
					## Model
					model = component["model"]
					f_txt.write(struct.pack("<I", len(model)))
					f_txt.write(model.encode("ascii"))
					
					## Unknown data
					f_txt.write(bytes.fromhex(component["unknown_1_1"]))
					f_txt.write(bytes.fromhex(component["unknown_1_2"]))
				
				instances = component["instances"]
				
				## Instances
				f_txt.write(struct.pack("<I", len(instances)))
				for instance in instances:
					## Position
					f_txt.write(struct.pack("<3f", *instance["pos"]))
					
					## Rotation
					f_txt.write(struct.pack("<3f", *instance["rot"]))
					
					## Unknown data
					f_txt.write(bytes.fromhex(instance["unknown_2_1"]))