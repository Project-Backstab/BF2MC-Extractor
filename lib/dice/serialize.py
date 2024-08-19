import re
import json

# Regex patterns to match the variable name, length, and items
array_pattern = re.compile(r'(\w+)\s*:\s*length\s*=\s*(\d+)')
array_item_pattern = re.compile(r'item\s+(\d+)')
class_pattern = re.compile(r'(\w+)\s*:\s*className\s*=\s*"([^"]*)"')
coordinate_pattern = re.compile(r'(\w+)\s*:\s*(-?\d+\.\d+);(-?\d+\.\d+);(-?\d+\.\d+)')
string_pattern = re.compile(r'(\w+)\s*:\s*"([^"]*)"')
float_pattern = re.compile(r'(\w+)\s*:\s*(-?\d+\.\d+)')
integer_pattern = re.compile(r'(\w+)\s*:\s*(-?\d+)')
value_pattern = re.compile(r'(\w+)\s*:\s*(.*)')

def parse_array(lines, i):
	items = []

	while i < len(lines) and not lines[i].strip().startswith('}'):
		line = lines[i].strip()

		if array_item_pattern.match(line):
			i, item = parse_value(lines, i + 2)
			items.append(item)
		
		i += 1

	return i, items

def parse_value(lines, i):
	obj = {}

	while i < len(lines) and not lines[i].strip().startswith('}'):
		line = lines[i].strip()

		array_match = array_pattern.match(line)
		class_match = class_pattern.match(line)
		coordinate_match = coordinate_pattern.match(line)
		string_match = string_pattern.match(line)
		float_match = float_pattern.match(line)
		integer_match = integer_pattern.match(line)
		value_match = value_pattern.match(line)

		# Array
		if array_match:
			name = array_match.group(1)
			i, items = parse_array(lines, i + 2)
			obj[name] = items
		
		# Class
		elif class_match:
			name = class_match.group(1)
			class_value = class_match.group(2)
			i, value = parse_value(lines, i + 2)
			value["className"] = class_value
			obj[name] = value
		
		# Coordinate
		elif coordinate_match:
			name = coordinate_match.group(1)
			x, y, z = coordinate_match.groups()[1:]
			obj[name] = {"x": float(x), "y": float(y), "z": float(z)}

		# String
		elif string_match:
			name = string_match.group(1)
			value = string_match.group(2)
			obj[name] = value
		
		# Float
		elif float_match:
			name = float_match.group(1)
			value = float_match.group(2)
			obj[name] = float(value)
		
		# Value
		elif integer_match:
			name = integer_match.group(1)
			value = integer_match.group(2)
			obj[name] = int(value)
		
		# Value
		elif value_match:
			name = value_match.group(1)
			value = value_match.group(2)
			obj[name] = value
		
		# Object
		elif(i + 1 < len(lines) and lines[i + 1].strip().startswith('{')):
			i, value = parse_value(lines, i + 2)
			obj[line] = value
		
		i += 1

	return i, obj

def Dice_UnSerialize(content):
	lines = content.splitlines()
	
	_, obj = parse_value(lines, 0)
	
	return obj

def Dice_UnSerializeFile(input_file_path, output_file_path):
	with open(input_file_path, 'r') as file:
		content = file.read()

		data = Dice_UnSerialize(content)
		
		with open(output_file_path, "w") as json_file:
			json.dump(data, json_file, indent=4)

