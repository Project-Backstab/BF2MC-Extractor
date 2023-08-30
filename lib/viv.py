#!/bin/env python3

import os
import json

from lib.functions import create_file

TEMPLATE_FILE_INFO = {
	"path":          "",  ## File path
	
	## These values are been temperarly used
	"data_address":  "",  ## File data address
	"size":           0,  ## File size
}

def export_viv(input_viv_filepath, output_files_path):	
	## Create directories if they are missing
	os.makedirs(output_files_path, exist_ok=True)
	
	## Read viv file
	with open(input_viv_filepath, "rb") as f_viv:
		files_info = []
		
		## Read Information header
		magic_bytes = f_viv.read(4)
		viv_file_size = int.from_bytes(f_viv.read(4), byteorder='little')
		total_files = int.from_bytes(f_viv.read(4), byteorder='big')
		files_data_address = f_viv.read(4)
		
		## Debug
		#print("magic_bytes = {}".format(magic_bytes))
		#print("viv_file_size = {}".format(hex(viv_file_size)))
		#print("total_files = {}".format(total_files))
		#print("files_data_address = 0x{}".format(files_data_address.hex()))
		
		for i in range(total_files):
			file_info = dict(TEMPLATE_FILE_INFO)
			
			file_info["data_address"] = hex(int.from_bytes(f_viv.read(4), byteorder='big'))
			file_info["size"] = int.from_bytes(f_viv.read(4), byteorder='big')
			
			## Read file path until we hit 0x00
			while(data := f_viv.read(1)):
				if(data == b'\x00'):
					break
				file_info["path"] += data.decode('ascii')
			
			file_info["path"] = file_info["path"].replace("\\", "/")
			
			## Save file information
			files_info.append(file_info)
		
		## Save file information inside files.json
		with open(output_files_path + "files.json", "w") as f_files:
			f_files.write(json.dumps(files_info))
		
		for file_info in files_info:
			## Set file offset
			f_viv.seek(int(file_info["data_address"], 16))
			
			## Extract file data
			file_data = f_viv.read(file_info["size"])
			
			## Save file
			create_file(output_files_path + file_info["path"], file_data)
			
def calc_files_info_end_address(files_info):
	writen_bytes = 24
	
	for file_info in files_info:
		writen_bytes += len(file_info["path"]) + 9
	
	return writen_bytes

def calc_viv_file_size(input_files_path, files_info):
	writen_bytes = calc_files_info_end_address(files_info)
	writen_bytes += 8
	
	x = writen_bytes % 0x800
	if(x != 0):
		writen_bytes += (0x800 - x)
	
	for file_info in files_info:
		## File size
		file_path = input_files_path + file_info["path"]
		writen_bytes += os.path.getsize(file_path)
		
		## empty space
		x = writen_bytes % 0x800
		if(x != 0):
			writen_bytes += (0x800 - x)
	
	return writen_bytes

def calc_next_file_data_address(file_data_address, file_size):
	next_file_data_address = file_data_address + file_size
	
	x = next_file_data_address % 0x800
	if(x != 0):
		next_file_data_address += (0x800 - x)
	
	return next_file_data_address

def import_viv(input_files_path, output_cat_filename):
	# Open files.json to get the files information to pack to .viv
	with open(input_files_path + "files.json", "r") as f_files:
		## Create new *.viv file
		with open(input_files_path  + output_cat_filename, "wb") as f_viv:
			files_info = json.load(f_files)
			
			viv_file_size = calc_viv_file_size(input_files_path, files_info)
			files_info_end_address = calc_files_info_end_address(files_info)
			
			## Write viv file header
			f_viv.write(bytes("BIG4", 'ascii'))				       # Magic bytes
			f_viv.write(viv_file_size.to_bytes(4, 'little'))       # .viv file size
			f_viv.write(len(files_info).to_bytes(4, 'big'))        # Total files
			f_viv.write(files_info_end_address.to_bytes(4, 'big')) # File information end address
			
			## Write file information
			file_data_address = calc_next_file_data_address(files_info_end_address, 8)
			for file_info in files_info:
				file_path = input_files_path + file_info["path"]
				
				## Patch values in case changes happend on the files
				file_info["size"] = os.path.getsize(file_path)
				file_info["data_address"] = file_data_address.to_bytes(4, 'big').hex()
				file_data_address = calc_next_file_data_address(file_data_address, file_info["size"])
				
				## Write file data address
				f_viv.write(int(file_info["data_address"], 16).to_bytes(4, 'big'))	# Needs fix
				
				## Write file size
				f_viv.write(file_info["size"].to_bytes(4, 'big'))
				
				## Write file path
				f_viv.write(bytes(file_info["path"].replace("/", "\\"), 'ascii'))
				f_viv.write(b'\x00')
			
			## Some random data WTF?!
			f_viv.write(bytes("L269", 'ascii'))
			f_viv.write(b'\x15\x05\x00\x00')
			
			writen_bytes = files_info_end_address
			
			## Some more random data WTF?!
			f_viv.write(bytes("Buy ERTS", 'ascii'))
			writen_bytes += 8
			
			## Write empty space
			x = writen_bytes % 0x800
			if(x != 0):
				f_viv.write(b'\x00' * (0x800 - x))
				writen_bytes += (0x800 - x)
			
			## Write file data
			for file_info in files_info:
				file_path = input_files_path + file_info["path"]
				
				## Open file
				with open(file_path, "rb") as f_file:
					f_viv.write(f_file.read(file_info["size"]))
					writen_bytes += file_info["size"]
				
				## Write empty space
				x = writen_bytes % 0x800
				if(x != 0):
					f_viv.write(b'\x00' * (0x800 - x))
					writen_bytes += (0x800 - x)