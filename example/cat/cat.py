#!/bin/env python3

import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from lib.cat import export_cat, export_cat_resource

def main():
	## PS2
	export_cat("files/BackStab/audio_common.cat",         "output/BackStab/audio_common.cat/")
	export_cat("files/BackStab/audio_CaptureTheFlag.cat", "output/BackStab/audio_CaptureTheFlag.cat/")
	export_cat("files/BackStab/audio_conquest.cat",       "output/BackStab/audio_conquest.cat/")
	
	export_cat_resource("files/BackStab/resources.cat",               "output/BackStab/resources.cat/")
	export_cat_resource("files/BackStab/resourcesCaptureTheFlag.cat", "output/BackStab/resourcesCaptureTheFlag.cat/")
	export_cat_resource("files/BackStab/resourcesconquest.cat",       "output/BackStab/resourcesconquest.cat/")
	
	## Not supported
	#export_cat("files/BackStab/spray_common.cat",         "output/BackStab/spray_common.cat/")
	#export_cat("files/BackStab/spray_CaptureTheFlag.cat", "output/BackStab/spray_CaptureTheFlag.cat/")
	#export_cat("files/BackStab/spray_conquest.cat",       "output/BackStab/spray_conquest.cat/")
	
	export_cat("files/BackStab/textures.cat",               "output/BackStab/textures.cat/")
	export_cat("files/BackStab/texturesCaptureTheFlag.cat", "output/BackStab/texturesCaptureTheFlag.cat/")
	export_cat("files/BackStab/texturesconquest.cat",       "output/BackStab/texturesconquest.cat/")
	
	## Xbox 360
	export_cat_resource("files/wilderness/resources.cat",               "output/wilderness/resources.cat/")
	export_cat_resource("files/wilderness/resourcescapturetheflag.cat", "output/wilderness/resourcescapturetheflag.cat/")
	export_cat_resource("files/wilderness/resourcesconquest.cat",       "output/wilderness/resourcesconquest.cat/")
	
	export_cat("files/wilderness/audio_common.cat",         "output/wilderness/audio_common.cat/")
	export_cat("files/wilderness/audio_capturetheflag.cat", "output/wilderness/audio_capturetheflag.cat/")
	export_cat("files/wilderness/audio_conquest.cat",       "output/wilderness/audio_conquest.cat/")
	
	export_cat("files/wilderness/textures.cat",               "output/wilderness/textures.cat/")
	export_cat("files/wilderness/texturescapturetheflag.cat", "output/wilderness/texturescapturetheflag.cat/")
	export_cat("files/wilderness/texturesconquest.cat",       "output/wilderness/texturesconquest.cat/")
	
main()