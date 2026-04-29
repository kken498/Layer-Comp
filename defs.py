import bpy
import re
import os

def get_addon_preference(context):
	addon_prefs = context.preferences.addons[__package__].preferences
	return addon_prefs

def offset_node(node_group, offset_node, type, offset):
	for node in node_group.nodes:
		if node.parent == offset_node.parent and node != offset_node:
			if type == 'X':
				if node.location[0] >= offset_node.location[0] - 1:
					node.location[0] = node.location[0] + offset
			elif type == 'Y':
				if node.location[1] >= offset_node.location[1] - 101:
					node.location[1] = node.location[1] + offset				

def get_scene_compositor(context):
	compositor = []
	for node in bpy.data.node_groups:
		if node.compositor_props.name != "":
			compositor.append(node.name)
	return compositor

def get_scene_tree(context):
	tree = context.scene.compositing_node_group
	return tree

def get_all_icon():
	icon_items = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.items()
	icon_dict = {tup[1].identifier: tup[1].value for tup in icon_items}
	i = 0
	list = []
	for identifier, value in icon_dict.items():
		list.append((identifier, '', '', identifier, i))
		i+1
	return list

def unique_name(base_name, existing_names):
    if base_name not in existing_names:
        return base_name

    match = re.match(r"^(.*?)(\.(\d+))?$", base_name)
    if match:
        base = match.group(1)
        number = int(match.group(3)) if match.group(3) else 1

        while f"{base}.{number:03d}" in existing_names:
            number += 1

        return f"{base}.{number:03d}"
    else:
        return base_name

def append_node(type, name, preset, nodes):
	filepath = get_filepath(type)
	blendfile = os.path.join(filepath, f'{preset}.blend')

	if name not in bpy.data.node_groups:
		with bpy.data.libraries.load(blendfile) as (data_from, data_to):
			data_to.node_groups = [name]

	node_group = bpy.data.node_groups[name]
	new_node = nodes.new("CompositorNodeGroup")
	new_node.node_tree = node_group

	return new_node

def get_presets(type):
	presets = []
	filepath = get_filepath(type)
	for item in os.listdir(filepath):
		if not item.startswith('.') and item.endswith('.blend') :
			presets.append(item.replace(".blend", ""))
	return presets

def get_presets_item(preset, type):
	items = []
	filepath = get_filepath(type)
	blendfile  = os.path.join(filepath, f"{preset}.blend")
	with bpy.data.libraries.load(blendfile, link=False) as (data_from, data_to):
		for node_group in data_from.node_groups:
			items.append(node_group)
		
	return items

def get_filepath(type):
	filepath = os.path.dirname(os.path.abspath(__file__))
	blendfolder = os.path.join(filepath, "Blends", type)
	return blendfolder

def convert_node_data(node, convert_node):
	if node.type not in ["IMAGE","TEXTURE"]:
		for attr in node.bl_rna.properties.keys():
			if attr not in ['name', 'location', 'location_absolute', 'parent']:
				if hasattr(node, attr) and not node.bl_rna.properties[attr].is_readonly:
					setattr(convert_node, attr, getattr(node, attr))

	if node.type in ["IMAGE", "TEXTURE"]:
		if node.type == "IMAGE":
			convert_node.image = node.image
		elif node.type == "TEXTURE":
			convert_node.texture = node.texture

	for i, inputs in enumerate(node.inputs):
		convert_node.inputs[i].default_value = node.inputs[i].default_value
	for i, outputs in enumerate(node.outputs):
		convert_node.outputs[i].default_value = node.outputs[i].default_value

def get_inputs(node):
	inputs = None
	if node.inputs.get('Image'):
		inputs = node.inputs['Image']
	elif node.inputs.get('Color'):
		inputs = node.inputs['Color']
	elif node.inputs.get('Background'):
		inputs = node.inputs['Background']
	elif node.inputs.get('Fac'):
		inputs = node.inputs['Fac']
	elif node.inputs:
		inputs = node.inputs[0]
	return inputs

def get_outputs(node, item):
	if item:
		outputs = node.outputs[item.channel]
	else:
		if node.outputs.get('Image'):
			outputs = node.outputs['Image']
		elif node.outputs.get('Color'):
			outputs = node.outputs['Color']
		elif node.outputs.get('Fac'):
			outputs = node.outputs['Fac']
		else:
			outputs = node.outputs[0]

	return outputs

def get_mix_node_inputs(mix_node, input):
	if input == 0:
		inputs = mix_node.inputs[1]
	elif input == 1:
		inputs = mix_node.inputs[2]
	elif input == 2:
		inputs = mix_node.inputs[3]
	return inputs

def get_mix_node_outputs(mix_node):
	outputs = mix_node.outputs['Mix']
	return outputs

def get_invert_node_inputs(invert_node, input, value):
	if input == 'Color':
		invert_node.inputs[2].default_value = value
	elif input == 'Alpha':
		invert_node.inputs[3].default_value = value