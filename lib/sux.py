import os
import json

from lib.functions import create_file

def isBlockHeader(block_header_data):
	return (
		len(block_header_data) == 0x50 and
		block_header_data[0] == 3 and block_header_data[1] == 0 and block_header_data[2] == 0 and block_header_data[3] == 0 and
		block_header_data[24] == 0x51 and block_header_data[40] == 0x52 and block_header_data[56] == 0x53
	)

def analise_sux(input_sux_filepath):
	## Read sux file
	with open(input_sux_filepath, "rb") as f_sux:
		sux_header_data = f_sux.read(0x60)
		
		print("============================================================")
		print("============================================================")
		print(input_sux_filepath)
		print("header: ")
		print("	{} {} {} {}\n	{} {} {} {}\n	{} {} {} {}\n	{} {} {} {}\n	{} {} {} {}\n	{} {} {} {}\n	{} {} {} {}".format(
			sux_header_data[0x00:0x04].hex(), sux_header_data[0x04:0x08].hex(), sux_header_data[0x08:0x0C].hex(), sux_header_data[0x0C:0x10].hex(),
			sux_header_data[0x10:0x14].hex(), sux_header_data[0x14:0x18].hex(), sux_header_data[0x18:0x1C].hex(), sux_header_data[0x1C:0x20].hex(),
			sux_header_data[0x20:0x24].hex(), sux_header_data[0x24:0x28].hex(), sux_header_data[0x28:0x2C].hex(), sux_header_data[0x2C:0x30].hex(),
			sux_header_data[0x30:0x34].hex(), sux_header_data[0x34:0x38].hex(), sux_header_data[0x38:0x3C].hex(), sux_header_data[0x3C:0x40].hex(),
			sux_header_data[0x40:0x44].hex(), sux_header_data[0x44:0x48].hex(), sux_header_data[0x48:0x4C].hex(), sux_header_data[0x4C:0x50].hex(),
			sux_header_data[0x50:0x54].hex(), sux_header_data[0x54:0x58].hex(), sux_header_data[0x58:0x5C].hex(), sux_header_data[0x5C:0x60].hex(),
			sux_header_data[0x60:0x64].hex(), sux_header_data[0x64:0x68].hex(), sux_header_data[0x68:0x6C].hex(), sux_header_data[0x6C:0x70].hex())
		)
		
		block_header_address = 0
		block_index = 0
		earlier_block_header_address = 0
		
		while(block_header_data := f_sux.read(0x50)):
			if(isBlockHeader(block_header_data)):
				if(block_index != 0):
					block_data_size = block_header_address - earlier_block_header_address - 0x50
					print("	data size: {}".format(hex(block_data_size)))
					print("")
				
				print("Block {}:".format(block_index))
				print("	header:")
				
				## All header values
				"""
				print("		{} {} {} {}\n		{} {} {} {}\n		{} {} {} {}\n		{} {} {} {}\n		{} {} {} {}".format(
					block_header_data[0x00:0x04].hex(), block_header_data[0x04:0x08].hex(), block_header_data[0x08:0x0C].hex(), block_header_data[0x0C:0x10].hex(),
					block_header_data[0x10:0x14].hex(), block_header_data[0x14:0x18].hex(), block_header_data[0x18:0x1C].hex(), block_header_data[0x1C:0x20].hex(),
					block_header_data[0x20:0x24].hex(), block_header_data[0x24:0x28].hex(), block_header_data[0x28:0x2C].hex(), block_header_data[0x2C:0x30].hex(),
					block_header_data[0x30:0x34].hex(), block_header_data[0x34:0x38].hex(), block_header_data[0x38:0x3C].hex(), block_header_data[0x3C:0x40].hex(),
					block_header_data[0x40:0x44].hex(), block_header_data[0x44:0x48].hex(), block_header_data[0x48:0x4C].hex(), block_header_data[0x4C:0x50].hex())
				)
				"""
				
				## Header values that are relavent
				print(
					"		{}\n		{} {}\n		{} {}".format(
						block_header_data[0x14:0x18].hex(),
						block_header_data[0x20:0x24].hex(), block_header_data[0x24:0x28].hex(),
						block_header_data[0x40:0x44].hex(), block_header_data[0x44:0x48].hex()
					)
				)
				print("	address: {}".format(hex(block_header_address)))
				
				width = int.from_bytes(block_header_data[0x20:0x24], byteorder='little')
				height = int.from_bytes(block_header_data[0x24:0x28], byteorder='little')
				
				block_data_size = width * height
				print("	width, height: {}, {}".format(width, height))
				print("	calc data size: {}".format(hex(block_data_size)))
				
				block_index += 1
				earlier_block_header_address = block_header_address
		
			## Set to next 4 bytes
			f_sux.seek(block_header_address + 4)
			block_header_address += 4
		
		block_data_size = os.path.getsize(input_sux_filepath) - earlier_block_header_address - 0x50
		print("	data size: {}".format(hex(block_data_size)))