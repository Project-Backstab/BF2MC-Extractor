#!/bin/env python3

import os
import json
import random
import bpy

def create_mesh(mesh_name, json_mesh):
	# Create a mesh data block
	mesh = bpy.data.meshes.new(mesh_name)

	vertices = []
	for vertex in json_mesh["vertices"]:
		position = vertex["position"]
		vertices.append((-position[0], position[2], position[1]))
	
	faces = []
	for face in json_mesh["faces"]:
		faces.append((face[0], face[1], face[2]))
	
	# Assign geometry to the mesh
	mesh.from_pydata(vertices, [], faces)
	mesh.update()
	
	return mesh

def create_object(json_object, obj_name, big_parent, materials):
	parent = None
	
	for i in range(len(json_object["meshes"])):
		json_mesh = json_object["meshes"][i]
		
		mesh = create_mesh(f"{obj_name}_mesh_{i}", json_mesh)
		
		obj = bpy.data.objects.new(f"{obj_name}_object_{i}", mesh)
		
		## Find material by index
		material = materials[json_mesh["material_index"]]
		
		## Add material to obj
		obj.data.materials.append(material)
		
		if(i == 0):
			obj.parent = big_parent
			parent = obj
		else:
			obj.parent = parent
		
		bpy.context.scene.collection.objects.link(obj)

def export_static_model_2_blend(input_file_path, output_file_path):
	with open(input_file_path, 'r') as f_json:
		static_model = json.load(f_json)
		
		if(static_model["class_name"] != "StaticModel" and static_model["class_name"] != "@StaticModel"):
			return
		
		## Clear existing data
		bpy.ops.wm.read_factory_settings(use_empty=True)
		
		## Create materials
		materials = []
		for json_material in static_model["materials"]:
			material = bpy.data.materials.new(name = json_material["name"])
			material.use_nodes = True
			
			## Color
			nodes = material.node_tree.nodes
			principled_node = nodes.get('Principled BSDF')
			if(principled_node):
				principled_node.inputs['Base Color'].default_value = (random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), random.uniform(0.0, 1.0), 1)  # Red color
				
				"""
				image_path = "files/image.jpg"  # Replace with the path to your texture image
				image = bpy.data.images.load(image_path)
				texture_node = nodes.new('ShaderNodeTexImage')
				texture_node.image = image

				# Step 4: Connect the Image Texture node to the Base Color input of the Principled BSDF node
				material.node_tree.links.new(texture_node.outputs['Color'], principled_node.inputs['Base Color'])
				"""
			
			## Culling
			material.use_backface_culling = False
			
			materials.append(material)

		obj_name = static_model["file_path"].split(":")[1]
		
		## Create biggest parent
		mesh = bpy.data.meshes.new(f"{obj_name}_mesh")
		big_parent = bpy.data.objects.new(f"{obj_name}", mesh)
		bpy.context.scene.collection.objects.link(big_parent)
		
		for json_object in static_model["objects"]:
			create_object(json_object, obj_name, big_parent, materials)

		# Save the .blend file
		bpy.ops.wm.save_as_mainfile(filepath=output_file_path)
		
		#bpy.ops.export_scene.gltf(filepath=f"{output_file_path}.gltf")