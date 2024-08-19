#!/bin/env python3

import os
import sys

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from lib.sgf import export_sgf, export_sgf_beta

def main():
	is_beta = True
	
	for root, dirs, files in os.walk('output/'):
		for file in files:
			if file.endswith('.sgf'):
				input_file_path = os.path.join(root, file)
				output_file_path = f"{input_file_path}.json"
				
				print(f"Export \"{input_file_path}\"")
				if(is_beta):
					export_sgf_beta(input_file_path, output_file_path)
				else:
					export_sgf(input_file_path, output_file_path)
				print("Done!")

if __name__ == "__main__":
    main()