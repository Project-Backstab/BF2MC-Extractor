#!/bin/env python3

import os
import json
import random
import bpy

def create_mesh(mesh_name, json_grid):
	# Create a mesh data block
	mesh = bpy.data.meshes.new(mesh_name)

	vertices = []
	for vertex in json_grid["vertices"]:
		if ("z_check" in vertex and vertex["z_check"] == False):
			continue
		
		x = vertex["x"]
		y = vertex["y"]
		z = vertex["z"]
		
		vertices.append((x, z, y))
	
	faces = []
	for face in json_grid["faces"]:
		faces.append((face[0], face[1], face[2]))
	
	# Assign geometry to the mesh
	mesh.from_pydata(vertices, [], faces)
	mesh.update()
	
	return mesh

def create_object(json_grid, obj_name, parent):		
	x = int(json_grid["x"])
	y = int(json_grid["z"])
	
	print(f"{obj_name}_{x}_{y}")
	
	mesh = create_mesh(f"{obj_name}_mesh_{x}_{y}", json_grid)
	
	obj = bpy.data.objects.new(f"{obj_name}_object_{x}_{y}", mesh)

	# Add a mirror modifier to the object
	mirror_modifier = obj.modifiers.new(name="Mirror", type='MIRROR')

	# Enable mirror on the X and Y axes
	mirror_modifier.use_axis[0] = True  # X axis
	mirror_modifier.use_axis[1] = True  # Y axis
	
	obj.parent = parent
		
	bpy.context.scene.collection.objects.link(obj)

def export_lnd_2_blend(input_file_path, output_file_path):
	with open(input_file_path, 'r') as f_json:
		land = json.load(f_json)
		
		## Clear existing data
		bpy.ops.wm.read_factory_settings(use_empty=True)
		
		obj_name = "Render_Land"
		
		## Create biggest parent
		mesh = bpy.data.meshes.new(f"{obj_name}_mesh")
		parent = bpy.data.objects.new(f"{obj_name}", mesh)
		bpy.context.scene.collection.objects.link(parent)
		
		for json_grid in land["grids"]:
			create_object(json_grid, obj_name, parent)

		for area in bpy.context.screen.areas:
			if area.type == 'VIEW_3D':
				for space in area.spaces:
					if space.type == 'VIEW_3D':
						space.clip_end = 10000.0

		# Save the .blend file
		bpy.ops.wm.save_as_mainfile(filepath=output_file_path)
		