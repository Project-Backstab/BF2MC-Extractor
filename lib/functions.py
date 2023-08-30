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
