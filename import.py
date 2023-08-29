#!/bin/env python3

import os
from lib.ark import import_ark
from lib.cat import import_cat

##
## Integrity check
##
def integrity_check():
	print("SHA256 Integrity check:")
	os.system("sha256sum files/SLUS-21026/DATA.ARK")
	os.system("sha256sum output/DATA.ARK/DATA.ARK")	

def main():
	## Create new audio_CaptureTheFlag.cat file
	print("Import \"output/Levels/BackStab/audio_CaptureTheFlag.cat/\"")
	import_cat("output/Levels/BackStab/audio_CaptureTheFlag.cat/", "audio_CaptureTheFlag.cat")
	print("Done!")
	
	## Copy results to DATA.ARK project
	os.system("cp output/Levels/BackStab/audio_CaptureTheFlag.cat/audio_CaptureTheFlag.cat output/DATA.ARK/Border/Levels/BackStab/")
	
	## Create new DATA.ARK
	print("Import \"output/DATA.ARK\"")
	import_ark("output/DATA.ARK/", "DATA.ARK")
	print("Done!")
	
	integrity_check()

main()
