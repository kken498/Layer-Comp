import bpy
from ..node import *

class CompositorNodeBoundaryLine(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeBoundaryLine'
	bl_label='BoundaryLine'
	bl_icon='MOD_LINEART'
	
	filter_items=(('LAPLACE', 'Laplace', 'Laplace'),
		('SOBEL', 'Sobel', 'Sobel'),
		('PREWITT', 'Prewitt', 'Prewitt'),
		('KIRSCH', 'Kirsch', 'Kirsch'))

	def update_filter_type(self, context):
		self.node_tree.nodes["Filter"].filter_type = self.filter_type

	filter_type : bpy.props.EnumProperty(default = 'LAPLACE', items = filter_items, name = "Falloff", update = update_filter_type)

	def init(self, context):
		self.getNodetree(context)
		self.filter_type = 'LAPLACE'
		self.inputs["Line Color"].default_value = (1, 0, 0, 1)
		self.inputs["Strength"].default_value = 1
		self.inputs["Threshold"].default_value = 0.5

	def draw_buttons(self, context, layout):
		layout.prop(self, 'filter_type', text='')

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"
		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'

		#Socket Line
		line_socket = node_tree.interface.new_socket(name = "Line", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		line_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 0.0)
		line_socket.attribute_domain = 'POINT'
		line_socket.default_input = 'VALUE'
		line_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Socket Line Color
		line_color_socket = node_tree.interface.new_socket(name = "Line Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		line_color_socket.default_value = (1.0, 0.0, 0.0, 1.0)
		line_color_socket.attribute_domain = 'POINT'
		line_color_socket.description = "Value of the first color input"
		line_color_socket.default_input = 'VALUE'
		line_color_socket.structure_type = 'AUTO'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 10000.0
		strength_socket.subtype = 'NONE'
		strength_socket.attribute_domain = 'POINT'
		strength_socket.default_input = 'VALUE'
		strength_socket.structure_type = 'AUTO'

		#Socket Threshold
		threshold_socket = node_tree.interface.new_socket(name = "Threshold", in_out='INPUT', socket_type = 'NodeSocketFloat')
		threshold_socket.default_value = 0.5
		threshold_socket.min_value = -10000.0
		threshold_socket.max_value = 10000.0
		threshold_socket.subtype = 'NONE'
		threshold_socket.attribute_domain = 'POINT'
		threshold_socket.default_input = 'VALUE'
		threshold_socket.structure_type = 'AUTO'

		#Socket Fill
		fill_socket = node_tree.interface.new_socket(name = "Fill", in_out='INPUT', socket_type = 'NodeSocketFloat')
		fill_socket.default_value = 0.0
		fill_socket.min_value = 0.0
		fill_socket.max_value = 1.0
		fill_socket.subtype = 'FACTOR'
		fill_socket.attribute_domain = 'POINT'
		fill_socket.description = "Amount of mixing between the A and B inputs"
		fill_socket.default_input = 'VALUE'
		fill_socket.structure_type = 'AUTO'

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (0.0, 0.0, 0.0, 1.0)
		color_socket.attribute_domain = 'POINT'
		color_socket.description = "Value of the second color input"
		color_socket.default_input = 'VALUE'
		color_socket.structure_type = 'AUTO'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Mix.004
		mix_004 = node_tree.nodes.new("ShaderNodeMix")
		mix_004.name = "Mix.004"
		mix_004.blend_type = 'MIX'
		mix_004.clamp_factor = True
		mix_004.clamp_result = False
		mix_004.data_type = 'RGBA'
		mix_004.factor_mode = 'UNIFORM'

		#node Filter
		filter = node_tree.nodes.new("CompositorNodeFilter")
		filter.name = "Filter"
		filter.filter_type = 'LAPLACE'
		#Fac
		filter.inputs[0].default_value = 1.0

		#node Mix.005
		mix_005 = node_tree.nodes.new("ShaderNodeMix")
		mix_005.name = "Mix.005"
		mix_005.blend_type = 'MIX'
		mix_005.clamp_factor = True
		mix_005.clamp_result = False
		mix_005.data_type = 'RGBA'
		mix_005.factor_mode = 'UNIFORM'
		#A_Color
		mix_005.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"
		reroute.socket_idname = "NodeSocketFloat"
		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = False

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'GREATER_THAN'
		math_001.use_clamp = False

		#node Math.002
		math_002 = node_tree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MULTIPLY'
		math_002.use_clamp = False
		#Value_001
		math_002.inputs[1].default_value = 0.10000000149011612

		#node Mix
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.clamp_factor = True
		mix.clamp_result = False
		mix.data_type = 'RGBA'
		mix.factor_mode = 'UNIFORM'

		#initialize node_tree links
		#reroute.Output -> mix_004.Factor
		node_tree.links.new(reroute.outputs[0], mix_004.inputs[0])
		#group_input.Image -> filter.Image
		node_tree.links.new(group_input.outputs[0], filter.inputs[1])
		#reroute.Output -> mix_005.Factor
		node_tree.links.new(reroute.outputs[0], mix_005.inputs[0])
		#mix_005.Result -> group_output.Line
		node_tree.links.new(mix_005.outputs[2], group_output.inputs[1])
		#mix_004.Result -> group_output.Image
		node_tree.links.new(mix_004.outputs[2], group_output.inputs[0])
		#group_input.Line Color -> mix_004.B
		node_tree.links.new(group_input.outputs[1], mix_004.inputs[7])
		#mix.Result -> mix_004.A
		node_tree.links.new(mix.outputs[2], mix_004.inputs[6])
		#group_input.Line Color -> mix_005.B
		node_tree.links.new(group_input.outputs[1], mix_005.inputs[7])
		#math_001.Value -> reroute.Input
		node_tree.links.new(math_001.outputs[0], reroute.inputs[0])
		#filter.Image -> math.Value
		node_tree.links.new(filter.outputs[0], math.inputs[0])
		#group_input.Strength -> math.Value
		node_tree.links.new(group_input.outputs[2], math.inputs[1])
		#math.Value -> math_001.Value
		node_tree.links.new(math.outputs[0], math_001.inputs[0])
		#math_002.Value -> math_001.Value
		node_tree.links.new(math_002.outputs[0], math_001.inputs[1])
		#group_input.Threshold -> math_002.Value
		node_tree.links.new(group_input.outputs[3], math_002.inputs[0])
		#group_input.Image -> mix.A
		node_tree.links.new(group_input.outputs[0], mix.inputs[6])
		#group_input.Fill -> mix.Factor
		node_tree.links.new(group_input.outputs[4], mix.inputs[0])
		#group_input.Color -> mix.B
		node_tree.links.new(group_input.outputs[5], mix.inputs[7])
		return node_tree