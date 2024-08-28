import os
import struct
import json
import math

from lib.dice.serialize import Dice_UnSerialize

def clean_nan(obj):
    if isinstance(obj, float):
        return None if math.isnan(obj) else obj
    elif isinstance(obj, list):
        return [clean_nan(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif is_dataclass(obj):
        return clean_nan(asdict(obj))
    return obj

class CustomEncoder(json.JSONEncoder):
	def default(self, obj):
		if is_dataclass(obj):
			return clean_nan(asdict(obj))
		return super().default(obj)

def export_beta_level_static_geometry_txt(input_file_path, output_file_path, is_client = True):
	static_geometry = {}
	
	with open(input_file_path, 'r') as f_txt:
		content = f_txt.read()

		static_geometry = Dice_UnSerialize(content)

		static_geometry["components"] = static_geometry.pop("staticComponentsList")
		
		for component in static_geometry["components"]:
			component["version"] = component["descriptor"].pop("version")
			component["primaryCollision"] = component["descriptor"].pop("primaryCollision")
			component["secondaryCollision"] = component["descriptor"].pop("secondaryCollision")
			component["model"] = component["descriptor"].pop("model")

			component["instances"] = component.pop("instancePositions")

			# Remove the "descriptor" property
			del component["descriptor"]

	## Write Static Geometry
	with open(output_file_path, 'w') as f_json:
		json.dump(static_geometry, f_json, cls=CustomEncoder)

