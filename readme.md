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


You need python3.11 and 7z to run the project.

```bash
	sudo apt update
	sudo apt install -y software-properties-common
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt update
```
```
	sudo apt install -y \
	  python3.11 python3.11-distutils python3.11-dev \
	  python3-pip p7zip-full \
	  build-essential git cmake ninja-build \
	  libx11-dev libxxf86vm-dev libxrandr-dev libxi-dev \
	  libasound2-dev libopenal-dev libsndfile1-dev \
	  libjpeg-dev libpng-dev libtiff5-dev libopenexr-dev \
	  libglu1-mesa-dev libglew-dev libssl-dev
```

Install pip for Python3.11
```
	curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
	sudo python3.11 /tmp/get-pip.py
```

Install additional depdendencies including the Blender bpy module.
```
	sudo python3.11 -m pip install --upgrade pip setuptools wheel
	sudo python3.11 -m pip install \
	  numpy<2.0 \
	  Pillow \
	  bpy
```

Verify bpy is installed

```
	python3.11 -c "import bpy; print('Loaded bpy, Blender', bpy.app.version_string)"

```
→ Loaded bpy, Blender 4.4.0

Within the BF2MC-Extractor folder create a directory called 'files'
```
	~/BF2MC-Extractor/files
```

Drop your ISO here and refer to config.py to comment in/out the version of game you are extracting. Pay attention to the .iso naming here.

## How to export

	python3.11 export.py
