import re
import os
import math
import json
import struct
from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List

@dataclass
class Vertex:
	data: str = ""
	x: float = 0.0
	y: float = 0.0
	z: float = 0.0

@dataclass
class Data:
	unknown_1: float = 0.0
	unknown_2: float = 0.0
	unknown_3: int = 0
	unknown_4: str = ""

@dataclass
class Grid:
	x: int = 0
	y: int = 0
	z: int = 0
	max_x: int = 0
	max_y: int = 0
	max_z: int = 0
	
	datas: List[Data] = field(default_factory=list)
	
	unknown_1: str = ""
	
	vertices: List[Vertex] = field(default_factory=list)
	faces: List[int] = field(default_factory=list)

@dataclass
class Land:
	unknown_1: int = 0
	unknown_2: int = 0
	unknown_3: int = 0
	grids: List[Grid] = field(default_factory=list)

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

def read_vertex(f_lnd, grid):
	vertex = Vertex()
				
	## Data
	data = f_lnd.read(4)
	vertex.data = data.hex()
	
	## Data x, y, z
	data_x = struct.unpack_from('<B', data[0:1])[0]
	data_y = struct.unpack_from('<H', data[1:3])[0]
	data_z = struct.unpack_from('<B', data[3:4])[0]
	
	## Vertex x, y, z
	vertex.x = (float(data_x) + grid.x)
	vertex.y = (float(data_y) / 100) + grid.y
	vertex.z = (float(data_z) + grid.z)
	
	#print("	Vertex:")
	#print(f"		data = {vertex.data}")
	#print(f"		x = {vertex.x}")
	#print(f"		y = {vertex.y}")
	#print(f"		z = {vertex.z}")
	
	return vertex

def export_pc_lnd(input_file_path, output_file_path):
	land = Land()
	
	with open(input_file_path, 'rb') as f_lnd:
		vertices_total = 1
		
		land.unknown_1 = struct.unpack('<I', f_lnd.read(4))[0]
		land.unknown_2 = struct.unpack('<I', f_lnd.read(4))[0]
		land.unknown_3 = struct.unpack('<I', f_lnd.read(4))[0]
		
		#print(f"unknown_1_1 = {land.unknown_1}")
		#print(f"unknown_1_2 = {land.unknown_2}")
		#print(f"unknown_1_3 = {land.unknown_3}")
		#print("")
		
		for i in range(1024):
			#print("Grid {}:".format(i))
			
			grid = Grid()
			
			## Grid properties
			grid.x = struct.unpack('<f', f_lnd.read(4))[0]
			grid.y = struct.unpack('<f', f_lnd.read(4))[0]
			grid.z = struct.unpack('<f', f_lnd.read(4))[0]
			grid.x_max = struct.unpack('<f', f_lnd.read(4))[0]
			grid.y_max = struct.unpack('<f', f_lnd.read(4))[0]
			grid.z_max = struct.unpack('<f', f_lnd.read(4))[0]
			
			#print(f"	x = {grid.x}")
			#print(f"	y = {grid.y}")
			#print(f"	z = {grid.z}")
			#print(f"	x_max = {grid.x_max}")
			#print(f"	y_max = {grid.y_max}")
			#print(f"	z_max = {grid.z_max}")
			#print("")
			
			## Data
			data_total = pow(struct.unpack('<I', f_lnd.read(4))[0], 2)
			for j in range(data_total):
				#print(f"	Data {j}:")
				
				data = Data()
				
				data.unknown_1 = struct.unpack('<f', f_lnd.read(4))[0]
				data.unknown_2 = struct.unpack('<f', f_lnd.read(4))[0]
				data.unknown_3 = struct.unpack('<I', f_lnd.read(4))[0]
				data.unknown_4 = f_lnd.read(4 * data.unknown_3).hex()
				
				#print(f"		unknown_1 = {data.unknown_1}")
				#print(f"		unknown_2 = {data.unknown_2}")
				#print(f"		unknown_3 = {data.unknown_3}")
				#print(f"		unknown_4 = 0x{data.unknown_4}")
				#print("")
				
				grid.datas.append(data)
			
			## Faces
			faces_total = struct.unpack('<I', f_lnd.read(4))[0]
			for j in range(0, faces_total, 3):
				x = struct.unpack('<I', f_lnd.read(4))[0]
				y = struct.unpack('<I', f_lnd.read(4))[0]
				z = struct.unpack('<I', f_lnd.read(4))[0]
				
				grid.faces.append([x, y, z])
			
			grid.unknown_1 = f_lnd.read(12).hex()
			
			#print(f"	unknown_1 = 0x{grid.unknown_1}")
				
			## Vertices
			grid_vertices_total = struct.unpack('<I', f_lnd.read(4))[0]
			for j in range(grid_vertices_total):
				#print(f"	Vertex {j}:")
				vertex = read_vertex(f_lnd, grid)
				
				grid.vertices.append(vertex)
			
			vertices_total += grid_vertices_total
			
			land.grids.append(grid)
	
	## Write Static Geometry
	with open(output_file_path, 'w') as f_json:
		json.dump(land, f_json, cls=CustomEncoder)

