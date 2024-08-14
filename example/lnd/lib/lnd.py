import re
import os
import struct
			
def export_pc_lnd(input_file_path, output_file_path):
	with open(input_file_path, 'rb') as f_lnd:
		with open(output_file_path, 'w') as f_obj:
			f_obj.write("o\n")
			
			vertices_total = 1
			
			unknown_1_1 = struct.unpack('<I', f_lnd.read(4))[0]
			unknown_1_2 = struct.unpack('<I', f_lnd.read(4))[0]
			unknown_1_3 = struct.unpack('<I', f_lnd.read(4))[0]
			
			print("unknown_1_1 = {}".format(unknown_1_1))
			print("unknown_1_2 = {}".format(unknown_1_2))
			print("unknown_1_3 = {}".format(unknown_1_3))
			print("")
			
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
				print("")
				
				unknown_3_1 = struct.unpack('<I', f_lnd.read(4))[0]
				
				print("	unknown_3_1 = {}".format(unknown_3_1))
				print("")
				
				for j in range(unknown_3_1 * unknown_3_1):
					print("	Unknown Object {}:".format(j))
					
					unknown_4_1 = struct.unpack('<f', f_lnd.read(4))[0]
					unknown_4_2 = struct.unpack('<f', f_lnd.read(4))[0]
					unknown_4_3 = struct.unpack('<I', f_lnd.read(4))[0]
					unknown_4_4 = f_lnd.read(4 * unknown_4_3)
					
					print("		unknown_4_1 = {}".format(unknown_4_1))
					print("		unknown_4_2 = {}".format(unknown_4_2))
					print("		unknown_4_3 = {}".format(unknown_4_3))
					print("		unknown_4_4 = 0x{}".format(unknown_4_4.hex()))
					print("")
				
				faces_total = struct.unpack('<I', f_lnd.read(4))[0]
				faces = []
				for i in range(0, faces_total, 3):
					x = struct.unpack('<I', f_lnd.read(4))[0]
					y = struct.unpack('<I', f_lnd.read(4))[0]
					z = struct.unpack('<I', f_lnd.read(4))[0]
					
					faces.append([vertices_total + z, vertices_total + y, vertices_total + x])
				
				unknown_5_3 = f_lnd.read(12)
				
				print("	faces_total = {}".format(faces_total))
				print("	unknown_5_3 = 0x{}".format(unknown_5_3.hex()))
				print("")
				
				grid_vertices_total = struct.unpack('<I', f_lnd.read(4))[0]
				
				print("	grid_vertices_total = {}".format(grid_vertices_total))
				print("")
				
				vertices_total += grid_vertices_total
				
				for j in range(grid_vertices_total):
					print("	Vertex {}:".format(j))
					
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

"""
	Calculate the area of a triangle given its vertices.

	vertices: A list of three coordinate pairs [[x1, y1], [x2, y2], [x3, y3]]
	Returns the area of the triangle.
"""
def calc_triangle_area(x1, y1, x2, y2, x3, y3):
	return 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))

def export_ps2_lnd(input_file_path, output_file_path):
	with open(input_file_path, 'rb') as f_lnd:
		with open(output_file_path, 'w') as f_obj:
			f_obj.write("o\n")
			
			vertices_total = 0
			
			unknown_1_1 = struct.unpack('<I', f_lnd.read(4))[0]
			unknown_1_2 = struct.unpack('<I', f_lnd.read(4))[0]
			unknown_1_3 = struct.unpack('<I', f_lnd.read(4))[0]
			
			print("unknown_1_1 = {}".format(unknown_1_1))
			print("unknown_1_2 = {}".format(unknown_1_2))
			print("unknown_1_3 = {}".format(unknown_1_3))
			print("")
			
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
				
				print("	blocks_total = {}".format(blocks_total))
				print("	data_total = {}".format(data_total))
				
				unknown_2_1 = f_lnd.read(0x34).hex()
				print("	unknown_2_1 = 0x{}".format(unknown_2_1))
				
				j = 0
				faces = []
				
				## Get first triangle vertices
				x1_data = struct.unpack_from('<B', f_lnd.read(1))[0]
				x1 = (float(x1_data & 0x7F) + grid_x)
				z1 = (float(struct.unpack_from('<B', f_lnd.read(1))[0]) + grid_z)
				y1 = (float(struct.unpack_from('<H', f_lnd.read(2))[0]) / 100) + grid_y
				
				f_obj.write(f"v {x1} {y1} {z1}\n")
				
				print("	Vertex {}:".format(j))
				#print("		x_data = {}".format(x1_data & 0x80))
				print("		x = {}".format(x1))
				print("		y = {}".format(y1))
				print("		z = {}".format(z1))
				print("")
				
				j += 1
				
				x2_data = struct.unpack_from('<B', f_lnd.read(1))[0]
				x2 = (float(x2_data & 0x7F) + grid_x)
				z2 = (float(struct.unpack_from('<B', f_lnd.read(1))[0]) + grid_z)
				y2 = (float(struct.unpack_from('<H', f_lnd.read(2))[0]) / 100) + grid_y
				
				f_obj.write(f"v {x2} {y2} {z2}\n")
				
				print("	Vertex {}:".format(j))
				#print("		x_data = {}".format(x2_data & 0x80))
				print("		x = {}".format(x2))
				print("		y = {}".format(y2))
				print("		z = {}".format(z2))
				print("")
				
				j += 1
				
				x3_data = struct.unpack_from('<B', f_lnd.read(1))[0]
				x3 = (float(x3_data & 0x7F) + grid_x)
				z3 = (float(struct.unpack_from('<B', f_lnd.read(1))[0]) + grid_z)
				y3 = (float(struct.unpack_from('<H', f_lnd.read(2))[0]) / 100) + grid_y
				
				f_obj.write(f"v {x3} {y3} {z3}\n")
				
				print("	Vertex {}:".format(j))
				#print("		x_data = {}".format(x3_data & 0x80))
				print("		x = {}".format(x3))
				print("		y = {}".format(y3))
				print("		z = {}".format(z3))
				print("")
				
				j += 1
				
				area = calc_triangle_area(x1, z1, x2, z2, x3, z3)
				vertices_total += 3
				faces.append([vertices_total - 2, vertices_total - 1, vertices_total])
				
				print("		area = {}".format(area))
				print("")
				
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
					
					if(z3_data <= 32):
						## Next
						vertices_total += 1
						
						print("	Vertex {}:".format(j))
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
							print("j = {}".format(j))
					else:
						unknown_5_1 = f_lnd.read(12).hex()
						print("	unknown_5_1 = {}".format(unknown_5_1))
						j += 3
						
						## Copy vertex
						x3, z3 = x2, z2
						x2, z2 = x1, z1
						
					j += 1
				
				for face in faces:
					x = face[0]
					y = face[1]
					z = face[2]
					
					f_obj.write(f"f {x} {y} {z}\n")
				
				unknown_3_1 = f_lnd.read(data_total - (j * 4) - 0x34).hex()
				print("	unknown_3_1 = 0x{}".format(unknown_3_1))

