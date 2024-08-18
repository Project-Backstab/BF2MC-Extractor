import struct
import os
import json
import math
from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List

@dataclass
class Vertex:
	position: List[float] = field(default_factory=list)
	unknown_1: str = ""
	flag: int = 0

@dataclass
class Mesh:
	material_index: int = 0
	vertices: List[Vertex] = field(default_factory=list)
	faces: List[int] = field(default_factory=list)

@dataclass
class Object:
	header: str = ""
	meshes: List[Mesh] = field(default_factory=list)

@dataclass
class Image:
	file_path: str = ""
	unknown_1: str = ""
	unknown_2: str = ""

@dataclass
class Material:
	name: str = ""
	unknown_1: str = ""
	unknown_2: str = ""
	unknown_3: str = ""
	type: str = ""
	images: List[Image] = field(default_factory=list)

@dataclass
class StaticModel:
	class_name: str = ""
	file_path: str = ""
	
	unknown_1: str = ""
	object_headers_total: int = 0
	unknown_2: str = ""
	unknown_3: str = ""
	
	materials: List[Material] = field(default_factory=list)
	objects: List[Object] = field(default_factory=list)

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

def read_string(f_sgf):
	data = f_sgf.read(4)
	
	while(data[-1] != 0x00):
		data += f_sgf.read(4)
	
	return data.rstrip(b'\x00').decode("ascii").strip()

