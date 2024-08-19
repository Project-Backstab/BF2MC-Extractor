import os

def create_file(filepath, file_data):
	# Split the given filepath into directory path and filename
	directory_path, filename = os.path.split(filepath)

	# Create directories if they don't exist
	os.makedirs(directory_path, exist_ok=True)

	# Create the file
	file_path = os.path.join(directory_path, filename)
	with open(file_path, 'wb') as file:
		file.write(file_data)

"""
	Convert file path to new one to avoid strange symboles:
	
	Example:
		Objects/Weapons/AC/Bag/Bag.sgf:Render_Ac_OpsKit
		output/Objects/Weapons/AC/Bag/Bag.Render_Ac_OpsKit.sgf
"""
def modify_file_path(file_path):
	## fix: windows slashes
	new_file_path = file_path.replace("\\", "/")

	## Fix: capital letter cases that caused trouble extracting.
	new_file_path = new_file_path.replace("vehicles/", "Vehicles/")
	new_file_path = new_file_path.replace("Ac/", "AC/")
	new_file_path = new_file_path.replace("Ac_Pickup/", "AC_Pickup/")
	new_file_path = new_file_path.replace("US_apache/", "US_Apache/")
	new_file_path = new_file_path.replace("Ch/", "CH/")
	new_file_path = new_file_path.replace("Eu/", "EU/")
	new_file_path = new_file_path.replace("SMAWrocketlauncher/", "SMAWRocketLauncher/")
	new_file_path = new_file_path.replace("SMAWrocketlauncher", "SMAWRocketLauncher2")
	new_file_path = new_file_path.replace("L85A2Assaultrifle/", "L85A2AssaultRifle/")
	new_file_path = new_file_path.replace("US_Lav/", "US_LAV/")
	new_file_path = new_file_path.replace("sounds/", "Sounds/")
	new_file_path = new_file_path.replace("scripts/", "Scripts/")
	new_file_path = new_file_path.replace("weapons/", "Weapons/")
	
	# Split the path on the last occurrence of ":"
	path_parts = new_file_path.rsplit(':', 1)
	
	if len(path_parts) != 2:
		# If the path doesn't contain ":", return it unchanged
		return new_file_path

	path_before_colon = path_parts[0]
	path_after_colon = path_parts[1]

	# Split the path_before_colon on the last occurrence of "."
	path_parts_before_dot = path_before_colon.rsplit('.', 1)
	if len(path_parts_before_dot) != 2:
		# If the path_before_colon doesn't contain ".", return it unchanged
		return new_file_path

	base_path = path_parts_before_dot[0]
	extension = path_parts_before_dot[1]

	# Construct the new path
	new_file_path = f"{base_path}.{path_after_colon}.{extension}"
	
	return new_file_path