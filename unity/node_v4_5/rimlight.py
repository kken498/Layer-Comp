import bpy
from ..node import *

class CompositorNodeRimLight(bpy.types.CompositorNodeCustomGroup, Node, Mix_Node):
	bl_name='CompositorNodeRimLight'
	bl_label='Rim Light'
	bl_icon='LIGHT_AREA'

	def init(self, context):
		self.getNodetree(context)
		self.inputs[1].default_value = (1.0, 0.9633176326751709, 0.8549970388412476, 1.0)
		self.inputs[2].default_value = 0.6108649969100952
		self.inputs[3].default_value = 5
		self.inputs[4].default_value = (15.0, 15.0)
		self.inputs[5].default_value = 1
		self.blend_type = 'LIGHTEN'

	def draw_buttons(self, context, layout):
		layout.prop(self, 'blend_type', text='')

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

		#Socket Rim Light
		rim_light_socket = node_tree.interface.new_socket(name = "Rim Light", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		rim_light_socket.default_value = (0.0, 0.0, 0.0, 1.0)
		rim_light_socket.attribute_domain = 'POINT'
		rim_light_socket.default_input = 'VALUE'
		rim_light_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Socket Rim Light
		rim_light_socket_1 = node_tree.interface.new_socket(name = "Rim Light", in_out='INPUT', socket_type = 'NodeSocketColor')
		rim_light_socket_1.default_value = (1.0, 0.9633176326751709, 0.8549970388412476, 1.0)
		rim_light_socket_1.attribute_domain = 'POINT'
		rim_light_socket_1.default_input = 'VALUE'
		rim_light_socket_1.structure_type = 'AUTO'

		#Socket Angle
		angle_socket = node_tree.interface.new_socket(name = "Angle", in_out='INPUT', socket_type = 'NodeSocketFloat')
		angle_socket.default_value = 0.6108649969100952
		angle_socket.min_value = -3.4028234663852886e+38
		angle_socket.max_value = 3.4028234663852886e+38
		angle_socket.subtype = 'ANGLE'
		angle_socket.attribute_domain = 'POINT'
		angle_socket.default_input = 'VALUE'
		angle_socket.structure_type = 'AUTO'

		#Socket Distance
		distance_socket = node_tree.interface.new_socket(name = "Distance", in_out='INPUT', socket_type = 'NodeSocketFloat')
		distance_socket.default_value = 5.0
		distance_socket.min_value = 0.0
		distance_socket.max_value = 10000.0
		distance_socket.subtype = 'NONE'
		distance_socket.attribute_domain = 'POINT'
		distance_socket.default_input = 'VALUE'
		distance_socket.structure_type = 'AUTO'

		#Socket Blur Size
		blur_size_socket = node_tree.interface.new_socket(name = "Blur Size", in_out='INPUT', socket_type = 'NodeSocketVector')
		blur_size_socket.default_value = (15.0, 15.0, 0.0)
		blur_size_socket.min_value = 0.0
		blur_size_socket.max_value = 3.4028234663852886e+38
		blur_size_socket.subtype = 'NONE'
		blur_size_socket.attribute_domain = 'POINT'
		blur_size_socket.default_input = 'VALUE'
		blur_size_socket.structure_type = 'AUTO'
		blur_size_socket.dimensions = 2

		#Socket Opacity
		opacity_socket = node_tree.interface.new_socket(name = "Opacity", in_out='INPUT', socket_type = 'NodeSocketFloat')
		opacity_socket.default_value = 1.0
		opacity_socket.min_value = 0.0
		opacity_socket.max_value = 1.0
		opacity_socket.subtype = 'FACTOR'
		opacity_socket.attribute_domain = 'POINT'
		opacity_socket.default_input = 'VALUE'
		opacity_socket.structure_type = 'AUTO'

		#Socket Fill
		fill_socket = node_tree.interface.new_socket(name = "Fill", in_out='INPUT', socket_type = 'NodeSocketFloat')
		fill_socket.default_value = 0.0
		fill_socket.min_value = 0.0
		fill_socket.max_value = 1.0
		fill_socket.subtype = 'FACTOR'
		fill_socket.attribute_domain = 'POINT'
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

		#node Translate
		translate = node_tree.nodes.new("CompositorNodeTranslate")
		translate.name = "Translate"
		translate.interpolation = 'NEAREST'
		translate.wrap_axis = 'NONE'

		#node Blur
		blur = node_tree.nodes.new("CompositorNodeBlur")
		blur.name = "Blur"
		blur.filter_type = 'FAST_GAUSS'
		#Extend Bounds
		blur.inputs[2].default_value = True
		#Separable
		blur.inputs[3].default_value = True

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#node Mix.001
		mix_001 = node_tree.nodes.new("ShaderNodeMix")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.clamp_factor = True
		mix_001.clamp_result = False
		mix_001.data_type = 'FLOAT'
		mix_001.factor_mode = 'UNIFORM'
		#A_Float
		mix_001.inputs[2].default_value = 0.0

		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'COSINE'
		math.use_clamp = False

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'SINE'
		math_001.use_clamp = False

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"
		reroute.socket_idname = "NodeSocketFloat"
		#node Math.002
		math_002 = node_tree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MULTIPLY'
		math_002.use_clamp = False

		#node Math.004
		math_004 = node_tree.nodes.new("ShaderNodeMath")
		math_004.name = "Math.004"
		math_004.operation = 'MULTIPLY'
		math_004.use_clamp = False

		#node Math.003
		math_003 = node_tree.nodes.new("ShaderNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'MULTIPLY'
		math_003.use_clamp = False
		#Value_001
		math_003.inputs[1].default_value = -1.0

		#node Reroute.001
		reroute_001 = node_tree.nodes.new("NodeReroute")
		reroute_001.name = "Reroute.001"
		reroute_001.socket_idname = "NodeSocketFloat"
		#node Math.005
		math_005 = node_tree.nodes.new("ShaderNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'MULTIPLY'
		math_005.use_clamp = False
		#Value_001
		math_005.inputs[1].default_value = 5.0

		#node Mix
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix"
		mix.blend_type = 'LIGHTEN'
		mix.clamp_factor = True
		mix.clamp_result = False
		mix.data_type = 'RGBA'
		mix.factor_mode = 'UNIFORM'

		#node Reroute.002
		reroute_002 = node_tree.nodes.new("NodeReroute")
		reroute_002.name = "Reroute.002"
		reroute_002.socket_idname = "NodeSocketColor"
		#node Set Alpha
		set_alpha = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha.name = "Set Alpha"
		set_alpha.mode = 'APPLY'

		#node Mix.002
		mix_002 = node_tree.nodes.new("ShaderNodeMix")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MIX'
		mix_002.clamp_factor = True
		mix_002.clamp_result = False
		mix_002.data_type = 'RGBA'
		mix_002.factor_mode = 'UNIFORM'

		#node Set Alpha.001
		set_alpha_001 = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha_001.name = "Set Alpha.001"
		set_alpha_001.mode = 'APPLY'

		#node Invert Color
		invert_color = node_tree.nodes.new("CompositorNodeInvert")
		invert_color.name = "Invert Color"
		#Fac
		invert_color.inputs[0].default_value = 1.0
		#Invert Color
		invert_color.inputs[2].default_value = True
		#Invert Alpha
		invert_color.inputs[3].default_value = False

		#initialize node_tree links
		#blur.Image -> translate.Image
		node_tree.links.new(blur.outputs[0], translate.inputs[0])
		#mix.Result -> group_output.Image
		node_tree.links.new(mix.outputs[2], group_output.inputs[0])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#group_input.Blur Size -> blur.Size
		node_tree.links.new(group_input.outputs[4], blur.inputs[1])
		#invert_color.Color -> mix_001.B
		node_tree.links.new(invert_color.outputs[0], mix_001.inputs[3])
		#group_input.Opacity -> mix_001.Factor
		node_tree.links.new(group_input.outputs[5], mix_001.inputs[0])
		#math_002.Value -> translate.X
		node_tree.links.new(math_002.outputs[0], translate.inputs[1])
		#math_004.Value -> translate.Y
		node_tree.links.new(math_004.outputs[0], translate.inputs[2])
		#reroute.Output -> math.Value
		node_tree.links.new(reroute.outputs[0], math.inputs[0])
		#reroute.Output -> math_001.Value
		node_tree.links.new(reroute.outputs[0], math_001.inputs[0])
		#math_003.Value -> reroute.Input
		node_tree.links.new(math_003.outputs[0], reroute.inputs[0])
		#math.Value -> math_002.Value
		node_tree.links.new(math.outputs[0], math_002.inputs[0])
		#reroute_001.Output -> math_002.Value
		node_tree.links.new(reroute_001.outputs[0], math_002.inputs[1])
		#math_001.Value -> math_004.Value
		node_tree.links.new(math_001.outputs[0], math_004.inputs[0])
		#reroute_001.Output -> math_004.Value
		node_tree.links.new(reroute_001.outputs[0], math_004.inputs[1])
		#group_input.Angle -> math_003.Value
		node_tree.links.new(group_input.outputs[2], math_003.inputs[0])
		#math_005.Value -> reroute_001.Input
		node_tree.links.new(math_005.outputs[0], reroute_001.inputs[0])
		#group_input.Distance -> math_005.Value
		node_tree.links.new(group_input.outputs[3], math_005.inputs[0])
		#mix_001.Result -> blur.Image
		node_tree.links.new(mix_001.outputs[0], blur.inputs[0])
		#translate.Image -> set_alpha.Image
		node_tree.links.new(translate.outputs[0], set_alpha.inputs[0])
		#separate_color.Alpha -> set_alpha.Alpha
		node_tree.links.new(separate_color.outputs[3], set_alpha.inputs[1])
		#reroute_002.Output -> mix.Factor
		node_tree.links.new(reroute_002.outputs[0], mix.inputs[0])
		#group_input.Image -> mix_002.A
		node_tree.links.new(group_input.outputs[0], mix_002.inputs[6])
		#group_input.Fill -> mix_002.Factor
		node_tree.links.new(group_input.outputs[6], mix_002.inputs[0])
		#group_input.Color -> mix_002.B
		node_tree.links.new(group_input.outputs[7], mix_002.inputs[7])
		#set_alpha.Image -> reroute_002.Input
		node_tree.links.new(set_alpha.outputs[0], reroute_002.inputs[0])
		#set_alpha_001.Image -> group_output.Rim Light
		node_tree.links.new(set_alpha_001.outputs[0], group_output.inputs[1])
		#reroute_002.Output -> set_alpha_001.Image
		node_tree.links.new(reroute_002.outputs[0], set_alpha_001.inputs[0])
		#set_alpha.Image -> set_alpha_001.Alpha
		node_tree.links.new(set_alpha.outputs[0], set_alpha_001.inputs[1])
		#group_input.Rim Light -> mix.B
		node_tree.links.new(group_input.outputs[1], mix.inputs[7])
		#mix_002.Result -> mix.A
		node_tree.links.new(mix_002.outputs[2], mix.inputs[6])
		#separate_color.Alpha -> invert_color.Color
		node_tree.links.new(separate_color.outputs[3], invert_color.inputs[1])
		return node_tree