def export_sgf(input_file_path, output_file_path):
	static_model = StaticModel()
	
	with open(input_file_path, 'rb') as f_sgf:
		static_model.class_name, static_model.file_path = read_cat_file_start(f_sgf)
		
		if(static_model.class_name != "StaticModel" and static_model.class_name != "@StaticModel"):
			return
		
		static_model.unknown_1 = f_sgf.read(4).hex()
		static_model.object_headers_total = struct.unpack('<I', f_sgf.read(4))[0]
		static_model.unknown_2 = f_sgf.read(4 * static_model.object_headers_total).hex()
		static_model.unknown_3 = f_sgf.read(4).hex()
		
		## Debug
		#print("unknown_1_1 = 0x{}".format(static_model.unknown_1))
		#print("object_headers_total = {}".format(static_model.object_headers_total))
		#print("unknown_1_2 = 0x{}".format(static_model.unknown_2))
		#print("unknown_1_3 = 0x{}".format(static_model.unknown_3))
		
		## Materials
		materials_total = struct.unpack('<I', f_sgf.read(4))[0]
		for material_index in range(materials_total):
			material = Material()
			
			material.name      = read_string(f_sgf)
			material.unknown_1 = read_string(f_sgf)
			material.unknown_2 = read_string(f_sgf)
			material.unknown_3 = read_string(f_sgf)
			material.type      = read_string(f_sgf)
			
			#print(f"Material {material_index}:")
			#print(f"	name      = \"{material.name}\"")
			#print(f"	unknown_1 = \"{material.unknown_1}\"")
			#print(f"	unknown_2 = \"{material.unknown_2}\"")
			#print(f"	unknown_3 = \"{material.unknown_3}\"")
			#print(f"	type      = \"{material.type}\"")
			
			## Images
			images_total = struct.unpack('<I', f_sgf.read(4))[0]
			#print("	images = {}".format(images_total))
			for img_index in range(images_total):
				image = Image()
				
				image.file_path = read_string(f_sgf)
				image.unknown_1 = f_sgf.read(8).hex()
				image.unknown_2 = f_sgf.read(4).hex()
				
				#print(f"	Image {img_index}:")
				#print(f"		file_path = \"{image.file_path}\"")
				#print(f"		unknown_1 = 0x{image.unknown_1}")
				#print(f"		unknown_2 = 0x{image.unknown_2}")
				
				material.images.append(image)
			
			static_model.materials.append(material)
		
		## Get current file position to keep iterating until end of the file
		current_position = f_sgf.tell()
		f_sgf.seek(0, os.SEEK_END)
		file_length = f_sgf.tell()
		f_sgf.seek(current_position)
		
		## Objects
		object_index = 0
		next_object_header = 0
		while(current_position < file_length):
			object = Object()
			
			#print(f"Object {object_index}:")
			
			if(object_index == next_object_header):
				next_object_header += struct.unpack('<I', f_sgf.read(4))[0]
				object.header = f_sgf.read(0x34).hex()
				
				#print(f"	next_object_header = {next_object_header}")
				#print(f"	header = 0x{object.header}")
			
			## Meshes
			meshes_total = struct.unpack('<I', f_sgf.read(4))[0]
			#print(f"	meshes_total = {meshes_total}")
			
			for mesh_index in range(meshes_total):
				mesh = Mesh()
				
				mesh.material_index = struct.unpack('<I', f_sgf.read(4))[0]
				assert (mesh.material_index < materials_total), "Error: material_index < materials_total. material_index = {}".format(mesh.material_index)
				
				#print("	Mesh {}:".format(mesh_index))
				#print(f"		material_index = {mesh.material_index}")
				
				## Vertices
				total_flags = 0  ## Extra check if data is correct. Can never be higher then 3
				
				vertices_total = struct.unpack('<I', f_sgf.read(4))[0]
				#print(f"		vertices_total = {vertices_total}")
				
				for vertex_index in range(vertices_total):
					vertex = Vertex()
					
					vertex.position = list(struct.unpack('<3f', f_sgf.read(12)))
					vertex.unknown_1 = f_sgf.read(40).hex()
					vertex.flag = struct.unpack('<I', f_sgf.read(4))[0]
					
					mesh.vertices.append(vertex)
					
					#print(f"		Vertex {vertex_index}:")
					#print(f"			position  = {vertex.position}")
					#print(f"			unknown_1 = 0x{vertex.unknown_1}")
					#print(f"			flag      = {vertex.flag}")
					
					## Extra check for data integrity
					assert (vertex.flag == 1 or vertex.flag == 0), "Error: vertex.flag = {}".format(vertex.flag)
					
					if(vertex.flag == 1):
						total_flags += 1
					else:
						total_flags = 0
						
					assert (total_flags < 3), "Error: total_flags = {}".format(total_flags)
					
				## Generate faces
				for i in range(vertices_total - 2):
					if mesh.vertices[i + 2].flag == 0:
						mesh.faces.append([i, i + 1, i + 2])
						
						#mesh.faces.append([i + 2, i + 1, i])
				
				## Add mesh
				object.meshes.append(mesh)
			
			static_model.objects.append(object)
			
			object_index += 1
			current_position = f_sgf.tell()
	
	with open(output_file_path, "w") as json_file:
		json.dump(static_model, json_file, cls=CustomEncoder, indent=4)

