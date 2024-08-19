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
class Mesh:
	class_name: str = ""
	resource_name: str = ""
	
@dataclass
class Component:
	resource_name: str = ""
	class_name: str = ""
	version: int = 1
	unknown_1_4: str = ""
	
	meshs: List[Mesh] = field(default_factory=list)
	
	rigidBodyDescriptor: str = ""
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

def export_level_txt(input_file_path, output_file_path):
	level_txt = LevelTxt()
	
	## read Static Geometry
	with open(input_file_path, 'rb') as f_txt:
		magic_code = f_txt.read(16)
		components_length = struct.unpack('<I', f_txt.read(4))[0]
		
		for i in range(components_length):
			component = Component()
			
			resource_name_length = struct.unpack('<I', f_txt.read(4))[0]
			component.resource_name = f_txt.read(resource_name_length).decode("ascii")
			
			class_name_length = struct.unpack('<I', f_txt.read(4))[0]
			component.class_name = f_txt.read(class_name_length).decode("ascii")
			
			if component.class_name != "SkyWrapperDescriptor":
				component.version = struct.unpack('<I', f_txt.read(4))[0]
				
				component.unknown_1_4 = f_txt.read(5).hex()	
			
			meshs_total = struct.unpack('<I', f_txt.read(4))[0]
			
			for j in range(meshs_total):
				mesh = Mesh()
				
				if component.class_name != "SkyWrapperDescriptor":
					mesh_class_name_length = struct.unpack('<I', f_txt.read(4))[0]
					mesh.class_name = f_txt.read(mesh_class_name_length).decode("ascii")
				
				mesh_resource_name_length = struct.unpack('<I', f_txt.read(4))[0]
				mesh.resource_name = f_txt.read(mesh_resource_name_length).decode("ascii")
				
				component.meshs.append(mesh)
				
			if component.class_name != "SkyWrapperDescriptor":
				rigidBodyDescriptor_length = struct.unpack('<I', f_txt.read(4))[0]
				component.rigidBodyDescriptor = f_txt.read(rigidBodyDescriptor_length).decode("ascii")
			
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
		json.dump(level_txt, f_json, cls=CustomEncoder)

def import_level_txt(input_file_path, output_file_path):
	with open(input_file_path, 'r') as f_json:
		with open(output_file_path, 'wb') as f_txt:
			static_geometry = json.load(f_json)
			
			components = static_geometry["components"]
			
			f_txt.write("Binary        \r\n".encode("ascii"))
			f_txt.write(struct.pack("<I", len(components)))
			
			for component in components:
				resource_name = component["resource_name"]
				f_txt.write(struct.pack("<I", len(resource_name)))
				f_txt.write(resource_name.encode("ascii"))
				
				class_name = component["class_name"]
				f_txt.write(struct.pack("<I", len(class_name)))
				f_txt.write(class_name.encode("ascii"))
				
				if class_name != "SkyWrapperDescriptor":
					f_txt.write(struct.pack("<I", component["version"]))
					
					f_txt.write(bytes.fromhex(component["unknown_1_4"]))
				
				## Meshs
				meshs = component["meshs"]
				f_txt.write(struct.pack("<I", len(meshs)))
				
				for mesh in meshs:
					if class_name != "SkyWrapperDescriptor":
						mesh_class_name = mesh["class_name"]
						f_txt.write(struct.pack("<I", len(mesh_class_name)))
						f_txt.write(mesh_class_name.encode("ascii"))
					
					resource_name = mesh["resource_name"]
					f_txt.write(struct.pack("<I", len(resource_name)))
					f_txt.write(resource_name.encode("ascii"))
				
				if class_name != "SkyWrapperDescriptor":
					rigidBodyDescriptor = component["rigidBodyDescriptor"]
					f_txt.write(struct.pack("<I", len(rigidBodyDescriptor)))
					f_txt.write(rigidBodyDescriptor.encode("ascii"))
					
					f_txt.write(bytes.fromhex(component["unknown_1_6"]))
				
				## Instances
				instances = component["instances"]
				f_txt.write(struct.pack("<I", len(instances)))
				
				for instance in instances:
					## Position
					f_txt.write(struct.pack("<3f", *instance["pos"]))
					
					## Rotation
					f_txt.write(struct.pack("<3f", *instance["rot"]))
