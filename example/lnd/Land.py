#!/bin/env python3

import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from lib.lnd.pc  import export_pc_lnd, export_pc_lnd_2_obj
from lib.lnd.ps2 import export_ps2_lnd, export_ps2_lnd_2_obj

def main():
	#export_pc_lnd("files/server/BackStab/MeshData/pc_high.lnd", "output/pc_high.lnd.json")
	export_ps2_lnd("files/client/BackStab/MeshData/ps2_high.lnd", "output/ps2_high.lnd.json")
	
	## Old feature
	#export_pc_lnd_2_obj("files/server/BackStab/MeshData/pc_high.lnd", "output/pc_high.lnd.obj")
	export_ps2_lnd_2_obj("files/client/BackStab/MeshData/ps2_high.lnd", "output/ps2_high.lnd.obj")
	
main()