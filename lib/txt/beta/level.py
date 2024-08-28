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

def export_beta_level_txt(input_file_path, output_file_path, is_client = True):
	level = {}
	
	with open(input_file_path, 'r') as f_txt:
		content = f_txt.read()

		level = Dice_UnSerialize(content)

		level["components"] = level.pop("objectInstances")

		for component in level["components"]:
			component["resource_name"] = component.pop("descriptorName")
			component["class_name"] = component["descriptor"].pop("className")
			
			if "meshDescriptors" in component["descriptor"]:
				component["version"] = component["descriptor"].pop("version")
				component["meshs"] = component["descriptor"].pop("meshDescriptors")
				component["rigidBodyDescriptor"] = component["descriptor"].pop("rigidBodyDescriptor")
				component["soundScript"] = component["descriptor"].pop("soundScript")
				component["ambientAnimated"] = component["descriptor"].pop("ambientAnimated")
				component["usesIndoorLighting"] = component["descriptor"].pop("usesIndoorLighting")
			else:
				component["meshs"] = [
					{
						"class_name": "",
						"resource_name": component["descriptor"].pop("meshDescriptor"),
					}
				]
			

			component["instances"] = component.pop("instancePositions")

			# Remove the "descriptor" property
			del component["descriptor"]

	## Write Static Geometry
	with open(output_file_path, 'w') as f_json:
		json.dump(level, f_json, cls=CustomEncoder)

