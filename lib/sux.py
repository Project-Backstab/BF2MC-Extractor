import os
import json

from lib.functions import create_file

def print_header(block_header_data, tabs):
    # Ensure the input is a bytes-like object
    if not isinstance(block_header_data, (bytes, bytearray)):
        raise ValueError("Input data must be bytes or bytearray.")

    # Determine the length of the data
    length = len(block_header_data)

    # Iterate over the data in chunks of 16 bytes
    for i in range(0, length, 16):
        # Extract a 16-byte segment (or less if at the end)
        line_bytes = block_header_data[i:i + 16]
        
        # Format the line in groups of 4 bytes
        formatted_line = " ".join(
            line_bytes[j:j + 4].hex().upper() for j in range(0, len(line_bytes), 4)
        )
        
        # Print the formatted line
        print(tabs + formatted_line)
				
def analise_sux(input_sux_filepath):
	## Read sux file
	with open(input_sux_filepath, "rb") as f_sux:
		print("============================================================")
		print(input_sux_filepath)
		
		## Read main header
		if(main_header_data := f_sux.read(0x60)):
			
			## Debug
			print("header: ")
			print_header(main_header_data, "	")
			
			image_index = 0
			while(image_header_data := f_sux.read(0x10)):
				## Calculate image data size
				image_data_size = ((image_header_data[1] << 0x8) + image_header_data[0]) * 0x10
				
				## Debug
				print("")
				print("	image {}: ".format(image_index))
				print("		header:")
				print_header(image_header_data, "			")
				print("		data_size: {} ({})".format(image_data_size, hex(image_data_size)))
				
				## Read blocks
				block_index = 0
				image_data_read = 0
				while(image_data_read < image_data_size):
					
					## Read block header
					if(block_header_data := f_sux.read(0x50)):
						image_data_read += 0x50
						
						## Calculate block data size and read block data
						block_data_size = ((block_header_data[0x41] & 0xF) << 0xC) + (block_header_data[0x40] << 0x4)
						image_data_read += block_data_size
						f_sux.read(block_data_size)
						
						## Debug
						print("")
						print("		block {}: ".format(block_index))
						print("			header:")
						print_header(block_header_data, "				")
						print("			data_size: {} ({})".format(block_data_size, hex(block_data_size)))
						
						block_index += 1
					else:
						print("ERROR: Can't read block header.")
				
				## In case there is not enough read then its defined in the file.
				if(image_data_read != image_data_size):
					print("ERROR: image_data_read != image_data_size")
				
				image_index += 1
		else:
			print("ERROR: Not enough sux data for the main header.")
		
		print("============================================================")