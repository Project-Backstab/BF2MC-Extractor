#!/bin/env python3

import os
import json
import re
import binascii
import zlib

from lib.functions import create_file, modify_file_path

from dataclasses import dataclass, field, asdict, is_dataclass
from typing import List

@dataclass
class FileInfo:
	file_path: str = ""
	file_path_space: str = ""
	audio_header: str = ""

@dataclass
class Cat:
	zlib: str = ""
	file_infos: List[FileInfo] = field(default_factory=list)

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

def export_cat(input_cat_filepath, output_files_path, has_audio_header = False):	
	## Create directories if they are missing
	os.makedirs(output_files_path, exist_ok=True)
	
	cat = Cat()
	
	## Read cat file
	with open(input_cat_filepath, "rb") as f_cat:
		files_info = []
		
		## Read all file data
		content = f_cat.read()
		
		## Check there is zlib compression
		if(content[0:4].decode("ascii") == "PZFB"):
			cat.zlib = content[:0x10].hex()
			content = zlib.decompress(content[0x10:])
		
		## Read file size bytes until the end of the cat file is reached.
		offset = 0
		while(offset + 4 < len(content)):
			file_info = FileInfo()
			
			## Get File path and spaces
			file_path_length = int.from_bytes(content[offset:offset + 4], byteorder='little')
			offset += 4
			file_path = content[offset:offset + file_path_length].decode('ascii')
			offset += file_path_length
			
			file_info.file_path = file_path.rstrip('\x00')
			file_info.file_path_space = len(file_path) - len(file_info.file_path)
			
			## Get extra audio header information. Only for audio_*.cat files
			if(has_audio_header):
				file_info.audio_header = content[offset:offset + 4].hex()
				offset += 4
			
			## Get file data
			file_data_length = int.from_bytes(content[offset:offset + 4], byteorder='little')
			offset += 4
			file_data = content[offset:offset + file_data_length]
			offset += file_data_length
			
			## Save file
			create_file(output_files_path + file_info.file_path, file_data)
			
			## Save file information
			cat.file_infos.append(file_info)
		
		## Save cat file information to json
		with open(output_files_path + "cat.json", "w") as json_file:
			json.dump(cat, json_file, cls=CustomEncoder)

def import_cat(input_files_path, output_file_path):
	content = b''
	
	with open(input_files_path + "cat.json", 'r') as f_json:
		cat = json.load(f_json)
			
		for file_info in cat["file_infos"]:
			file_path_length = len(file_info["file_path"]) + file_info["file_path_space"]
			
			## Write file path
			content += file_path_length.to_bytes(4, 'little')
			content += file_info["file_path"].encode('ascii')
			content += b'\x00' * file_info["file_path_space"]
			
			## Fix: write extra header value for audio_*.cat files 
			if(file_info["audio_header"] != ""):
				content += bytes.fromhex(file_info["audio_header"])
			
			## Write file data
			file_path = input_files_path + "/" + file_info["file_path"]
			with open(file_path, "rb") as f_file:
				file_size = os.path.getsize(file_path)
				
				content += file_size.to_bytes(4, 'little')
				content += f_file.read(file_size)
		
		## Zlib compression
		if(cat["zlib"] != ""):
			content = bytes.fromhex(cat["zlib"]) + zlib.compress(content)
		
	## Create new *.cat file
	with open(output_file_path, "wb") as f_cat:
		f_cat.write(content)