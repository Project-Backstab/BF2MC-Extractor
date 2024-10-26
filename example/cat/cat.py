#!/bin/env python3

import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from lib.cat          import export_cat, import_cat
from lib.cat_resource import export_cat_resource, import_cat_resource

def test_cat(input_file_path, output_files_path, output_file_path, has_audio_header = False):
	print(f"export \"{input_file_path}\" -> \"{output_files_path}\"")
	export_cat(input_file_path, output_files_path, has_audio_header)
	print("Done!")
	
	print(f"import \"{output_files_path}\" -> \"{output_file_path}\"")
	import_cat(output_files_path, output_file_path)
	print("Done!")
	
	os.system(f"sha256sum {input_file_path}")
	os.system(f"sha256sum {output_file_path}")

def test_cat_resource(input_file_path, output_files_path, output_file_path):
	print(f"export \"{input_file_path}\" -> \"{output_files_path}\"")
	export_cat_resource(input_file_path, output_files_path)
	print("Done!")
	
	print(f"import \"{output_files_path}\" -> \"{output_file_path}\"")
	import_cat_resource(output_files_path, output_file_path)
	print("Done!")
	
	os.system(f"sha256sum {input_file_path}")
	os.system(f"sha256sum {output_file_path}")

def main():
	## PS2
	test_cat("files/BackStab/audio_common.cat",                       "output/BackStab/audio_common.cat/",              "output/BackStab/audio_common.new.cat",           True)
	test_cat("files/BackStab/audio_CaptureTheFlag.cat",               "output/BackStab/audio_CaptureTheFlag.cat/",      "output/BackStab/audio_CaptureTheFlag.new.cat",   True)
	test_cat("files/BackStab/audio_conquest.cat",                     "output/BackStab/audio_conquest.cat/",            "output/BackStab/audio_conquest.new.cat",         True)
	
	## Resource
	test_cat_resource("files/BackStab/resources.cat",                 "output/BackStab/resources.cat/",                 "output/BackStab/resources.new.cat")
	test_cat_resource("files/BackStab/resourcesCaptureTheFlag.cat",   "output/BackStab/resourcesCaptureTheFlag.cat/",   "output/BackStab/resourcesCaptureTheFlag.new.cat")
	test_cat_resource("files/BackStab/resourcesconquest.cat",         "output/BackStab/resourcesconquest.cat/",         "output/BackStab/resourcesconquest.new.cat")
	
	## Not supported
	#export_cat("files/BackStab/spray_common.cat",                    "output/BackStab/spray_common.cat/")
	#export_cat("files/BackStab/spray_CaptureTheFlag.cat",            "output/BackStab/spray_CaptureTheFlag.cat/")
	#export_cat("files/BackStab/spray_conquest.cat",                  "output/BackStab/spray_conquest.cat/")
	
	test_cat("files/BackStab/textures.cat",                           "output/BackStab/textures.cat/",                  "output/BackStab/textures.new.cat")
	test_cat("files/BackStab/texturesCaptureTheFlag.cat",             "output/BackStab/texturesCaptureTheFlag.cat/",    "output/BackStab/texturesCaptureTheFlag.new.cat")
	test_cat("files/BackStab/texturesconquest.cat",                   "output/BackStab/texturesconquest.cat/",          "output/BackStab/texturesconquest.new.cat", )
	
	## Xbox 360
	test_cat_resource("files/wilderness/resources.cat",               "output/wilderness/resources.cat/",               "output/wilderness/resources.new.cat")
	test_cat_resource("files/wilderness/resourcescapturetheflag.cat", "output/wilderness/resourcescapturetheflag.cat/", "output/wilderness/resourcescapturetheflag.new.cat")
	test_cat_resource("files/wilderness/resourcesconquest.cat",       "output/wilderness/resourcesconquest.cat/",       "output/wilderness/resourcesconquest.new.cat")
	
	test_cat("files/wilderness/audio_common.cat",                     "output/wilderness/audio_common.cat/",            "output/wilderness/audio_common.new.cat")
	test_cat("files/wilderness/audio_capturetheflag.cat",             "output/wilderness/audio_capturetheflag.cat/",    "output/wilderness/audio_capturetheflag.new.cat")
	test_cat("files/wilderness/audio_conquest.cat",                   "output/wilderness/audio_conquest.cat/",          "output/wilderness/audio_conquest.new.cat")
	
	test_cat("files/wilderness/textures.cat",                         "output/wilderness/textures.cat/",                "output/wilderness/textures.new.cat")
	test_cat("files/wilderness/texturescapturetheflag.cat",           "output/wilderness/texturescapturetheflag.cat/",  "output/wilderness/texturescapturetheflag.new.cat")
	test_cat("files/wilderness/texturesconquest.cat",                 "output/wilderness/texturesconquest.cat/",        "output/wilderness/texturesconquest.new.cat")
	
	test_cat_resource("files/winterland/resources.cat",               "output/winterland/resources.cat/",               "output/winterland/resources.new.cat")
	test_cat_resource("files/winterland/resourcescapturetheflag.cat", "output/winterland/resourcescapturetheflag.cat/", "output/winterland/resourcescapturetheflag.new.cat")
	test_cat_resource("files/winterland/resourcesconquest.cat",       "output/winterland/resourcesconquest.cat/",       "output/winterland/resourcesconquest.new.cat")


main()