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

@dataclass
class Model:
	type: str = ""
	name: str = ""
	
@dataclass
class Component:
	unknown_1_1: str = ""
	unknown_1_2: str = ""
	unknown_1_3: int = 0
	unknown_1_4: str = ""
	
	models: List[Model] = field(default_factory=list)
	
	unknown_1_5: str = ""
	unknown_1_6: str = ""
	
	instances: List[TransformData] = field(default_factory=list)

@dataclass
class LevelTxt:
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

def extract_level_txt(input_file_path, output_file_path):
	level_txt = LevelTxt()
	
	## read Static Geometry
	with open(input_file_path, 'rb') as f_txt:
		magic_code = f_txt.read(16)
		components_length = struct.unpack('<I', f_txt.read(4))[0]
		
		for i in range(components_length):
			component = Component()
			
			unknown_1_1_length = struct.unpack('<I', f_txt.read(4))[0]
			component.unknown_1_1 = f_txt.read(unknown_1_1_length).decode("ascii")
			
			unknown_1_2_length = struct.unpack('<I', f_txt.read(4))[0]
			component.unknown_1_2 = f_txt.read(unknown_1_2_length).decode("ascii")
			
			if component.unknown_1_2 != "SkyWrapperDescriptor":
				component.unknown_1_3 = struct.unpack('<I', f_txt.read(4))[0]
				
				component.unknown_1_4 = f_txt.read(5).hex()	
			
			models_total = struct.unpack('<I', f_txt.read(4))[0]
			
			for j in range(models_total):
				model = Model()
				
				if component.unknown_1_2 != "SkyWrapperDescriptor":
					model_type_length = struct.unpack('<I', f_txt.read(4))[0]
					model.type = f_txt.read(model_type_length).decode("ascii")
				
				model_length = struct.unpack('<I', f_txt.read(4))[0]
				model.name = f_txt.read(model_length).decode("ascii")
				
				component.models.append(model)
				
			if component.unknown_1_2 != "SkyWrapperDescriptor":
				unknown_1_5_length = struct.unpack('<I', f_txt.read(4))[0]
				component.unknown_1_5 = f_txt.read(unknown_1_5_length).decode("ascii")
			
				component.unknown_1_6 = f_txt.read(4).hex()
			
			## Instances
			instances_length = struct.unpack('<I', f_txt.read(4))[0]

			for j in range(instances_length):
				transform = TransformData()
				
				transform.pos = list(struct.unpack('<3f', f_txt.read(0xC)))
				transform.rot = list(struct.unpack('<3f', f_txt.read(0xC)))
				
				component.instances.append(transform)
		
			level_txt.components.append(component)
				
	## Write Static Geometry
	with open(output_file_path, 'w') as f_json:
		json.dump(level_txt, f_json, cls=CustomEncoder, indent=4)

def import_level_txt(input_file_path, output_file_path):
	with open(input_file_path, 'r') as f_json:
		with open(output_file_path, 'wb') as f_txt:
			static_geometry = json.load(f_json)
			
			components = static_geometry["components"]
			
			f_txt.write("Binary        \r\n".encode("ascii"))
			f_txt.write(struct.pack("<I", len(components)))
			
			for component in components:
				unknown_1_1 = component["unknown_1_1"]
				f_txt.write(struct.pack("<I", len(unknown_1_1)))
				f_txt.write(unknown_1_1.encode("ascii"))
				
				unknown_1_2 = component["unknown_1_2"]
				f_txt.write(struct.pack("<I", len(unknown_1_2)))
				f_txt.write(unknown_1_2.encode("ascii"))
				
				if unknown_1_2 != "SkyWrapperDescriptor":
					f_txt.write(struct.pack("<I", component["unknown_1_3"]))
					
					f_txt.write(bytes.fromhex(component["unknown_1_4"]))
				
				## Models
				models = component["models"]
				f_txt.write(struct.pack("<I", len(models)))
				
				for model in models:
					if unknown_1_2 != "SkyWrapperDescriptor":
						model_type = model["type"]
						f_txt.write(struct.pack("<I", len(model_type)))
						f_txt.write(model_type.encode("ascii"))
					
					model_name = model["name"]
					f_txt.write(struct.pack("<I", len(model_name)))
					f_txt.write(model_name.encode("ascii"))
				
				if unknown_1_2 != "SkyWrapperDescriptor":
					unknown_1_5 = component["unknown_1_5"]
					f_txt.write(struct.pack("<I", len(unknown_1_5)))
					f_txt.write(unknown_1_5.encode("ascii"))
					
					f_txt.write(bytes.fromhex(component["unknown_1_6"]))
				
				## Instances
				instances = component["instances"]
				f_txt.write(struct.pack("<I", len(instances)))
				
				for instance in instances:
					## Position
					f_txt.write(struct.pack("<3f", *instance["pos"]))
					
					## Rotation
					f_txt.write(struct.pack("<3f", *instance["rot"]))
