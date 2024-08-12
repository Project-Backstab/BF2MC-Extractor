import os
import json

from lib.functions import create_file

def print_data(tabs, data):
    # Ensure the input is a bytes-like object
    if not isinstance(data, (bytes, bytearray)):
        raise ValueError("Input data must be bytes or bytearray.")

    # Determine the length of the data
    length = len(data)

    # Iterate over the data in chunks of 16 bytes
    for i in range(0, length, 16):
        # Extract a 16-byte segment (or less if at the end)
        line_bytes = data[i:i + 16]
        
        # Format the line in groups of 4 bytes
        formatted_line = " ".join(
            line_bytes[j:j + 4].hex().upper() for j in range(0, len(line_bytes), 4)
        )
        
        # Print the formatted line
        print(tabs + formatted_line)

def read_images(sux_filepath, f_sux):
	image_index = 0
	
	while(image_header_data := f_sux.read(0x10)):
		## Calculate image data size
		image_data_size = ((image_header_data[1] << 0x8) + image_header_data[0]) * 0x10
		
		## Debug
		print("")
		print("	image {}: ".format(image_index))
		print("		header:")
		print_data("			", image_header_data)
		print("		data_size: {} ({})".format(image_data_size, hex(image_data_size)))
		
		read_blocks(sux_filepath, f_sux, image_index, image_data_size)
		
		image_index += 1

def read_blocks(sux_filepath, f_sux, image_index, image_data_size):
	block_index = 0
	image_data_read = 0
	
	while(image_data_read < image_data_size):
		
		## Read block header
		if(block_header_data := f_sux.read(0x50)):
			image_data_read += 0x50
			
			## x and y cordination
			block_x = block_header_data[0x14]
			block_y = block_header_data[0x15]
			
			## Width and height
			block_width = block_header_data[0x20]
			block_height = block_header_data[0x24]
			
			## Check if block is palette
			block_is_palette = block_header_data[0x41] & 0xF0
			
			## Calculate block data size and read block data
			block_data_size = ((block_header_data[0x41] & 0xF) << 0xC) + (block_header_data[0x40] << 0x4)
			image_data_read += block_data_size
			
			## Read block data
			block_data = f_sux.read(block_data_size)
			
			## Write block
			block_filepath = sux_filepath + ".image_{}.block_{}".format(image_index, block_index)
			create_file(block_filepath, block_data)
			
			## Debug
			print("")
			print("		block {}: ".format(block_index))
			print("			header:")
			print_data("				", block_header_data)
			print("			data_size: {} ({})".format(block_data_size, hex(block_data_size)))
			print("			block_x: {}".format(block_x))
			print("			block_y: {}".format(block_y))
			print("			block_width: {}".format(block_width))
			print("			block_height: {}".format(block_height))
			print("			block_palette: {} ({})".format(block_is_palette, hex(block_is_palette)))
		else:
			print("ERROR: Can't read block header.")
		
		block_index += 1
	
	## In case there is not enough read then its defined in the file.
	if(image_data_read != image_data_size):
		print("ERROR: image_data_read != image_data_size")

def analise_sux(sux_filepath):
	## Read sux file
	with open(sux_filepath, "rb") as f_sux:
		print("============================================================")
		print(sux_filepath)
		
		## Read main header
		if(main_header_data := f_sux.read(0x60)):
			
			## Debug
			print("header: ")
			print_data("	", main_header_data)
			
			read_images(sux_filepath, f_sux)
		else:
			print("ERROR: Not enough sux data for the main header.")
		
		print("============================================================")