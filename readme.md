# Battlefield 2: Modern Combat Extractor

This is a project to extract the files out of the ps2/xbox 360 game.

The following version has been tested for PS2:
* US
* V2.01
* V1.00
* BETA

It has capability to extract:
* .viv: packed EA files
* .cat: Packed DICE files
* .lnd: Landscape files
* .sgf: 3d Models
* .txt: Client and Static Geometry
* .brs: Object descriptors

The 3d models are been exported to blender. Then all the objects are been linked to a scene.blender file to get the full map.

## Install

You need python3 to run the project with following packages:

	pip3 install bpy

You also will need 7z to extract the iso.

## How to export

	python3 export.py
