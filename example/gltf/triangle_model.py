#!/bin/env python3

from pygltflib import GLTF2, Buffer, BufferView, Accessor, Mesh, Primitive, Node, Scene
import numpy as np
from enum import Enum

class ComponentType(Enum):
    BYTE = 5120
    UNSIGNED_BYTE = 5121
    SHORT = 5122
    UNSIGNED_SHORT = 5123
    UNSIGNED_INT = 5125
    FLOAT = 5126

def create_triangle_model_gltf(filename):
    gltf = GLTF2()

    # Define the vertices of the triangle
    vertex_data = np.array([
        0.0,  0.5, 0.0,  # Vertex 1
       -0.5, -0.5, 0.0,  # Vertex 2
        0.5, -0.5, 0.0   # Vertex 3
    ], dtype=np.float32).tobytes()

    # Define the indices for the triangle
    index_data = np.array([
        0, 1, 2  # Triangle
    ], dtype=np.uint16).tobytes()

    # Combine vertex and index data into a single buffer
    buffer_data = vertex_data + index_data

    # Create a binary buffer
    buffer = Buffer(uri="triangle.bin", byteLength=len(buffer_data))
    gltf.buffers.append(buffer)

    # Create buffer views for vertices and indices
    buffer_view_vertices = BufferView(buffer=0, byteOffset=0, byteLength=len(vertex_data), target=34962)  # ARRAY_BUFFER
    buffer_view_indices = BufferView(buffer=0, byteOffset=len(vertex_data), byteLength=len(index_data), target=34963)  # ELEMENT_ARRAY_BUFFER
    gltf.bufferViews.extend([buffer_view_vertices, buffer_view_indices])

    # Create accessors for vertices and indices
    accessor_positions = Accessor(bufferView=0, byteOffset=0, componentType=ComponentType.FLOAT, count=3, type="VEC3", max=[0.5, 0.5, 0.0], min=[-0.5, -0.5, 0.0])
    accessor_indices = Accessor(bufferView=1, byteOffset=0, componentType=ComponentType.UNSIGNED_SHORT, count=3, type="SCALAR", max=[2], min=[0])
    gltf.accessors.extend([accessor_positions, accessor_indices])

    # Create the mesh with a single primitive
    primitive = Primitive(attributes={"POSITION": 0}, indices=1, mode=4)  # TRIANGLES
    mesh = Mesh(primitives=[primitive])
    gltf.meshes.append(mesh)

    # Create nodes for two instances of the mesh
    node1 = Node(mesh=0, translation=[0, 0, 0])  # Position 1
    node2 = Node(mesh=0, translation=[2, 0, 0])  # Position 2
    gltf.nodes.extend([node1, node2])

    # Create a scene with the two nodes
    scene = Scene(nodes=[0, 1])
    gltf.scenes.append(scene)
    gltf.scene = 0

    # Save the GLTF file
    with open(filename, "w") as f:
        import json
        json.dump(gltf.to_dict(), f, indent=2)  # Save JSON data with pretty print

    # Write the binary data to the file
    with open("triangle.bin", "wb") as f:
        f.write(buffer_data)

create_triangle_model_gltf("triangle_model.gltf")