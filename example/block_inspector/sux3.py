#!/bin/env python3

from lib.PS2Textures import write_tex_psmct32, read_tex_psmt8
from PIL import Image

width, height = 128, 64

with open('files/gamespy_128x64_block_1.sux', 'rb') as block_1:
	with open('files/gamespy_128x64_block_2.sux', 'rb') as block_2:
		swizzled_data = block_1.read()
		
		rrw = width // 2
		rrh = height // 2
		
		## unswizzle data
		write_tex_psmct32(0, 0, 0, 0, rrw, rrh, swizzled_data);
		unswizzled_data = read_tex_psmt8(0, 0, 0, 0, width, height);
		
		palette = block_2.read()

		# Create a new image with RGBA mode (4 channels: Red, Green, Blue, Alpha)
		image = Image.new('RGBA', (width, height))
		
		# Get the pixel access object
		pixels = image.load()
		
		index = 0
		for y in range(height):
			for x in range(width):
				palette_index = unswizzled_data[index] * 4
				pixel = palette[palette_index:palette_index+4]
				
				r = pixel[0]
				g = pixel[1]
				b = pixel[2]
				a = pixel[3]
				
				pixels[x, y] = (r, g, b, a)
				
				index += 1
				
				"""
				if(x == 0 and y == 0):
					print("palette_index = {}".format(palette_index))
					print("pixel = {}".format(pixel))
					print("r = {}".format(r))
					print("g = {}".format(g))
					print("b = {}".format(b))
					print("a = {}".format(a))
				"""
		
		# Save the image as an 8-bit PNG file
		image.save("output/gamespy_128x64.png", "PNG")