#!/bin/env python3

from pygltflib import GLTF2, Scene, Node, Asset, Buffer
import json

def create_scene_gltf(filename):
    # Load the existing triangle model
    triangle_gltf = GLTF2.load('triangle_model.gltf')

    # Extract necessary data from the existing model
    triangle_buffers = triangle_gltf.buffers
    triangle_buffer_views = triangle_gltf.bufferViews
    triangle_accessors = triangle_gltf.accessors
    triangle_meshes = triangle_gltf.meshes

    # Define nodes for instances of the triangle mesh in the scene
    nodes = [
        Node(name="Triangle1", mesh=0, translation=[1.0, 0.0, 0.0]),
        Node(name="Triangle2", mesh=0, translation=[-1.0, 0.0, 0.0]),
		Node(children=[0, 1], name="TriangleCollection")
    ]

    # Define the scene
    scene = Scene(nodes=[0, 1])

    # Create the scene GLTF2 object
    scene_gltf = GLTF2(
        asset=Asset(),
        buffers=[
            # Adjust URI to reference the existing binary file
            Buffer(uri="triangle.bin", byteLength=triangle_buffers[0].byteLength)
        ],
        bufferViews=triangle_buffer_views,  # Include buffer views from the triangle model
        accessors=triangle_accessors,  # Include accessors from the triangle model
        meshes=triangle_meshes,  # Include meshes from the triangle model
        nodes=nodes,
        scenes=[scene],
        scene=0  # Set the default scene
    )

    scene_gltf.save(filename)

create_scene_gltf("scene.gltf")