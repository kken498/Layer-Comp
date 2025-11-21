import bpy
from ..node import *

class CompositorNodeRenoiser(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeRenoiser'
	bl_label='Renoiser'
	bl_icon='TEXTURE'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Strength"].default_value = 1
		self.inputs["Scale"].default_value = 50
		self.inputs["Color"].default_value = 1

	def draw_buttons(self, context, layout):
		return

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"	

		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 0.5
		strength_socket.min_value = 0.0
		strength_socket.max_value = 1.0
		strength_socket.subtype = 'FACTOR'
		strength_socket.attribute_domain = 'POINT'
		strength_socket.description = "Amount of mixing between the A and B inputs"
		strength_socket.default_input = 'VALUE'
		strength_socket.structure_type = 'AUTO'

		#Socket Scale
		scale_socket = node_tree.interface.new_socket(name = "Scale", in_out='INPUT', socket_type = 'NodeSocketFloat')
		scale_socket.default_value = 50.0
		scale_socket.min_value = 1.0
		scale_socket.max_value = 200.0
		scale_socket.subtype = 'NONE'
		scale_socket.attribute_domain = 'POINT'
		scale_socket.description = "Scale of the base noise octave"
		scale_socket.default_input = 'VALUE'
		scale_socket.structure_type = 'AUTO'

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketFloat')
		color_socket.default_value = 1.0
		color_socket.min_value = 0.0
		color_socket.max_value = 1.0
		color_socket.subtype = 'FACTOR'
		color_socket.attribute_domain = 'POINT'
		color_socket.description = "Amount of mixing between the A and B inputs"
		color_socket.default_input = 'VALUE'
		color_socket.structure_type = 'AUTO'

		#Socket Sharpen
		sharpen_socket = node_tree.interface.new_socket(name = "Sharpen", in_out='INPUT', socket_type = 'NodeSocketFloat')
		sharpen_socket.default_value = 0.0
		sharpen_socket.min_value = 0.0
		sharpen_socket.max_value = 1.0
		sharpen_socket.subtype = 'FACTOR'
		sharpen_socket.attribute_domain = 'POINT'
		sharpen_socket.default_input = 'VALUE'
		sharpen_socket.structure_type = 'AUTO'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Image Coordinates.001
		image_coordinates_001 = node_tree.nodes.new("CompositorNodeImageCoordinates")
		image_coordinates_001.name = "Image Coordinates.001"

		#node Scene Time
		scene_time = node_tree.nodes.new("CompositorNodeSceneTime")
		scene_time.name = "Scene Time"

		#node Mix.004
		mix_004 = node_tree.nodes.new("ShaderNodeMix")
		mix_004.name = "Mix.004"
		mix_004.blend_type = 'OVERLAY'
		mix_004.clamp_factor = True
		mix_004.clamp_result = False
		mix_004.data_type = 'RGBA'
		mix_004.factor_mode = 'UNIFORM'

		#node Filter
		filter = node_tree.nodes.new("CompositorNodeFilter")
		filter.name = "Filter"
		filter.filter_type = 'SHARPEN'

		#node Noise Texture
		noise_texture = node_tree.nodes.new("ShaderNodeTexNoise")
		noise_texture.name = "Noise Texture"
		noise_texture.noise_dimensions = '4D'
		noise_texture.noise_type = 'FBM'
		noise_texture.normalize = True
		#Detail
		noise_texture.inputs[3].default_value = 2.0
		#Roughness
		noise_texture.inputs[4].default_value = 1.0
		#Lacunarity
		noise_texture.inputs[5].default_value = 2.0
		#Distortion
		noise_texture.inputs[8].default_value = 0.0

		#node Map Range
		map_range = node_tree.nodes.new("ShaderNodeMapRange")
		map_range.name = "Map Range"
		map_range.clamp = False
		map_range.data_type = 'FLOAT'
		map_range.interpolation_type = 'LINEAR'
		#From Min
		map_range.inputs[1].default_value = 1.0
		#From Max
		map_range.inputs[2].default_value = 200.0
		#To Min
		map_range.inputs[3].default_value = 300.0
		#To Max
		map_range.inputs[4].default_value = 50.0

		#node Mix.005
		mix_005 = node_tree.nodes.new("ShaderNodeMix")
		mix_005.name = "Mix.005"
		mix_005.blend_type = 'MIX'
		mix_005.clamp_factor = True
		mix_005.clamp_result = False
		mix_005.data_type = 'RGBA'
		mix_005.factor_mode = 'UNIFORM'

		#initialize node_tree links
		#group_input.Image -> image_coordinates_001.Image
		node_tree.links.new(group_input.outputs[0], image_coordinates_001.inputs[0])
		#filter.Image -> mix_004.A
		node_tree.links.new(filter.outputs[0], mix_004.inputs[6])
		#mix_004.Result -> group_output.Image
		node_tree.links.new(mix_004.outputs[2], group_output.inputs[0])
		#group_input.Image -> filter.Image
		node_tree.links.new(group_input.outputs[0], filter.inputs[1])
		#group_input.Sharpen -> filter.Fac
		node_tree.links.new(group_input.outputs[4], filter.inputs[0])
		#mix_005.Result -> mix_004.B
		node_tree.links.new(mix_005.outputs[2], mix_004.inputs[7])
		#image_coordinates_001.Uniform -> noise_texture.Vector
		node_tree.links.new(image_coordinates_001.outputs[0], noise_texture.inputs[0])
		#group_input.Strength -> mix_004.Factor
		node_tree.links.new(group_input.outputs[1], mix_004.inputs[0])
		#group_input.Scale -> map_range.Value
		node_tree.links.new(group_input.outputs[2], map_range.inputs[0])
		#map_range.Result -> noise_texture.Scale
		node_tree.links.new(map_range.outputs[0], noise_texture.inputs[2])
		#noise_texture.Color -> mix_005.B
		node_tree.links.new(noise_texture.outputs[1], mix_005.inputs[7])
		#noise_texture.Fac -> mix_005.A
		node_tree.links.new(noise_texture.outputs[0], mix_005.inputs[6])
		#group_input.Color -> mix_005.Factor
		node_tree.links.new(group_input.outputs[3], mix_005.inputs[0])
		#scene_time.Seconds -> noise_texture.W
		node_tree.links.new(scene_time.outputs[0], noise_texture.inputs[1])
		return node_tree
