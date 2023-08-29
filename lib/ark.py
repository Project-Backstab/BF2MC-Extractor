import os
import json

from lib.functions import create_file

TEMPLATE_FILE_INFO = {
	"unknown":           0,		## Unknown value that is always 1 for some reason
	"path":              "",	## File path
	"extra_data" :       "",	## On the end in the file information header they add extra bytes to fill up in modulo 4 way
								## This data can be sometimes random with no reason. To maintain the same hash we copy this data over
	
	## These values are been temperarly used
	"start_block":       0,		## Start block of file data
	"size":              0,		## Size of file
}

def _export_ark_files_info(input_ark_filepath):
	files_info = []
	
	## Read ark file
	with open(input_ark_filepath, "rb") as f_ark:
		ark_file_size = os.path.getsize(input_ark_filepath)
		
		## Read files header on the bottom of the ark file
		f_ark.seek(ark_file_size - 0x800)
		files_data_blocks = int.from_bytes(f_ark.read(4), byteorder='little')
		files_info_blocks = int.from_bytes(f_ark.read(4), byteorder='little')
		files_info_address = ark_file_size - 0x800 - (files_info_blocks * 0x800)
		
		## Read files header
		f_ark.seek(files_info_address)
		total_files = int.from_bytes(f_ark.read(4), byteorder='little')
		
		## Set file offset
		f_ark.seek(files_info_address + 0x800)
		
		for i in range(total_files):
			## Copy template
			file_info = dict(TEMPLATE_FILE_INFO)
			
			## Get file info
			file_info["unknown"]     = int.from_bytes(f_ark.read(4), byteorder='little')
			file_info["start_block"] = int.from_bytes(f_ark.read(4), byteorder='little')
			file_info["size"]        = int.from_bytes(f_ark.read(4), byteorder='little')
			path_length              = int.from_bytes(f_ark.read(4), byteorder='little')
			file_info["path"]        = f_ark.read(path_length).decode('utf-8')
			
			extra_data_length = 1 if (path_length + 1) % 4 == 0 else 5 - ((path_length + 1) % 4)
			file_info["extra_data"] = f_ark.read(extra_data_length).hex()
			
			files_info.append(file_info)
		
		## Debug
		#print("files_data_blocks = {}".format(files_data_blocks))
		#print("files_info_blocks = {}".format(files_info_blocks))
		#print("files_info_address = 0x{:x}".format(files_info_address))
		#print("total_files = {}".format(total_files))
		
	return files_info

def export_ark(input_ark_filepath, output_files_path):
	## Create directories if they are missing
	os.makedirs(output_files_path, exist_ok=True)
	
	## Extract file information
	files_info = _export_ark_files_info(input_ark_filepath)
	
	## Save file information inside files.json
	with open(output_files_path + "files.json", "w") as f_files:
		f_files.write(json.dumps(files_info))
	
	## Read ark file
	with open(input_ark_filepath, "rb") as f_ark:
		for file_info in files_info:
			## Set file offset
			f_ark.seek(file_info["start_block"] * 0x800)
			
			## Extract file data
			file_data = f_ark.read(file_info["size"])
		
			## Save file
			create_file(output_files_path + file_info["path"], file_data)

def import_ark(input_files_path, output_ark_filename):
	## Open files.json to get the files information to pack to .ark
	with open(input_files_path + "files.json", "r") as f_files:
		## Create new *.ark file
		with open(input_files_path  + output_ark_filename, "wb") as f_ark:
			files_info = json.load(f_files)
			
			## Write ARK header information
			f_ark.write(b'\x41\x52\x4B\x20')	## Magic code
			f_ark.write(b'\x01')				## Unknown header configuration
			f_ark.write(b'\x00' * 0x7FB)		## Empty space
			
			## Patch file information and write file data
			files_data_blocks = 1
			for file_info in files_info:
				file_path = input_files_path + file_info["path"]
				
				## Patch file information
				file_info["size"] = os.path.getsize(file_path)
				file_info["start_block"] = files_data_blocks
				
				## Write file data
				with open(file_path, "rb") as f_file:
					f_ark.write(f_file.read(file_info["size"]))
				
				## Write empty space
				x = file_info["size"] % 0x800
				files_data_blocks += file_info["size"] // 0x800
				if(x != 0):
					files_data_blocks += 1
					f_ark.write(b'\x00' * (0x800 - x))
			
			## Write total files
			files_info_blocks = 1
			f_ark.write(len(files_info).to_bytes(4, 'little'))
			f_ark.write(b'\x00' * 0x7FC)
			
			## Write files information
			writen_bytes = 0   ## Keep track how many bytes are been written
			for file_info in files_info:
				f_ark.write(file_info["unknown"].to_bytes(4, 'little'))
				f_ark.write(file_info["start_block"].to_bytes(4, 'little'))
				f_ark.write(file_info["size"].to_bytes(4, 'little'))
				f_ark.write(len(file_info["path"]).to_bytes(4, 'little'))
				writen_bytes += 16
				
				data = bytes(file_info["path"], 'ascii')
				f_ark.write(data)
				writen_bytes += len(data)
				
				data = bytes.fromhex(file_info["extra_data"])
				f_ark.write(data)
				writen_bytes += len(data)
			
			## Fill up with empty space if it doesnt end with a block of 0x800
			x = writen_bytes % 0x800
			files_info_blocks += writen_bytes // 0x800
			if(x != 0):
				files_info_blocks += 1
				f_ark.write(b'\x00' * (0x800 - x))
			
			## Write block information
			f_ark.write(files_data_blocks.to_bytes(4, 'little'))
			f_ark.write(files_info_blocks.to_bytes(4, 'little'))
			f_ark.write(b'\x00' * 0x7F8)

