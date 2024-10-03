import os
import bpy
import json

from lib.functions import modify_file_path

def create_object(data_to, collection, suffix, location, rotation):
	for i, obj in enumerate(data_to.objects):
		obj_override = obj.override_create(remap_local_usages=True)
		
		if(obj_override.parent == None):
			obj_override.location = location
			obj_override.rotation_euler = rotation
			obj_override.name = f"{obj.name}_{suffix}"
		else:
			obj_override.name = f"{obj.name}_{suffix}_{i}"
		
		collection.objects.link(obj_override)

def load_blend(cube_blend_path, obj_name, json_instances):
	with bpy.data.libraries.load(cube_blend_path, link=True, relative=True) as (data_from, data_to):
		data_to.objects = data_from.objects
	
	collection = bpy.data.collections.new(obj_name)
	bpy.context.scene.collection.children.link(collection)
	
	for i, json_instance in enumerate(json_instances):
		position = json_instance["pos"]
		rotation = json_instance["rot"]
		
		new_position = (-position["x"], position["z"], position["y"])
		new_rotation = (-rotation["x"], rotation["z"], rotation["y"])
		
		create_object(data_to, collection, i, new_position, new_rotation)

def update_library_paths(output_directory, levels_directory, cats_directory):
	for lib in bpy.data.libraries:
		if lib.filepath:
			if levels_directory in lib.filepath:
				lib.filepath = lib.filepath.replace(levels_directory, levels_directory.replace(output_directory, "//../../"))
				
				print(f"Updated library: {lib.filepath}")
			elif cats_directory in lib.filepath:
				lib.filepath = lib.filepath.replace(cats_directory, "//")
				
				print(f"Updated library: {lib.filepath}")

CAT_FILES = [
	"resources.cat",
	"resourcescapturetheflag.cat",
	"resourcesCaptureTheFlag.cat",
	"resourcesconquest.cat",
	"resourcesConquest.cat"
]

def export_scene(output_directory, level_name):
	levels_directory = f"{output_directory}/DATA.ARK/Border/Levels/{level_name}".replace("//", "/")
	cats_directory = f"{output_directory}/Levels/{level_name}/".replace("//", "/")
	
	## Clear existing data
	bpy.ops.wm.read_factory_settings(use_empty=True)
	
	map_settings = [
		{ "pos": {"x": 0.0,    "y": 0.0, "z": 0.0    }, "rot": {"x": 0.0, "y": 0.0, "z": 0.0} },
		{ "pos": {"x": 2048.0, "y": 0.0, "z": 0.0    }, "rot": {"x": 0.0, "y": 0.0, "z": 0.0} },
		{ "pos": {"x": 2048.0, "y": 0.0, "z": 2048.0 }, "rot": {"x": 0.0, "y": 0.0, "z": 0.0} },
		{ "pos": {"x": 0.0,    "y": 0.0, "z": 2048.0 }, "rot": {"x": 0.0, "y": 0.0, "z": 0.0} }
	]
	
	map_model = f"{levels_directory}/MeshTerrain/MeshData/ps2_high.lnd.blend"
	#print(f"map_model = {map_model}")
	load_blend(map_model, f"Render_Land", map_settings)
	
	with open(f"{levels_directory}/level_client_static_geometry.txt.json", 'r') as f_json:
		static_geometry = json.load(f_json)
		
		for json_component in static_geometry["components"]:
			model = json_component["model"]
			
			model_file_path = modify_file_path(model) + ".blend"
			
			found = False
			
			for cat_file in CAT_FILES:
				file_path = f"{cats_directory}/{cat_file}/{model_file_path}"
				
				#print(f"file_path = {file_path}")

				if os.path.exists(file_path):
					print(f"Found: model = {model}")
					obj_name = model.split(":")[1]
					
					print(f"load_blend \"{file_path}\"")
					load_blend(file_path, obj_name, json_component["instances"])
					print("Done!")
					
					found = True
					
					break
			
			if(found == False):
				print(f"Not Found: {model_file_path}")
	
	## Update library paths
	update_library_paths(output_directory, levels_directory, cats_directory)
	
	## Update view distance
	for area in bpy.context.screen.areas:
		if area.type == 'VIEW_3D':
			for space in area.spaces:
				if space.type == 'VIEW_3D':
					space.clip_end = 10000.0
	
	## Save blender file
	bpy.ops.wm.save_as_mainfile(filepath=f"{cats_directory}/scene.blend")
