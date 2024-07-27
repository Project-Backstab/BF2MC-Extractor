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

def isBlockHeader(block_header_data):
	return (
		len(block_header_data) == 0x50 and
		block_header_data[0] == 3 and block_header_data[1] == 0 and block_header_data[2] == 0 and block_header_data[3] == 0 and
		block_header_data[24] == 0x51 and block_header_data[40] == 0x52 and block_header_data[56] == 0x53
	)

def analise_sux(input_sux_filepath):
	## Read sux file
	with open(input_sux_filepath, "rb") as f_sux:
		print("============================================================")
		print("============================================================")
		print(input_sux_filepath)
		
		if(sux_header_data := f_sux.read(0x70)):
			
			print("header: ")
			print_header(sux_header_data, "	")
			
			block_index = 0
			while(block_header_data := f_sux.read(0x50)):				
				if(isBlockHeader(block_header_data)):
					block_data_size = ((block_header_data[0x41] & 0xF) << 0xC) + (block_header_data[0x40] << 0x4)
				else:
					extra_data = f_sux.read(0x10)
					block_header_data = block_header_data + extra_data
					block_data_size = ((block_header_data[0x51] & 0xF) << 0xC) + (block_header_data[0x50] << 0x4)
					
					if(not isBlockHeader(block_header_data[0x10:0x60])):
						print("Something went wrong?! {}".format(block_header_data[0x00:0x04].hex()))
						return
				
				block_data = f_sux.read(block_data_size)
				
				print("")
				print("Block {}:".format(block_index))
				print("	header:")
				print_header(block_header_data, "		")
				print("	data_size: {} ({})".format(block_data_size, hex(block_data_size)))
				
				block_index += 1
		else:
			print("Sux file doesn't have enough data.")
				
				