def export_sgf_beta(input_file_path, output_file_path):
	static_model = StaticModel()
	
	with open(input_file_path, 'rb') as f_sgf:
		static_model.class_name, static_model.file_path = read_cat_file_start(f_sgf)
		
		if(static_model.class_name != "StaticModel" and static_model.class_name != "@StaticModel"):
			return
		
		static_model.object_headers_total = struct.unpack('<I', f_sgf.read(4))[0]
		static_model.unknown_2 = f_sgf.read(4 * static_model.object_headers_total).hex()
		
		## Debug
		#print("object_headers_total = {}".format(static_model.object_headers_total))
		#print("unknown_1_2 = 0x{}".format(static_model.unknown_2))
		
		## Materials
		materials_total = struct.unpack('<I', f_sgf.read(4))[0]
		for material_index in range(materials_total):
			material = Material()
			
			material.name      = read_string(f_sgf)
			material.unknown_1 = read_string(f_sgf)
			material.unknown_2 = read_string(f_sgf)
			material.unknown_3 = read_string(f_sgf)
			material.type      = read_string(f_sgf)
			
			#print(f"Material {material_index}:")
			#print(f"	name      = \"{material.name}\"")
			#print(f"	unknown_1 = \"{material.unknown_1}\"")
			#print(f"	unknown_2 = \"{material.unknown_2}\"")
			#print(f"	unknown_3 = \"{material.unknown_3}\"")
			#print(f"	type      = \"{material.type}\"")
			
			## Images
			images_total = struct.unpack('<I', f_sgf.read(4))[0]
			#print("	images = {}".format(images_total))
			
			for img_index in range(images_total):
				image = Image()
				
				image.file_path = read_string(f_sgf)
				image.unknown_1 = f_sgf.read(8).hex()
				image.unknown_2 = f_sgf.read(4).hex()
				
				#print(f"	Image {img_index}:")
				#print(f"		file_path = \"{image.file_path}\"")
				#print(f"		unknown_1 = 0x{image.unknown_1}")
				#print(f"		unknown_2 = 0x{image.unknown_2}")
				
				material.images.append(image)
			
			static_model.materials.append(material)
		
		## Get current file position to keep iterating until end of the file
		current_position = f_sgf.tell()
		f_sgf.seek(0, os.SEEK_END)
		file_length = f_sgf.tell()
		f_sgf.seek(current_position)
		
		## Objects
		object_index = 0
		next_object_header = 0
		while(current_position + 4 < file_length):
			object = Object()
			
			#print(f"Object {object_index}:")
			
			if(object_index == next_object_header):
				next_object_header += struct.unpack('<I', f_sgf.read(4))[0]
				
				#print(f"	next_object_header = {next_object_header}")
			
			## Meshes
			meshes_total = struct.unpack('<I', f_sgf.read(4))[0]
			#print(f"	meshes_total = {meshes_total}")
			
			for mesh_index in range(meshes_total):
				mesh = Mesh()
				
				mesh.material_index = struct.unpack('<I', f_sgf.read(4))[0]
				assert (mesh.material_index < materials_total), "Error: material_index < materials_total. material_index = {}".format(mesh.material_index)
				
				#print("	Mesh {}:".format(mesh_index))
				#print(f"		material_index = {mesh.material_index}")
				
				## Vertices
				total_flags = 0  ## Extra check if data is correct. Can never be higher then 3
				
				vertices_total = struct.unpack('<I', f_sgf.read(4))[0]
				#print(f"		vertices_total = {vertices_total}")
				
				for vertex_index in range(vertices_total):
					vertex = Vertex()
					
					vertex.position = list(struct.unpack('<3f', f_sgf.read(12)))
					vertex.unknown_1 = f_sgf.read(80).hex()
					vertex.flag = struct.unpack('<I', f_sgf.read(4))[0]
					
					mesh.vertices.append(vertex)
					
					#print(f"		Vertex {vertex_index}:")
					#print(f"			position  = {vertex.position}")
					#print(f"			unknown_1 = 0x{vertex.unknown_1}")
					#print(f"			flag      = {vertex.flag}")
					
					## Extra check for data integrity
					assert (vertex.flag == 1 or vertex.flag == 0), "Error: vertex.flag = {}".format(vertex.flag)
					
					if(vertex.flag == 1):
						total_flags += 1
					else:
						total_flags = 0
						
					assert (total_flags < 3), "Error: total_flags = {}".format(total_flags)
					
				## Generate faces
				for i in range(vertices_total - 2):
					if mesh.vertices[i + 2].flag == 0:
						mesh.faces.append([i, i + 1, i + 2])
						
						#mesh.faces.append([i + 2, i + 1, i])
				
				## Add mesh
				object.meshes.append(mesh)
			
			static_model.objects.append(object)
			
			object_index += 1
			current_position = f_sgf.tell()
	
	#if(current_position != file_length):
	#	print(f"current_position, file_length = {current_position}, {file_length}")
	
	with open(output_file_path, "w") as json_file:
		json.dump(static_model, json_file, cls=CustomEncoder, indent=4)

