import bpy
import importlib
from pathlib import Path
import os
from typing import List, Tuple, Type

def create_transform_node_group():
	__transform = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = ".*Transform")

	__transform.color_tag = 'NONE'
	__transform.description = ""
	__transform.default_group_node_width = 140
	

	#__transform interface
	#Socket Image
	image_socket = __transform.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
	image_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
	image_socket.attribute_domain = 'POINT'

	#Socket Image
	image_socket_1 = __transform.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
	image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
	image_socket_1.attribute_domain = 'POINT'
	image_socket_1.hide_value = True

	#Socket X
	x_socket = __transform.interface.new_socket(name = "X", in_out='INPUT', socket_type = 'NodeSocketFloat')
	x_socket.default_value = 0.0
	x_socket.min_value = -10000.0
	x_socket.max_value = 10000.0
	x_socket.subtype = 'NONE'
	x_socket.attribute_domain = 'POINT'

	#Socket Y
	y_socket = __transform.interface.new_socket(name = "Y", in_out='INPUT', socket_type = 'NodeSocketFloat')
	y_socket.default_value = 0.0
	y_socket.min_value = -10000.0
	y_socket.max_value = 10000.0
	y_socket.subtype = 'NONE'
	y_socket.attribute_domain = 'POINT'

	#Socket Rotate
	rotate_socket = __transform.interface.new_socket(name = "Rotate", in_out='INPUT', socket_type = 'NodeSocketFloat')
	rotate_socket.default_value = 0.0
	rotate_socket.min_value = -10000.0
	rotate_socket.max_value = 10000.0
	rotate_socket.subtype = 'ANGLE'
	rotate_socket.attribute_domain = 'POINT'

	#Socket X
	x_socket_1 = __transform.interface.new_socket(name = "X", in_out='INPUT', socket_type = 'NodeSocketFloat')
	x_socket_1.default_value = 1.0
	x_socket_1.min_value = 9.999999747378752e-05
	x_socket_1.max_value = 12000.0
	x_socket_1.subtype = 'NONE'
	x_socket_1.attribute_domain = 'POINT'

	#Socket Y
	y_socket_1 = __transform.interface.new_socket(name = "Y", in_out='INPUT', socket_type = 'NodeSocketFloat')
	y_socket_1.default_value = 1.0
	y_socket_1.min_value = 9.999999747378752e-05
	y_socket_1.max_value = 12000.0
	y_socket_1.subtype = 'NONE'
	y_socket_1.attribute_domain = 'POINT'


	#initialize __transform nodes
	#node Group Output
	group_output = __transform.nodes.new("NodeGroupOutput")
	group_output.name = "Group Output"
	group_output.is_active_output = True

	#node Group Input
	group_input = __transform.nodes.new("NodeGroupInput")
	group_input.name = "Group Input"

	
	#node Scale
	scale = __transform.nodes.new("CompositorNodeScale")
	scale.name = "Scale"

	#node Rotate
	rotate = __transform.nodes.new("CompositorNodeRotate")
	rotate.name = "Rotate"

	#node Translate
	translate = __transform.nodes.new("CompositorNodeTranslate")
	translate.name = "Translate"

	scale.frame_method = 'STRETCH'
	scale.space = 'RELATIVE'

	rotate.filter_type = 'BILINEAR'

	translate.interpolation = 'NEAREST'
	translate.use_relative = False
	translate.wrap_axis = 'NONE'

	#Set locations
	group_output.location = (350.03118896484375, 0.0)
	group_input.location = (-360.0312194824219, 0.0)
	scale.location = (-160.03121948242188, 0.6955108642578125)
	rotate.location = (-4.1747283935546875, -0.6955108642578125)
	translate.location = (160.03121948242188, -0.6954803466796875)

	#Set dimensions
	group_output.width, group_output.height = 140.0, 100.0
	group_input.width, group_input.height = 140.0, 100.0
	scale.width, scale.height = 140.0, 100.0
	rotate.width, rotate.height = 140.0, 100.0
	translate.width, translate.height = 140.0, 100.0

	#initialize __transform links
	#rotate.Image -> translate.Image
	__transform.links.new(rotate.outputs[0], translate.inputs[0])
	#scale.Image -> rotate.Image
	__transform.links.new(scale.outputs[0], rotate.inputs[0])
	#translate.Image -> group_output.Image
	__transform.links.new(translate.outputs[0], group_output.inputs[0])
	#group_input.Image -> scale.Image
	__transform.links.new(group_input.outputs[0], scale.inputs[0])
	#group_input.X -> translate.X
	__transform.links.new(group_input.outputs[1], translate.inputs[1])
	#group_input.Y -> translate.Y
	__transform.links.new(group_input.outputs[2], translate.inputs[2])
	#group_input.Rotate -> rotate.Degr
	__transform.links.new(group_input.outputs[3], rotate.inputs[1])
	#group_input.X -> scale.X
	__transform.links.new(group_input.outputs[4], scale.inputs[1])
	#group_input.Y -> scale.Y
	__transform.links.new(group_input.outputs[5], scale.inputs[2])
	return __transform

def create_mix_node(node_group):
	version = bpy.app.version
	if version >= (4, 5, 0):
		mix_node = node_group.nodes.new("ShaderNodeMix")
		mix_node.data_type = 'RGBA'
	elif version < (4, 5, 0):
		mix_node = node_group.nodes.new("CompositorNodeMixRGB")
		mix_node.use_alpha = True
		mix_node.use_clamp = True
	return mix_node

