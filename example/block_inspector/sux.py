#!/bin/env python3

from PIL import Image
import os

def gen_image(filepath, width, height):
	directory_path, filename = os.path.split(filepath)

	# Create a new image with RGBA mode (4 channels: Red, Green, Blue, Alpha)
	image = Image.new('RGBA', (width, height))

	# Get the pixel access object
	pixels = image.load()
	
	x, y = 0, 0
	
	with open(filepath, "rb") as f_sux:
		while (data := f_sux.read(1)):
			r = int.from_bytes(data, byteorder='little')
			g = int.from_bytes(f_sux.read(1), byteorder='little')
			b = int.from_bytes(f_sux.read(1), byteorder='little')
			a = int.from_bytes(f_sux.read(1), byteorder='little')
			
			# Set the pixel color
			pixels[x, y] = (r, g, b, a)
			
			x += 1
			if x >= width:
				x = 0
				y += 1
	
	print(y)
	
	# Save the image as an 8-bit PNG file
	image.save("output/" + filename + ".png", "PNG")


def main():
	gen_image("files/gamespy_128x64_block_1.sux.2", 128, 64)

main()