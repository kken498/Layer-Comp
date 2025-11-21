import bpy
from ..node import *

class CompositorNodeChromaticAberration(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeChromaticAberration'
	bl_label='Chromatic Aberration'
	bl_icon='SEQ_CHROMA_SCOPE'

	def init(self, context):
		self.getNodetree(context)

	def draw_buttons(self, context, layout):
		return

	def getNodetree(self, context):
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

		#Socket Red/Cyan
		red_cyan_socket = node_tree.interface.new_socket(name = "Red/Cyan", in_out='INPUT', socket_type = 'NodeSocketFloat')
		red_cyan_socket.default_value = 0.0
		red_cyan_socket.min_value = -10.0
		red_cyan_socket.max_value = 10.0
		red_cyan_socket.subtype = 'NONE'
		red_cyan_socket.attribute_domain = 'POINT'
		red_cyan_socket.default_input = 'VALUE'
		red_cyan_socket.structure_type = 'AUTO'

		#Socket Green/magenta
		green_magenta_socket = node_tree.interface.new_socket(name = "Green/magenta", in_out='INPUT', socket_type = 'NodeSocketFloat')
		green_magenta_socket.default_value = 0.0
		green_magenta_socket.min_value = -10.0
		green_magenta_socket.max_value = 10.0
		green_magenta_socket.subtype = 'NONE'
		green_magenta_socket.attribute_domain = 'POINT'
		green_magenta_socket.default_input = 'VALUE'
		green_magenta_socket.structure_type = 'AUTO'

		#Socket Blue/yellow
		blue_yellow_socket = node_tree.interface.new_socket(name = "Blue/yellow", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blue_yellow_socket.default_value = 0.0
		blue_yellow_socket.min_value = -10.0
		blue_yellow_socket.max_value = 10.0
		blue_yellow_socket.subtype = 'NONE'
		blue_yellow_socket.attribute_domain = 'POINT'
		blue_yellow_socket.default_input = 'VALUE'
		blue_yellow_socket.structure_type = 'AUTO'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node RGB Curves
		rgb_curves = node_tree.nodes.new("CompositorNodeCurveRGB")
		rgb_curves.name = "RGB Curves"
		#mapping settings
		rgb_curves.mapping.extend = 'EXTRAPOLATED'
		rgb_curves.mapping.tone = 'STANDARD'
		rgb_curves.mapping.black_level = (0.0, 0.0, 0.0)
		rgb_curves.mapping.white_level = (1.0, 1.0, 1.0)
		rgb_curves.mapping.clip_min_x = 0.0
		rgb_curves.mapping.clip_min_y = 0.0
		rgb_curves.mapping.clip_max_x = 1.0
		rgb_curves.mapping.clip_max_y = 1.0
		rgb_curves.mapping.use_clip = True
		#curve 0
		rgb_curves_curve_0 = rgb_curves.mapping.curves[0]
		rgb_curves_curve_0_point_0 = rgb_curves_curve_0.points[0]
		rgb_curves_curve_0_point_0.location = (0.0, 0.0)
		rgb_curves_curve_0_point_0.handle_type = 'AUTO'
		rgb_curves_curve_0_point_1 = rgb_curves_curve_0.points[1]
		rgb_curves_curve_0_point_1.location = (1.0, 1.0)
		rgb_curves_curve_0_point_1.handle_type = 'AUTO'
		#curve 1
		rgb_curves_curve_1 = rgb_curves.mapping.curves[1]
		rgb_curves_curve_1_point_0 = rgb_curves_curve_1.points[0]
		rgb_curves_curve_1_point_0.location = (0.0, 0.0)
		rgb_curves_curve_1_point_0.handle_type = 'AUTO'
		rgb_curves_curve_1_point_1 = rgb_curves_curve_1.points[1]
		rgb_curves_curve_1_point_1.location = (1.0, 0.0)
		rgb_curves_curve_1_point_1.handle_type = 'AUTO'
		#curve 2
		rgb_curves_curve_2 = rgb_curves.mapping.curves[2]
		rgb_curves_curve_2_point_0 = rgb_curves_curve_2.points[0]
		rgb_curves_curve_2_point_0.location = (0.0, 0.0)
		rgb_curves_curve_2_point_0.handle_type = 'AUTO'
		rgb_curves_curve_2_point_1 = rgb_curves_curve_2.points[1]
		rgb_curves_curve_2_point_1.location = (1.0, 0.0)
		rgb_curves_curve_2_point_1.handle_type = 'AUTO'
		#curve 3
		rgb_curves_curve_3 = rgb_curves.mapping.curves[3]
		rgb_curves_curve_3_point_0 = rgb_curves_curve_3.points[0]
		rgb_curves_curve_3_point_0.location = (0.0, 0.0)
		rgb_curves_curve_3_point_0.handle_type = 'AUTO'
		rgb_curves_curve_3_point_1 = rgb_curves_curve_3.points[1]
		rgb_curves_curve_3_point_1.location = (1.0, 1.0)
		rgb_curves_curve_3_point_1.handle_type = 'AUTO'
		#update curve after changes
		rgb_curves.mapping.update()
		rgb_curves.inputs[0].hide = True
		rgb_curves.inputs[2].hide = True
		rgb_curves.inputs[3].hide = True
		#Fac
		rgb_curves.inputs[0].default_value = 1.0
		#Black Level
		rgb_curves.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
		#White Level
		rgb_curves.inputs[3].default_value = (1.0, 1.0, 1.0, 1.0)

		#node RGB Curves.001
		rgb_curves_001 = node_tree.nodes.new("CompositorNodeCurveRGB")
		rgb_curves_001.name = "RGB Curves.001"
		#mapping settings
		rgb_curves_001.mapping.extend = 'EXTRAPOLATED'
		rgb_curves_001.mapping.tone = 'STANDARD'
		rgb_curves_001.mapping.black_level = (0.0, 0.0, 0.0)
		rgb_curves_001.mapping.white_level = (1.0, 1.0, 1.0)
		rgb_curves_001.mapping.clip_min_x = 0.0
		rgb_curves_001.mapping.clip_min_y = 0.0
		rgb_curves_001.mapping.clip_max_x = 1.0
		rgb_curves_001.mapping.clip_max_y = 1.0
		rgb_curves_001.mapping.use_clip = True
		#curve 0
		rgb_curves_001_curve_0 = rgb_curves_001.mapping.curves[0]
		rgb_curves_001_curve_0_point_0 = rgb_curves_001_curve_0.points[0]
		rgb_curves_001_curve_0_point_0.location = (0.0, 0.0)
		rgb_curves_001_curve_0_point_0.handle_type = 'AUTO'
		rgb_curves_001_curve_0_point_1 = rgb_curves_001_curve_0.points[1]
		rgb_curves_001_curve_0_point_1.location = (1.0, 0.0)
		rgb_curves_001_curve_0_point_1.handle_type = 'AUTO'
		#curve 1
		rgb_curves_001_curve_1 = rgb_curves_001.mapping.curves[1]
		rgb_curves_001_curve_1_point_0 = rgb_curves_001_curve_1.points[0]
		rgb_curves_001_curve_1_point_0.location = (0.0, 0.0)
		rgb_curves_001_curve_1_point_0.handle_type = 'AUTO'
		rgb_curves_001_curve_1_point_1 = rgb_curves_001_curve_1.points[1]
		rgb_curves_001_curve_1_point_1.location = (1.0, 1.0)
		rgb_curves_001_curve_1_point_1.handle_type = 'AUTO'
		#curve 2
		rgb_curves_001_curve_2 = rgb_curves_001.mapping.curves[2]
		rgb_curves_001_curve_2_point_0 = rgb_curves_001_curve_2.points[0]
		rgb_curves_001_curve_2_point_0.location = (0.0, 0.0)
		rgb_curves_001_curve_2_point_0.handle_type = 'AUTO'
		rgb_curves_001_curve_2_point_1 = rgb_curves_001_curve_2.points[1]
		rgb_curves_001_curve_2_point_1.location = (1.0, 0.0)
		rgb_curves_001_curve_2_point_1.handle_type = 'AUTO'
		#curve 3
		rgb_curves_001_curve_3 = rgb_curves_001.mapping.curves[3]
		rgb_curves_001_curve_3_point_0 = rgb_curves_001_curve_3.points[0]
		rgb_curves_001_curve_3_point_0.location = (0.0, 0.0)
		rgb_curves_001_curve_3_point_0.handle_type = 'AUTO'
		rgb_curves_001_curve_3_point_1 = rgb_curves_001_curve_3.points[1]
		rgb_curves_001_curve_3_point_1.location = (1.0, 1.0)
		rgb_curves_001_curve_3_point_1.handle_type = 'AUTO'
		#update curve after changes
		rgb_curves_001.mapping.update()
		rgb_curves_001.inputs[0].hide = True
		rgb_curves_001.inputs[2].hide = True
		rgb_curves_001.inputs[3].hide = True
		#Fac
		rgb_curves_001.inputs[0].default_value = 1.0
		#Black Level
		rgb_curves_001.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
		#White Level
		rgb_curves_001.inputs[3].default_value = (1.0, 1.0, 1.0, 1.0)

		#node RGB Curves.002
		rgb_curves_002 = node_tree.nodes.new("CompositorNodeCurveRGB")
		rgb_curves_002.name = "RGB Curves.002"
		#mapping settings
		rgb_curves_002.mapping.extend = 'EXTRAPOLATED'
		rgb_curves_002.mapping.tone = 'STANDARD'
		rgb_curves_002.mapping.black_level = (0.0, 0.0, 0.0)
		rgb_curves_002.mapping.white_level = (1.0, 1.0, 1.0)
		rgb_curves_002.mapping.clip_min_x = 0.0
		rgb_curves_002.mapping.clip_min_y = 0.0
		rgb_curves_002.mapping.clip_max_x = 1.0
		rgb_curves_002.mapping.clip_max_y = 1.0
		rgb_curves_002.mapping.use_clip = True
		#curve 0
		rgb_curves_002_curve_0 = rgb_curves_002.mapping.curves[0]
		rgb_curves_002_curve_0_point_0 = rgb_curves_002_curve_0.points[0]
		rgb_curves_002_curve_0_point_0.location = (0.0, 0.0)
		rgb_curves_002_curve_0_point_0.handle_type = 'AUTO'
		rgb_curves_002_curve_0_point_1 = rgb_curves_002_curve_0.points[1]
		rgb_curves_002_curve_0_point_1.location = (1.0, 0.0)
		rgb_curves_002_curve_0_point_1.handle_type = 'AUTO'
		#curve 1
		rgb_curves_002_curve_1 = rgb_curves_002.mapping.curves[1]
		rgb_curves_002_curve_1_point_0 = rgb_curves_002_curve_1.points[0]
		rgb_curves_002_curve_1_point_0.location = (0.0, 0.0)
		rgb_curves_002_curve_1_point_0.handle_type = 'AUTO'
		rgb_curves_002_curve_1_point_1 = rgb_curves_002_curve_1.points[1]
		rgb_curves_002_curve_1_point_1.location = (1.0, 0.0)
		rgb_curves_002_curve_1_point_1.handle_type = 'AUTO'
		#curve 2
		rgb_curves_002_curve_2 = rgb_curves_002.mapping.curves[2]
		rgb_curves_002_curve_2_point_0 = rgb_curves_002_curve_2.points[0]
		rgb_curves_002_curve_2_point_0.location = (0.0, 0.0)
		rgb_curves_002_curve_2_point_0.handle_type = 'AUTO'
		rgb_curves_002_curve_2_point_1 = rgb_curves_002_curve_2.points[1]
		rgb_curves_002_curve_2_point_1.location = (1.0, 1.0)
		rgb_curves_002_curve_2_point_1.handle_type = 'AUTO'
		#curve 3
		rgb_curves_002_curve_3 = rgb_curves_002.mapping.curves[3]
		rgb_curves_002_curve_3_point_0 = rgb_curves_002_curve_3.points[0]
		rgb_curves_002_curve_3_point_0.location = (0.0, 0.0)
		rgb_curves_002_curve_3_point_0.handle_type = 'AUTO'
		rgb_curves_002_curve_3_point_1 = rgb_curves_002_curve_3.points[1]
		rgb_curves_002_curve_3_point_1.location = (1.0, 1.0)
		rgb_curves_002_curve_3_point_1.handle_type = 'AUTO'
		#update curve after changes
		rgb_curves_002.mapping.update()
		rgb_curves_002.inputs[0].hide = True
		rgb_curves_002.inputs[2].hide = True
		rgb_curves_002.inputs[3].hide = True
		#Fac
		rgb_curves_002.inputs[0].default_value = 1.0
		#Black Level
		rgb_curves_002.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
		#White Level
		rgb_curves_002.inputs[3].default_value = (1.0, 1.0, 1.0, 1.0)

		#node Mix.001
		mix_001 = node_tree.nodes.new("ShaderNodeMix")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'SCREEN'
		mix_001.clamp_factor = False
		mix_001.clamp_result = False
		mix_001.data_type = 'RGBA'
		mix_001.factor_mode = 'UNIFORM'
		#Factor_Float
		mix_001.inputs[0].default_value = 1.0

		#node Mix.002
		mix_002 = node_tree.nodes.new("ShaderNodeMix")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'SCREEN'
		mix_002.clamp_factor = False
		mix_002.clamp_result = False
		mix_002.data_type = 'RGBA'
		mix_002.factor_mode = 'UNIFORM'
		#Factor_Float
		mix_002.inputs[0].default_value = 1.0

		#node Scale
		scale = node_tree.nodes.new("CompositorNodeScale")
		scale.name = "Scale"
		scale.frame_method = 'STRETCH'
		scale.interpolation = 'NEAREST'
		scale.space = 'RELATIVE'

		#node Scale.001
		scale_001 = node_tree.nodes.new("CompositorNodeScale")
		scale_001.name = "Scale.001"
		scale_001.frame_method = 'STRETCH'
		scale_001.interpolation = 'NEAREST'
		scale_001.space = 'RELATIVE'

		#node Scale.002
		scale_002 = node_tree.nodes.new("CompositorNodeScale")
		scale_002.name = "Scale.002"
		scale_002.frame_method = 'STRETCH'
		scale_002.interpolation = 'NEAREST'
		scale_002.space = 'RELATIVE'

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"
		reroute.socket_idname = "NodeSocketColor"
		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY_ADD'
		math.use_clamp = False
		#Value_001
		math.inputs[1].default_value = 0.009999999776482582
		#Value_002
		math.inputs[2].default_value = 1.0

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'MULTIPLY_ADD'
		math_001.use_clamp = False
		#Value_001
		math_001.inputs[1].default_value = 0.009999999776482582
		#Value_002
		math_001.inputs[2].default_value = 1.0

		#node Math.002
		math_002 = node_tree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MULTIPLY_ADD'
		math_002.use_clamp = False
		#Value_001
		math_002.inputs[1].default_value = 0.009999999776482582
		#Value_002
		math_002.inputs[2].default_value = 1.0

		#node Math.004
		math_004 = node_tree.nodes.new("ShaderNodeMath")
		math_004.name = "Math.004"
		math_004.operation = 'MULTIPLY'
		math_004.use_clamp = False

		#node Math.005
		math_005 = node_tree.nodes.new("ShaderNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'MULTIPLY'
		math_005.use_clamp = False

		#node Math.006
		math_006 = node_tree.nodes.new("ShaderNodeMath")
		math_006.name = "Math.006"
		math_006.operation = 'MULTIPLY'
		math_006.use_clamp = False

		#node Clamp.001
		clamp_001 = node_tree.nodes.new("ShaderNodeClamp")
		clamp_001.name = "Clamp.001"
		clamp_001.clamp_type = 'MINMAX'
		#Min
		clamp_001.inputs[1].default_value = 1.0
		#Max
		clamp_001.inputs[2].default_value = 1.100000023841858

		#node Math.003
		math_003 = node_tree.nodes.new("ShaderNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'MULTIPLY_ADD'
		math_003.use_clamp = False
		#Value_001
		math_003.inputs[1].default_value = -0.009999999776482582
		#Value_002
		math_003.inputs[2].default_value = 1.0

		#node Clamp.002
		clamp_002 = node_tree.nodes.new("ShaderNodeClamp")
		clamp_002.name = "Clamp.002"
		clamp_002.clamp_type = 'MINMAX'
		#Min
		clamp_002.inputs[1].default_value = 1.0
		#Max
		clamp_002.inputs[2].default_value = 1.100000023841858

		#node Set Alpha
		set_alpha = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha.name = "Set Alpha"
		set_alpha.mode = 'APPLY'

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#node Math.007
		math_007 = node_tree.nodes.new("ShaderNodeMath")
		math_007.name = "Math.007"
		math_007.operation = 'MULTIPLY_ADD'
		math_007.use_clamp = False
		#Value_001
		math_007.inputs[1].default_value = -0.009999999776482582
		#Value_002
		math_007.inputs[2].default_value = 1.0

		#node Clamp.003
		clamp_003 = node_tree.nodes.new("ShaderNodeClamp")
		clamp_003.name = "Clamp.003"
		clamp_003.clamp_type = 'MINMAX'
		#Min
		clamp_003.inputs[1].default_value = 1.0
		#Max
		clamp_003.inputs[2].default_value = 1.100000023841858

		#node Math.008
		math_008 = node_tree.nodes.new("ShaderNodeMath")
		math_008.name = "Math.008"
		math_008.operation = 'MULTIPLY_ADD'
		math_008.use_clamp = False
		#Value_001
		math_008.inputs[1].default_value = -0.009999999776482582
		#Value_002
		math_008.inputs[2].default_value = 1.0

		#node Clamp.004
		clamp_004 = node_tree.nodes.new("ShaderNodeClamp")
		clamp_004.name = "Clamp.004"
		clamp_004.clamp_type = 'MINMAX'
		#Min
		clamp_004.inputs[1].default_value = 1.0
		#Max
		clamp_004.inputs[2].default_value = 1.100000023841858

		#node Clamp.005
		clamp_005 = node_tree.nodes.new("ShaderNodeClamp")
		clamp_005.name = "Clamp.005"
		clamp_005.clamp_type = 'MINMAX'
		#Min
		clamp_005.inputs[1].default_value = 1.0
		#Max
		clamp_005.inputs[2].default_value = 1.100000023841858

		#node Math.009
		math_009 = node_tree.nodes.new("ShaderNodeMath")
		math_009.name = "Math.009"
		math_009.operation = 'MULTIPLY'
		math_009.use_clamp = False

		#node Clamp.006
		clamp_006 = node_tree.nodes.new("ShaderNodeClamp")
		clamp_006.name = "Clamp.006"
		clamp_006.clamp_type = 'MINMAX'
		#Min
		clamp_006.inputs[1].default_value = 1.0
		#Max
		clamp_006.inputs[2].default_value = 1.100000023841858

		#node Math.010
		math_010 = node_tree.nodes.new("ShaderNodeMath")
		math_010.name = "Math.010"
		math_010.operation = 'MULTIPLY'
		math_010.use_clamp = False

		#node Math.011
		math_011 = node_tree.nodes.new("ShaderNodeMath")
		math_011.name = "Math.011"
		math_011.operation = 'MULTIPLY'
		math_011.use_clamp = False

		#node Set Alpha.001
		set_alpha_001 = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha_001.name = "Set Alpha.001"
		set_alpha_001.mode = 'APPLY'

		#node Set Alpha.002
		set_alpha_002 = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha_002.name = "Set Alpha.002"
		set_alpha_002.mode = 'APPLY'

		#initialize node_tree links
		#mix_001.Result -> mix_002.A
		node_tree.links.new(mix_001.outputs[2], mix_002.inputs[6])
		#set_alpha_001.Image -> mix_001.B
		node_tree.links.new(set_alpha_001.outputs[0], mix_001.inputs[7])
		#set_alpha_002.Image -> mix_002.B
		node_tree.links.new(set_alpha_002.outputs[0], mix_002.inputs[7])
		#mix_002.Result -> group_output.Image
		node_tree.links.new(mix_002.outputs[2], group_output.inputs[0])
		#scale.Image -> rgb_curves.Image
		node_tree.links.new(scale.outputs[0], rgb_curves.inputs[1])
		#scale_001.Image -> rgb_curves_001.Image
		node_tree.links.new(scale_001.outputs[0], rgb_curves_001.inputs[1])
		#scale_002.Image -> rgb_curves_002.Image
		node_tree.links.new(scale_002.outputs[0], rgb_curves_002.inputs[1])
		#reroute.Output -> scale.Image
		node_tree.links.new(reroute.outputs[0], scale.inputs[0])
		#reroute.Output -> scale_001.Image
		node_tree.links.new(reroute.outputs[0], scale_001.inputs[0])
		#reroute.Output -> scale_002.Image
		node_tree.links.new(reroute.outputs[0], scale_002.inputs[0])
		#group_input.Image -> reroute.Input
		node_tree.links.new(group_input.outputs[0], reroute.inputs[0])
		#group_input.Red/Cyan -> math.Value
		node_tree.links.new(group_input.outputs[1], math.inputs[0])
		#group_input.Green/magenta -> math_001.Value
		node_tree.links.new(group_input.outputs[2], math_001.inputs[0])
		#group_input.Blue/yellow -> math_002.Value
		node_tree.links.new(group_input.outputs[3], math_002.inputs[0])
		#math.Value -> clamp_001.Value
		node_tree.links.new(math.outputs[0], clamp_001.inputs[0])
		#group_input.Red/Cyan -> math_003.Value
		node_tree.links.new(group_input.outputs[1], math_003.inputs[0])
		#clamp_002.Result -> math_006.Value
		node_tree.links.new(clamp_002.outputs[0], math_006.inputs[0])
		#math_003.Value -> clamp_002.Value
		node_tree.links.new(math_003.outputs[0], clamp_002.inputs[0])
		#set_alpha.Image -> mix_001.A
		node_tree.links.new(set_alpha.outputs[0], mix_001.inputs[6])
		#rgb_curves.Image -> set_alpha.Image
		node_tree.links.new(rgb_curves.outputs[0], set_alpha.inputs[0])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#separate_color.Alpha -> set_alpha.Alpha
		node_tree.links.new(separate_color.outputs[3], set_alpha.inputs[1])
		#group_input.Green/magenta -> math_007.Value
		node_tree.links.new(group_input.outputs[2], math_007.inputs[0])
		#math_007.Value -> clamp_003.Value
		node_tree.links.new(math_007.outputs[0], clamp_003.inputs[0])
		#math_008.Value -> clamp_004.Value
		node_tree.links.new(math_008.outputs[0], clamp_004.inputs[0])
		#clamp_001.Result -> math_004.Value
		node_tree.links.new(clamp_001.outputs[0], math_004.inputs[1])
		#clamp_003.Result -> math_004.Value
		node_tree.links.new(clamp_003.outputs[0], math_004.inputs[0])
		#clamp_001.Result -> math_005.Value
		node_tree.links.new(clamp_001.outputs[0], math_005.inputs[1])
		#clamp_004.Result -> math_005.Value
		node_tree.links.new(clamp_004.outputs[0], math_005.inputs[0])
		#math_001.Value -> clamp_005.Value
		node_tree.links.new(math_001.outputs[0], clamp_005.inputs[0])
		#clamp_005.Result -> math_006.Value
		node_tree.links.new(clamp_005.outputs[0], math_006.inputs[1])
		#math_005.Value -> math_009.Value
		node_tree.links.new(math_005.outputs[0], math_009.inputs[0])
		#clamp_005.Result -> math_009.Value
		node_tree.links.new(clamp_005.outputs[0], math_009.inputs[1])
		#math_002.Value -> clamp_006.Value
		node_tree.links.new(math_002.outputs[0], clamp_006.inputs[0])
		#math_004.Value -> math_010.Value
		node_tree.links.new(math_004.outputs[0], math_010.inputs[0])
		#math_006.Value -> math_011.Value
		node_tree.links.new(math_006.outputs[0], math_011.inputs[0])
		#math_011.Value -> scale.X
		node_tree.links.new(math_011.outputs[0], scale.inputs[1])
		#math_011.Value -> scale.Y
		node_tree.links.new(math_011.outputs[0], scale.inputs[2])
		#math_010.Value -> scale_001.X
		node_tree.links.new(math_010.outputs[0], scale_001.inputs[1])
		#math_010.Value -> scale_001.Y
		node_tree.links.new(math_010.outputs[0], scale_001.inputs[2])
		#math_009.Value -> scale_002.X
		node_tree.links.new(math_009.outputs[0], scale_002.inputs[1])
		#math_009.Value -> scale_002.Y
		node_tree.links.new(math_009.outputs[0], scale_002.inputs[2])
		#group_input.Blue/yellow -> math_008.Value
		node_tree.links.new(group_input.outputs[3], math_008.inputs[0])
		#clamp_006.Result -> math_010.Value
		node_tree.links.new(clamp_006.outputs[0], math_010.inputs[1])
		#clamp_006.Result -> math_011.Value
		node_tree.links.new(clamp_006.outputs[0], math_011.inputs[1])
		#rgb_curves_001.Image -> set_alpha_001.Image
		node_tree.links.new(rgb_curves_001.outputs[0], set_alpha_001.inputs[0])
		#rgb_curves_002.Image -> set_alpha_002.Image
		node_tree.links.new(rgb_curves_002.outputs[0], set_alpha_002.inputs[0])
		#separate_color.Alpha -> set_alpha_001.Alpha
		node_tree.links.new(separate_color.outputs[3], set_alpha_001.inputs[1])
		#separate_color.Alpha -> set_alpha_002.Alpha
		node_tree.links.new(separate_color.outputs[3], set_alpha_002.inputs[1])
		return node_tree