def get_mix_node_inputs(mix_node, input):
	version = bpy.app.version
	if version >= (5, 0, 0):
		if input == 0:
			inputs = mix_node.inputs[1]
		elif input == 1:
			inputs = mix_node.inputs[2]
		elif input == 2:
			inputs = mix_node.inputs[3]
	elif version >= (4, 5, 0) and version < (5, 0, 0):
		if input == 0:
			inputs = mix_node.inputs[0]
		elif input == 1:
			inputs = mix_node.inputs[6]
		elif input == 2:
			inputs = mix_node.inputs[7]
	elif version < (4, 5, 0):
		inputs = mix_node.inputs[input]
	return inputs

def get_mix_node_outputs(mix_node):
	version = bpy.app.version
	if version >= (5, 0, 0):
		outputs = mix_node.outputs['Mix']
	elif version >= (4, 5, 0) and version < (5, 0, 0):
		outputs = mix_node.outputs['Result']
	elif version < (4, 5, 0):
		outputs = mix_node.outputs[0]
	return outputs

def get_invert_node_inputs(invert_node, input, value):
	version = bpy.app.version
	if version >= (4, 5, 0):
		if input == 'Color':
			invert_node.inputs[2].default_value = value
		elif input == 'Alpha':
			invert_node.inputs[3].default_value = value
	elif version < (4, 5, 0):
		if input == 'Color':
			invert_node.invert_rgb = value
		elif input == 'Alpha':
			invert_node.invert_alpha = value

class Node:
	def free(self):
		if self.node_tree.users == 1:
			bpy.data.node_groups.remove(self.node_tree, do_unlink=True)

	def addSocket(self, is_output, sockettype, name):
		if is_output == True:
			socket = self.node_tree.interface.new_socket(
				name, in_out="OUTPUT", socket_type=sockettype
			)
		else:
			socket = self.node_tree.interface.new_socket(
				name, in_out="INPUT", socket_type=sockettype
			)

		return socket
	
class Mix_Node:
	blend_items=(('MIX', 'Mix', 'Mix'),
		('DARKEN', 'Darken', 'Darken'),
		('MULTIPLY', 'Multiply', 'Multiply'),
		('BURN', 'Color Burn', 'Burn'),
		('LIGHTEN', 'Lighten', 'Lighten'),
		('DODGE', 'Color Dodge', 'Color Dodge'),
		('ADD', 'Add', 'Add'),
		('OVERLAY', 'Overlay', 'Overlay'),
		('SOFT_LIGHT', 'Soft Light', 'Soft Light'),
		('LINEAR_LIGHT', 'Linear Light', 'Linear Light'),
		('DIFFERENCE', 'Difference', 'Difference'),
		('EXCLUSION', 'Exclusion', 'Exclusion'),
		('SUBTRACT', 'Subtract', 'Subtract'),
		('DIVIDE', 'Divide', 'Divide'),
		('HUE', 'Hue', 'Hue'),
		('SATURATION', 'Saturation', 'Saturation'),
		('COLOR', 'Color', 'Color'),
		('VALUE', 'Value', 'Value'),
		)

	def update_blend(self, context):
		if self.node_tree:
			self.node_tree.nodes["Mix"].blend_type = self.blend_type

	blend_type : bpy.props.EnumProperty(default = 'MIX', items = blend_items, name = "Blend", update = update_blend)

class NodeLib:
	BASE_DIR = Path(os.path.join(os.path.dirname(os.path.abspath(__file__))))

	@staticmethod
	def get_node() -> List[Type]:
		"""Safely retrieve node definitions"""
		try:
			return NodeLib()()
		except Exception as e:
			print(f"Error loading node definitions: {e}")
			return []
		
	@staticmethod
	def import_classes_from_folder(folder_path):

		folder_name = folder_path.name
		imported_classes = []
		prefix = "CompositorNode"

		# Pre-fetch all .py files
		py_files = [
			f
			for f in folder_path.iterdir()
			if f.suffix == ".py" and f.stem not in {"__init__", "_utils"}
		]

		for py_file in py_files:
			module_name = f".{folder_name}.{py_file.stem}"

			try:
				module = importlib.import_module(module_name, package=__package__)
			except ImportError as e:
				continue

			for attr_name, attr in module.__dict__.items():
				if (
					isinstance(attr, type)
					and attr_name.startswith(prefix)
					and attr_name != prefix
				):
					imported_classes.append(attr)
				
		return imported_classes

	@classmethod
	def __call__(cls):
		version = bpy.app.version

		if version >= (4, 5, 0):
			folder = cls.BASE_DIR / "node_v4_5"
		elif version < (4, 5, 0):
			folder = cls.BASE_DIR / "node_v4_4_below"
			
		classes = cls.import_classes_from_folder(folder)

		return classes

def register():
	if bpy.app.version < (5, 0, 0):
		nodes = NodeLib.get_node()
		for cls in nodes:
			bpy.utils.register_class(cls)

def unregister():
	if bpy.app.version < (5, 0, 0):
		nodes = NodeLib.get_node()
		for cls in nodes:
			bpy.utils.unregister_class(cls)