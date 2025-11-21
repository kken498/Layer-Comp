import bpy
from ..node import *

class CompositorNodeHalation(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeHalation'
	bl_label='Halation'
	bl_icon='SHADERFX'

	def init(self, context):
		self.getNodetree(context)
		self.inputs[1].default_value = (1,0,0,1)
		self.inputs[2].default_value = 0.3
		self.inputs[3].default_value = 1
		self.inputs[4].default_value = 40
		self.inputs[5].default_value = 0.2
		self.inputs[6].default_value = 1.0

	def draw_buttons(self, context, layout):
		return

	def getNodetree(self, context):
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"

		#node_tree interface
		#Socket Result
		result_socket = node_tree.interface.new_socket(name = "Result", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		result_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		result_socket.attribute_domain = 'POINT'
		result_socket.default_input = 'VALUE'
		result_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.hide_value = True
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (1.0, 0.0, 0.0, 1.0)
		color_socket.attribute_domain = 'POINT'
		color_socket.description = "Color of the node_tree effect. Red is the color that is usually associated with it"
		color_socket.default_input = 'VALUE'
		color_socket.structure_type = 'AUTO'

		#Socket Threshold
		threshold_socket = node_tree.interface.new_socket(name = "Threshold", in_out='INPUT', socket_type = 'NodeSocketFloat')
		threshold_socket.default_value = 0.29999998211860657
		threshold_socket.min_value = 0.0
		threshold_socket.max_value = 1.0
		threshold_socket.subtype = 'NONE'
		threshold_socket.attribute_domain = 'POINT'
		threshold_socket.description = "Limuits which parts of the image should be affected by node_tree. A value of 0 will result in the entire image being affected by node_tree. A higher value will limit the node_tree effect to the highlights of the image"
		threshold_socket.default_input = 'VALUE'
		threshold_socket.structure_type = 'AUTO'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 10000.0
		strength_socket.subtype = 'NONE'
		strength_socket.attribute_domain = 'POINT'
		strength_socket.description = "Controls the intensity of the node_tree effect"
		strength_socket.default_input = 'VALUE'
		strength_socket.structure_type = 'AUTO'

		#Socket Blur Size
		blur_size_socket = node_tree.interface.new_socket(name = "Blur Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blur_size_socket.default_value = 40.0
		blur_size_socket.min_value = 0.0
		blur_size_socket.max_value = 100.0
		blur_size_socket.subtype = 'NONE'
		blur_size_socket.attribute_domain = 'POINT'
		blur_size_socket.default_input = 'VALUE'
		blur_size_socket.structure_type = 'AUTO'

		#Socket Blur Aspect
		blur_aspect_socket = node_tree.interface.new_socket(name = "Blur Aspect", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blur_aspect_socket.default_value = 0.19999998807907104
		blur_aspect_socket.min_value = -1.0
		blur_aspect_socket.max_value = 1.0
		blur_aspect_socket.subtype = 'NONE'
		blur_aspect_socket.attribute_domain = 'POINT'
		blur_aspect_socket.description = "Aspect ratio of the Blur. Values below 0 will result in a more horizontal blur and values above 0 will result in a more vertical blur"
		blur_aspect_socket.default_input = 'VALUE'
		blur_aspect_socket.structure_type = 'AUTO'

		#Socket Opacity
		opacity_socket = node_tree.interface.new_socket(name = "Opacity", in_out='INPUT', socket_type = 'NodeSocketFloat')
		opacity_socket.default_value = 1.0
		opacity_socket.min_value = 0.0
		opacity_socket.max_value = 1.0
		opacity_socket.subtype = 'FACTOR'
		opacity_socket.attribute_domain = 'POINT'
		opacity_socket.description = "Overall Opacity of the effect"
		opacity_socket.default_input = 'VALUE'
		opacity_socket.structure_type = 'AUTO'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node RGB to BW
		rgb_to_bw = node_tree.nodes.new("CompositorNodeRGBToBW")
		rgb_to_bw.name = "RGB to BW"

		#node Map Range
		map_range = node_tree.nodes.new("ShaderNodeMapRange")
		map_range.name = "Map Range"
		map_range.clamp = True
		map_range.data_type = 'FLOAT'
		map_range.interpolation_type = 'LINEAR'
		#From Max
		map_range.inputs[2].default_value = 1.0
		#To Min
		map_range.inputs[3].default_value = 0.0
		#To Max
		map_range.inputs[4].default_value = 1.0

		#node Blur
		blur = node_tree.nodes.new("CompositorNodeBlur")
		blur.name = "Blur"
		blur.filter_type = 'FAST_GAUSS'
		#Extend Bounds
		blur.inputs[2].default_value = True
		#Separable
		blur.inputs[3].default_value = True

		#node Mix.001
		mix_001 = node_tree.nodes.new("ShaderNodeMix")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'SCREEN'
		mix_001.clamp_factor = True
		mix_001.clamp_result = False
		mix_001.data_type = 'RGBA'
		mix_001.factor_mode = 'UNIFORM'

		#node Vector Math
		vector_math = node_tree.nodes.new("ShaderNodeVectorMath")
		vector_math.name = "Vector Math"
		vector_math.operation = 'MULTIPLY'

		#node Combine XYZ
		combine_xyz = node_tree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz.name = "Combine XYZ"
		#Z
		combine_xyz.inputs[2].default_value = 0.0

		#node Map Range.001
		map_range_001 = node_tree.nodes.new("ShaderNodeMapRange")
		map_range_001.name = "Map Range.001"
		map_range_001.hide = True
		map_range_001.clamp = True
		map_range_001.data_type = 'FLOAT'
		map_range_001.interpolation_type = 'LINEAR'
		#From Min
		map_range_001.inputs[1].default_value = 0.0
		#From Max
		map_range_001.inputs[2].default_value = 1.0
		#To Min
		map_range_001.inputs[3].default_value = 1.0
		#To Max
		map_range_001.inputs[4].default_value = 0.0

		#node Map Range.002
		map_range_002 = node_tree.nodes.new("ShaderNodeMapRange")
		map_range_002.name = "Map Range.002"
		map_range_002.hide = True
		map_range_002.clamp = True
		map_range_002.data_type = 'FLOAT'
		map_range_002.interpolation_type = 'LINEAR'
		#From Min
		map_range_002.inputs[1].default_value = 0.0
		#From Max
		map_range_002.inputs[2].default_value = -1.0
		#To Min
		map_range_002.inputs[3].default_value = 1.0
		#To Max
		map_range_002.inputs[4].default_value = 0.0

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"
		reroute.socket_idname = "NodeSocketFloat"
		#node Mix.002
		mix_002 = node_tree.nodes.new("ShaderNodeMix")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MIX'
		mix_002.clamp_factor = True
		mix_002.clamp_result = False
		mix_002.data_type = 'RGBA'
		mix_002.factor_mode = 'UNIFORM'

		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = False

		#initialize node_tree links
		#rgb_to_bw.Val -> map_range.Value
		node_tree.links.new(rgb_to_bw.outputs[0], map_range.inputs[0])
		#map_range.Result -> blur.Image
		node_tree.links.new(map_range.outputs[0], blur.inputs[0])
		#group_input.Image -> rgb_to_bw.Image
		node_tree.links.new(group_input.outputs[0], rgb_to_bw.inputs[0])
		#group_input.Image -> mix_001.A
		node_tree.links.new(group_input.outputs[0], mix_001.inputs[6])
		#mix_002.Result -> group_output.Result
		node_tree.links.new(mix_002.outputs[2], group_output.inputs[0])
		#vector_math.Vector -> blur.Size
		node_tree.links.new(vector_math.outputs[0], blur.inputs[1])
		#group_input.Threshold -> map_range.From Min
		node_tree.links.new(group_input.outputs[2], map_range.inputs[1])
		#group_input.Blur Size -> vector_math.Vector
		node_tree.links.new(group_input.outputs[4], vector_math.inputs[0])
		#reroute.Output -> map_range_001.Value
		node_tree.links.new(reroute.outputs[0], map_range_001.inputs[0])
		#map_range_001.Result -> combine_xyz.X
		node_tree.links.new(map_range_001.outputs[0], combine_xyz.inputs[0])
		#map_range_002.Result -> combine_xyz.Y
		node_tree.links.new(map_range_002.outputs[0], combine_xyz.inputs[1])
		#group_input.Blur Aspect -> reroute.Input
		node_tree.links.new(group_input.outputs[5], reroute.inputs[0])
		#reroute.Output -> map_range_002.Value
		node_tree.links.new(reroute.outputs[0], map_range_002.inputs[0])
		#combine_xyz.Vector -> vector_math.Vector
		node_tree.links.new(combine_xyz.outputs[0], vector_math.inputs[1])
		#group_input.Image -> mix_002.A
		node_tree.links.new(group_input.outputs[0], mix_002.inputs[6])
		#mix_001.Result -> mix_002.B
		node_tree.links.new(mix_001.outputs[2], mix_002.inputs[7])
		#group_input.Opacity -> mix_002.Factor
		node_tree.links.new(group_input.outputs[6], mix_002.inputs[0])
		#math.Value -> mix_001.Factor
		node_tree.links.new(math.outputs[0], mix_001.inputs[0])
		#blur.Image -> math.Value
		node_tree.links.new(blur.outputs[0], math.inputs[0])
		#group_input.Strength -> math.Value
		node_tree.links.new(group_input.outputs[3], math.inputs[1])
		#group_input.Color -> mix_001.B
		node_tree.links.new(group_input.outputs[1], mix_001.inputs[7])
		return node_tree
