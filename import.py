#!/bin/env python3

import os
from lib.ark import import_ark
from lib.cat import import_cat
from lib.viv import import_viv

##
## Integrity check
##
def integrity_check():
	print("SHA256 Integrity check:")
	os.system("sha256sum output/iso/BF2MC_MP/DATA.ARK")
	os.system("sha256sum output/DATA.ARK/DATA.ARK")
	
	os.system("sha256sum output/iso/SINGLE/8.VIV")
	os.system("sha256sum output/8.VIV/8.VIV")
	
	os.system("sha256sum output/iso/SINGLE/DATA.VIV")
	os.system("sha256sum output/DATA.VIV/DATA.VIV")
	
	os.system("sha256sum output/iso/SINGLE/DATA2.VIV")
	os.system("sha256sum output/DATA2.VIV/DATA2.VIV")

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
	
	## Copy DATA.ARK
	os.system("cp output/DATA.ARK/DATA.ARK output/iso/BF2MC_MP/")
	
	## Create .iso file
	## Doesnt work yet,... spend hours to fix this... =,='
	## Right now use ImgBurn on the output/iso directory to fix it yourself...
	#os.system("mkisofs -o output.iso output/iso/")
	
	## Create new *.VIV files
	print("Import \"output/8.VIV/\"")
	import_viv("output/8.VIV/", "8.VIV")
	print("Done!")
	
	print("Import \"output/DATA.VIV/\"")
	import_viv("output/DATA.VIV/", "DATA.VIV")
	print("Done!")
	
	print("Import \"output/DATA2.VIV/\"")
	import_viv("output/DATA2.VIV/", "DATA2.VIV")
	print("Done!")
	
	integrity_check()
	
main()
