#!/bin/env python3

from lib.lnd import export_pc_lnd, export_ps2_lnd

def main():
	export_pc_lnd("files/server/BackStab/MeshData/pc_high.lnd", "output/pc_high.lnd.obj")
	export_ps2_lnd("files/client/BackStab/MeshData/ps2_high.lnd", "output/ps2_high.lnd.obj")

main()