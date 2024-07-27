#!/bin/env python3

from PIL import Image

# Specify the width and height of the image
width = 128
height = 64

# Read raw pixel data from a file
with open('files/gamespy_128x64_block_1.sux.2', 'rb') as file:
    raw_data = file.read()

# Unpack the raw pixel data into a list of integers (assuming 8bpp)
pixel_data = list(raw_data)

# Define the palette colors (replace these with your actual palette colors)
palette = [
    (255, 255, 255),  # Color 0 (example: white)
    (255, 0, 0),      # Color 1 (example: red)
    (0, 255, 0),      # Color 2 (example: green)
    (0, 0, 255),      # Color 3 (example: blue)
    # Add more colors as needed
]

# Get the palette colors for each pixel index in pixel_data, ensuring index is valid
pixels = [(255, 255, 255) for _ in range(width * height)]  # Default to white

for i, index in enumerate(pixel_data):
    if 0 <= index < len(palette):
        pixels[i] = palette[index]
    else:
        print(f"Invalid pixel index: {index} at position {i}")

# Create an image from the pixel data
image = Image.new('RGB', (width, height))
image.putdata(pixels)

# Save the image as PNG
image.save('output.png')

print('Image created and saved as "output.png"')