## Old feature
def export_pc_lnd_2_obj(input_file_path, output_file_path):
	with open(input_file_path, 'rb') as f_lnd:
		with open(output_file_path, 'w') as f_obj:
			f_obj.write("o\n")
			
			vertices_total = 1
			
			unknown_1_1 = struct.unpack('<I', f_lnd.read(4))[0]
			unknown_1_2 = struct.unpack('<I', f_lnd.read(4))[0]
			unknown_1_3 = struct.unpack('<I', f_lnd.read(4))[0]
			
			print(f"unknown_1_1 = {unknown_1_1}")
			print(f"unknown_1_2 = {unknown_1_2}")
			print(f"unknown_1_3 = {unknown_1_3}")
			print("")
			
			for i in range(1024):
				print("Grid {}:".format(i))
				
				grid_x = struct.unpack('<f', f_lnd.read(4))[0]
				grid_y = struct.unpack('<f', f_lnd.read(4))[0]
				grid_z = struct.unpack('<f', f_lnd.read(4))[0]
				grid_x_max = struct.unpack('<f', f_lnd.read(4))[0]
				grid_y_max = struct.unpack('<f', f_lnd.read(4))[0]
				grid_z_max = struct.unpack('<f', f_lnd.read(4))[0]
				
				print(f"	grid_x = {grid_x}")
				print(f"	grid_y = {grid_y}")
				print(f"	grid_z = {grid_z}")
				print(f"	grid_x_max = {grid_x_max}")
				print(f"	grid_y_max = {grid_y_max}")
				print(f"	grid_z_max = {grid_z_max}")
				print("")
				
				unknown_3_1 = struct.unpack('<I', f_lnd.read(4))[0]
				
				print(f"	unknown_3_1 = {unknown_3_1}")
				print("")
				
				for j in range(unknown_3_1 * unknown_3_1):
					print(f"	Unknown Object {j}:")
					
					unknown_4_1 = struct.unpack('<f', f_lnd.read(4))[0]
					unknown_4_2 = struct.unpack('<f', f_lnd.read(4))[0]
					unknown_4_3 = struct.unpack('<I', f_lnd.read(4))[0]
					unknown_4_4 = f_lnd.read(4 * unknown_4_3).hex()
					
					print(f"		unknown_4_1 = {unknown_4_1}")
					print(f"		unknown_4_2 = {unknown_4_2}")
					print(f"		unknown_4_3 = {unknown_4_3}")
					print(f"		unknown_4_4 = 0x{unknown_4_4}")
					print("")
				
				faces_total = struct.unpack('<I', f_lnd.read(4))[0]
				faces = []
				for j in range(0, faces_total, 3):
					x = struct.unpack('<I', f_lnd.read(4))[0]
					y = struct.unpack('<I', f_lnd.read(4))[0]
					z = struct.unpack('<I', f_lnd.read(4))[0]
					
					faces.append([vertices_total + z, vertices_total + y, vertices_total + x])
				
				unknown_5_3 = f_lnd.read(12).hex()
				
				print(f"	faces_total = {faces_total}")
				print(f"	unknown_5_3 = 0x{unknown_5_3}")
				print("")
				
				grid_vertices_total = struct.unpack('<I', f_lnd.read(4))[0]
				
				print(f"	grid_vertices_total = {grid_vertices_total}")
				print("")
				
				vertices_total += grid_vertices_total
				
				for j in range(grid_vertices_total):
					print(f"	Vertex {j}:")
					
					data_x = f_lnd.read(1)
					data_y = f_lnd.read(2)
					data_z = f_lnd.read(1)
					
					x = (float(struct.unpack_from('<B', data_x)[0]) + grid_x)
					y = (float(struct.unpack_from('<H', data_y)[0]) / 100) + grid_y
					z = (float(struct.unpack_from('<B', data_z)[0]) + grid_z)
					
					print("		data_x = 0x{}".format(data_x.hex()))
					print("		data_y = 0x{}".format(data_y.hex()))
					print("		data_z = 0x{}".format(data_z.hex()))
					
					print("		x = {}".format(x))
					print("		y = {}".format(y))
					print("		z = {}".format(z))
					print("")
					
					f_obj.write(f"v {x} {y} {z}\n")
				
				for face in faces:
					x = face[0]
					y = face[1]
					z = face[2]
					
					f_obj.write(f"f {x} {y} {z}\n")
					
			
			# Save the current position
			current_pos = f_lnd.tell()

			# Move the cursor to the end of the file to get its length
			f_lnd.seek(0, os.SEEK_END)
			file_length = f_lnd.tell()

			# Restore the cursor to its original position
			f_lnd.seek(current_pos, os.SEEK_SET)
			
			print(f"current_pos, file_length = {current_pos}, {file_length}")

