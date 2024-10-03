import subprocess
import json
import numpy as np
from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List

@dataclass
class Block:
	header: str = ""
	x: int = 0
	y: int = 0
	width: int = 0
	height: int = 0
	is_palette: bool = False
	format_type: int = 0
	data_size: int = 0
	data: str = ""

@dataclass
class Image:
	header: str = ""
	data_size: int = 0
	blocks: List[Block] = field(default_factory=list)

@dataclass
class Sux:
	header: str = ""
	images: List[Image] = field(default_factory=list)

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

def create_tga(filename, palette, indices):
	width = len(indices[0])
	height = len(indices)
	
	with open(filename, 'wb') as f:
		# Header (18 bytes)
		f.write(bytearray([
			0,          # ID length
			1,          # Color map type (1 for palette)
			1,          # Image type (1 for uncompressed, color-mapped)
			0, 0,       # Color map first entry index
			len(palette) & 0xFF, (len(palette) >> 8) & 0xFF,  # Color map length (number of entries)
			32,
			0, 0,       # X-origin
			0, 0,       # Y-origin
			width & 0xFF, (width >> 8) & 0xFF,  # Width
			height & 0xFF, (height >> 8) & 0xFF,  # Height
			8,          # Pixel depth (8 bits per pixel)
			0           # Image descriptor
		]))

		# Color Map Data
		for color in palette:
			f.write(bytearray([color[2], color[1], color[0], color[3]]))  # BGRA order

		# Image Data
		for row in indices:
			f.write(bytearray(row))

def tga2sux(input_file_path, output_file_path, sux_flags):
	sux_exe = "wine SUX3_Converter/ImageConverter.exe"
	
	command = f"{sux_exe} {sux_flags} {input_file_path} {output_file_path}"

	result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	
	#print(f"{result.stdout}")
	#print(f"{result.stderr}")

def sux2json(input_file_path, output_file_path):
	sux = Sux()
	
	with open(input_file_path, 'rb') as f_sux:
		if(sux_header := f_sux.read(0x60)):
			sux.header = sux_header.hex()
			while(image_header_data := f_sux.read(0x10)):
				image = Image()
				
				image.header = image_header_data.hex()
				image.data_size = ((image_header_data[1] << 0x8) + image_header_data[0]) * 0x10
				
				image_data_read = 0
				while(image_data_read < image.data_size):
					## Read block header
					if(block_header_data := f_sux.read(0x50)):
						image_data_read += 0x50
						
						block = Block()
						
						block.header = block_header_data.hex()
						block.x = block_header_data[0x15]
						block.y = block_header_data[0x14]
						block.width = block_header_data[0x20]
						block.height = block_header_data[0x24]
						block.is_palette = (block_header_data[0x41] & 0xF0) == 0x80
						block.data_size = ((block_header_data[0x41] & 0xF) << 0xC) + (block_header_data[0x40] << 0x4)
						
						area = block.width * block.height
						if(area == block.data_size * 2):
							block.format_type = 4
						elif(area == block.data_size):
							block.format_type = 8
						else:
							block.format_type = 32
						
						block.data = f_sux.read(block.data_size).hex()
						image_data_read += block.data_size
						
						image.blocks.append(block)
					else:
						print("ERROR: Can't read block header.")
				
				sux.images.append(image)
		else:
			print("ERROR: Not enough sux data for the main header.")
	
	with open(output_file_path, "w") as json_file:
		json.dump(sux, json_file, cls=CustomEncoder)

def data2indices(data, width, height):
	if len(data) != width * height:
		raise ValueError("Hex string size does not match the specified width and height.")

	# Convert hex string to binary string, then take 4-bit chunks
	binary_string = bin(int(data, 16))[2:].zfill(width * height * 4)
	
	chunks = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
	
	# Convert each 4-bit chunk into an integer
	int_values = [int(chunk, 2) for chunk in chunks]

	# Arrange into 2D array
	array_2d = [int_values[i:i+width] for i in range(0, len(int_values), width)]

	return array_2d

def find_change(indices):
	for row_index, row in enumerate(indices):
		if 1 in row:
			col_index = row.index(1)
			return row_index, col_index
	
	return None

def unswizzle(indices, swap_list):
	for y in range(len(indices)):
		for x in range(len(indices[0])):
			swap = swap_list[y][x]
			x2 = swap[0]
			y2 = swap[1]
			
			indices[y][x], indices[y2][x2] = indices[y2][x2], indices[y][x]
	
	return indices

def gen_swap_list(width, height):
	palette = [
		(0,   0,   0,   255),  # Black
		(255, 255, 255, 255)   # White
	]

	indices = [[0] * width for _ in range(height)]
	swap_list = [[[0, 0]] * width for _ in range(height)]
	
	for y in range(height):
		for x in range(width):
			indices[y][x] = 1
			
			create_tga("output.tga", palette, indices)
			tga2sux("output.tga", "output.sux", "-4 -nomipmaps")
			sux2json("output.sux", "output.sux.json")
			
			with open("output.sux.json", 'r') as f_json:
				sux = json.load(f_json)
				image = sux["images"][0]
				block = image["blocks"][0]
				
				indices = data2indices(block["data"], width, height)
				
				indices = unswizzle(indices, swap_list)
				
				x2, y2 = find_change(indices)
				
				swap_list[y][x] = [x2, y2]
				
				print("----------------------")
				print(f"x, y = {x}, {y}")
				print(f"x2, y2 = {x2}, {y2}")
			
			indices[y][x] = 0
	
	with open(f"swap_list_{width}x{height}", "w") as json_file:
		json.dump(swap_list, json_file, cls=CustomEncoder)

def main():
	gen_swap_list(128, 128)

main()