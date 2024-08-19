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
	flag: bool = False
	z_check: bool = False
	unknown_2: str = ""
	
@dataclass
class Grid:
	x: int = 0
	y: int = 0
	z: int = 0
	max_x: int = 0
	max_y: int = 0
	max_z: int = 0
	
	blocks_total: int = 0
	unknown_1: str = ""
	
	vertices: List[Vertex] = field(default_factory=list)
	faces: List[int] = field(default_factory=list)
	
	unknown_2: str = ""
	
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

"""
	Calculate the area of a triangle given its vertices.

	vertices: A list of three coordinate pairs [[x1, y1], [x2, y2], [x3, y3]]
	Returns the area of the triangle.
"""
def calc_triangle_area(x1, y1, x2, y2, x3, y3):
	return 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))

def read_vertex(f_lnd, grid, data_read):
	vertex = Vertex()
	
	## Data
	data = f_lnd.read(4)
	data_read += 4
	vertex.data = data.hex()
	
	## Data x, y, z
	data_x = struct.unpack_from('<B', data[0:1])[0]
	data_y = struct.unpack_from('<H', data[2:4])[0]
	data_z = struct.unpack_from('<B', data[1:2])[0]
	
	## Vertex information
	vertex.x =  float(data_x & 0x7F) + grid.x
	vertex.y = (float(data_y) / 100) + grid.y
	vertex.z =  float(data_z)        + grid.z
	
	## Checks
	vertex.flag = (data_x & 0x80 == 0)
	vertex.z_check = (data_z <= 32)
	
	if(vertex.z_check == False):
		vertex.unknown_2 = f_lnd.read(12).hex()
		data_read += 12
	
	#print("	Vertex:")
	#print(f"		data = {vertex.data}")
	#print(f"		x = {vertex.x}")
	#print(f"		y = {vertex.y}")
	#print(f"		z = {vertex.z}")
	
	return vertex, data_read

def export_ps2_lnd(input_file_path, output_file_path):
	land = Land()
	
	with open(input_file_path, 'rb') as f_lnd:			
		land.unknown_1 = struct.unpack('<I', f_lnd.read(4))[0]
		land.unknown_2 = struct.unpack('<I', f_lnd.read(4))[0]
		land.unknown_3 = struct.unpack('<I', f_lnd.read(4))[0]
		
		#print(f"unknown_1 = {land.unknown_1}")
		#print(f"unknown_2 = {land.unknown_2}")
		#print(f"unknown_3 = {land.unknown_3}")
		#print("")
		
		for i in range(1024):
			#print(f"Grid {i}:")
			
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
			
			grid.blocks_total = struct.unpack('<I', f_lnd.read(4))[0]
			data_total = (grid.blocks_total * 0x10) + 0x10
			data_read = 0
			
			#print(f"	blocks_total = {grid.blocks_total}")
			#print(f"	data_total = {data_total}")
			
			grid.unknown_1 = f_lnd.read(0x34).hex()
			data_read += 0x34
			#print("	unknown_1 = 0x{}".format(grid.unknown_1))
			
			v1, data_read = read_vertex(f_lnd, grid, data_read)
			grid.vertices.append(v1)
			
			v2, data_read = read_vertex(f_lnd, grid, data_read)
			grid.vertices.append(v2)
			
			v3, data_read = read_vertex(f_lnd, grid, data_read)
			grid.vertices.append(v3)
			
			
			## Calculate area
			area = calc_triangle_area(v1.x, v1.z, v2.x, v2.z, v3.x, v3.z)
			
			#print("	area = {}".format(area))
			#print("")
			
			grid.faces.append([0, 1, 2])
			
			vertices_total = 3
			while(area < 1024.0):
				## Copy vertex
				v1, v2 = v2, v3
				
				## Get next vertex
				v3, data_read = read_vertex(f_lnd, grid, data_read)
				grid.vertices.append(v3)
				
				if(v3.z_check):
					## Next
					vertices_total += 1
					
					if(v3.flag):
						## Calculate new area
						area += calc_triangle_area(v1.x, v1.z, v2.x, v2.z, v3.x, v3.z)
						
						#print("	area = {}".format(area))
						#print("")
						
						grid.faces.append([vertices_total - 3, vertices_total - 2, vertices_total - 1])
				else:
					## Copy back vertex
					v2, v3 = v1, v2
			
			## Data integrity check
			assert (area == 1024.0), "Error: area = {area}"
			
			grid.unknown_2 = f_lnd.read(data_total - data_read).hex()
			#print(f"	unknown_2 = 0x{grid.unknown_2}")
			
			land.grids.append(grid)
	
	## Write Static Geometry
	with open(output_file_path, 'w') as f_json:
		json.dump(land, f_json, cls=CustomEncoder)

