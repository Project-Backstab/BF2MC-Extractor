#!/bin/env python3

from lib.brs.mesh_descriptor import export_mesh_descriptor, import_mesh_descriptor

def main():
	export_mesh_descriptor("files/backstab_market.Component_backstab_market.brs", "output/backstab_market.Component_backstab_market.brs.json")
	export_mesh_descriptor("files/balcony_bars_001.Component_balcony_bars_001.brs", "output/balcony_bars_001.Component_balcony_bars_001.brs.json")
	
	## Not ready yet
	#import_mesh_descriptor("output/backstab_market.Component_backstab_market.brs.json", "output/backstab_market.Component_backstab_market.brs")
	#import_mesh_descriptor("output/balcony_bars_001.Component_balcony_bars_001.brs.json", "output/balcony_bars_001.Component_balcony_bars_001.brs")

main()