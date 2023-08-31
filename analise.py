#!/bin/env python3

import os
from lib.sux import analise_sux

def main():
	for root, dirs, files in os.walk('output/'):
		for file in files:
			if file.endswith('.sux'):
				sux_file_path = os.path.join(root, file)
				analise_sux(sux_file_path)
	
	"""
	analise_sux("output/DATA.ARK/Border/menus/Textures/advert.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/BorderLogo.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/BorderSplash.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/dnas_small.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/film_blur.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/lensflare1.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/FrontEnd.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/Generic.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/Hud.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/lensflare0.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/lensflare1.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/passcode_item.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/Tiles.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/video0.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/video1.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/video2.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/video3.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/video4.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/video5.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/video6.sux")
	analise_sux("output/DATA.ARK/Border/menus/Textures/video7.sux")	
	
	analise_sux("example/gamespy_sux/powered_by_gamespy.sux")
	analise_sux("example/gamespy_sux/gamespy.sux")
	
	analise_sux("example/gamespy_sux2/gamespy_16x8.sux")
	analise_sux("example/gamespy_sux2/gamespy_32x16.sux")
	analise_sux("example/gamespy_sux2/gamespy_64x32.sux")
	analise_sux("example/gamespy_sux2/gamespy_128x64.sux")
	analise_sux("example/gamespy_sux2/gamespy_256x128.sux")
	analise_sux("example/gamespy_sux2/gamespy_512x256.sux")
	analise_sux("example/gamespy_sux2/gamespy_1024x512.sux")
	"""

main()