## Old feature
def export_ps2_lnd_2_obj(input_file_path, output_file_path):
	with open(input_file_path, 'rb') as f_lnd:
		with open(output_file_path, 'w') as f_obj:
			f_obj.write("o\n")
			
			unknown_1_1 = struct.unpack('<I', f_lnd.read(4))[0]
			unknown_1_2 = struct.unpack('<I', f_lnd.read(4))[0]
			unknown_1_3 = struct.unpack('<I', f_lnd.read(4))[0]
			
			print("unknown_1_1 = {}".format(unknown_1_1))
			print("unknown_1_2 = {}".format(unknown_1_2))
			print("unknown_1_3 = {}".format(unknown_1_3))
			print("")
			
			vertices_total = 0
			for i in range(1024):
				print("Grid {}:".format(i))
				
				grid_x = struct.unpack('<f', f_lnd.read(4))[0]
				grid_y = struct.unpack('<f', f_lnd.read(4))[0]
				grid_z = struct.unpack('<f', f_lnd.read(4))[0]
				grid_x_max = struct.unpack('<f', f_lnd.read(4))[0]
				grid_y_max = struct.unpack('<f', f_lnd.read(4))[0]
				grid_z_max = struct.unpack('<f', f_lnd.read(4))[0]
				
				print("	grid_x = {}".format(grid_x))
				print("	grid_y = {}".format(grid_y))
				print("	grid_z = {}".format(grid_z))
				print("	grid_x_max = {}".format(grid_x_max))
				print("	grid_y_max = {}".format(grid_y_max))
				print("	grid_z_max = {}".format(grid_z_max))
				
				blocks_total = struct.unpack('<I', f_lnd.read(4))[0]
				data_total = (blocks_total * 0x10) + 0x10
				data_read = 0
				
				print("	blocks_total = {}".format(blocks_total))
				print("	data_total = {}".format(data_total))
				
				unknown_2_1 = f_lnd.read(0x34).hex()
				data_read += 0x34
				print("	unknown_2_1 = 0x{}".format(unknown_2_1))
				
				faces = []
				
				## Get first triangle vertices
				x1_data = struct.unpack_from('<B', f_lnd.read(1))[0]
				x1 = (float(x1_data & 0x7F) + grid_x)
				z1 = (float(struct.unpack_from('<B', f_lnd.read(1))[0]) + grid_z)
				y1 = (float(struct.unpack_from('<H', f_lnd.read(2))[0]) / 100) + grid_y
				data_read += 4
				
				f_obj.write(f"v {x1} {y1} {z1}\n")
				
				print("	Vertex {}:")
				#print("		x_data = {}".format(x1_data & 0x80))
				print("		x = {}".format(x1))
				print("		y = {}".format(y1))
				print("		z = {}".format(z1))
				print("")
				
				x2_data = struct.unpack_from('<B', f_lnd.read(1))[0]
				x2 = (float(x2_data & 0x7F) + grid_x)
				z2 = (float(struct.unpack_from('<B', f_lnd.read(1))[0]) + grid_z)
				y2 = (float(struct.unpack_from('<H', f_lnd.read(2))[0]) / 100) + grid_y
				data_read += 4
				
				f_obj.write(f"v {x2} {y2} {z2}\n")
				
				print("	Vertex:")
				#print("		x_data = {}".format(x2_data & 0x80))
				print("		x = {}".format(x2))
				print("		y = {}".format(y2))
				print("		z = {}".format(z2))
				print("")
				
				x3_data = struct.unpack_from('<B', f_lnd.read(1))[0]
				x3 = (float(x3_data & 0x7F) + grid_x)
				z3 = (float(struct.unpack_from('<B', f_lnd.read(1))[0]) + grid_z)
				y3 = (float(struct.unpack_from('<H', f_lnd.read(2))[0]) / 100) + grid_y
				data_read += 4
				
				f_obj.write(f"v {x3} {y3} {z3}\n")
				
				print("	Vertex:")
				#print("		x_data = {}".format(x3_data & 0x80))
				print("		x = {}".format(x3))
				print("		y = {}".format(y3))
				print("		z = {}".format(z3))
				print("")
				
				area = calc_triangle_area(x1, z1, x2, z2, x3, z3)
				print("		area = {}".format(area))
				print("")
				
				vertices_total += 3
				faces.append([vertices_total - 2, vertices_total - 1, vertices_total])
				
				while(area < 1024.0):
					## Copy vertex
					x1, z1 = x2, z2
					x2, z2 = x3, z3
					
					## Get next vertex
					x3_data = struct.unpack_from('<B', f_lnd.read(1))[0]
					z3_data = struct.unpack_from('<B', f_lnd.read(1))[0]
					
					x3 = (float(x3_data & 0x7F) + grid_x)
					z3 = (float(z3_data) + grid_z)
					y3 = (float(struct.unpack_from('<H', f_lnd.read(2))[0]) / 100) + grid_y
					data_read += 4
					
					if(z3_data <= 32):
						## Next
						vertices_total += 1
						
						print("	Vertex:")
						#print("		x_data = {}".format(x3_data))
						#print("		z_data = {}".format(z3_data))
						print("		x = {}".format(x3))
						print("		y = {}".format(y3))
						print("		z = {}".format(z3))
						print("")
						
						f_obj.write(f"v {x3} {y3} {z3}\n")
						
						if(x3_data & 0x80 == 0):
							## Increate area
							area += calc_triangle_area(x1, z1, x2, z2, x3, z3)
							
							print("	area = {}".format(area))
							print("")
							
							faces.append([vertices_total - 2, vertices_total - 1, vertices_total])
							
							print("vertices_total = {}".format(vertices_total))
					else:
						unknown_5_1 = f_lnd.read(12).hex()
						data_read += 12
						
						print("	unknown_5_1 = {}".format(unknown_5_1))
						
						## Copy vertex
						x3, z3 = x2, z2
						x2, z2 = x1, z1
				
				for face in faces:
					x = face[0]
					y = face[1]
					z = face[2]
					
					f_obj.write(f"f {x} {y} {z}\n")
				
				unknown_3_1 = f_lnd.read(data_total - data_read).hex()
				print("	unknown_3_1 = 0x{}".format(unknown_3_1))
