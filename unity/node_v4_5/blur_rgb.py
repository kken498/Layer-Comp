import bpy
from ..node import *

class CompositorNodeBlurRGB(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeBlurRGB'
	bl_label='Blur RGB'
	bl_icon='PROP_CON'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Distortion"].default_value = 45
		self.inputs["G"].default_value = 0.15
		self.inputs["B"].default_value = 0.25

	def draw_buttons(self, context, layout):
		return

	def getNodetree(self, context):
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"

		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (1, 1, 1, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'
		image_socket_1.hide_value = True

		#Socket Offset
		offset_socket = node_tree.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketVector')
		offset_socket.default_value = (0.0, 0.0, 0.0)
		offset_socket.min_value = -1.0
		offset_socket.max_value = 1.0
		offset_socket.subtype = 'FACTOR'
		offset_socket.attribute_domain = 'POINT'
		offset_socket.default_input = 'VALUE'
		offset_socket.structure_type = 'AUTO'
		offset_socket.dimensions = 2

		#Socket Distortion
		distortion_socket = node_tree.interface.new_socket(name = "Distortion", in_out='INPUT', socket_type = 'NodeSocketFloat')
		distortion_socket.default_value = 45.0
		distortion_socket.min_value = 0.0
		distortion_socket.max_value = 100.0
		distortion_socket.subtype = 'NONE'
		distortion_socket.attribute_domain = 'POINT'
		distortion_socket.default_input = 'VALUE'
		distortion_socket.structure_type = 'AUTO'

		#Socket Blur Amount
		blur_amount_socket = node_tree.interface.new_socket(name = "Blur Amount", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blur_amount_socket.default_value = 0.0
		blur_amount_socket.min_value = 0.0
		blur_amount_socket.max_value = 100.0
		blur_amount_socket.subtype = 'FACTOR'
		blur_amount_socket.attribute_domain = 'POINT'
		blur_amount_socket.default_input = 'VALUE'
		blur_amount_socket.structure_type = 'AUTO'

		#Panel Blur
		blur_panel = node_tree.interface.new_panel("Blur")
		#Socket R
		r_socket = node_tree.interface.new_socket(name = "R", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = blur_panel)
		r_socket.default_value = 0.0
		r_socket.min_value = 0.0
		r_socket.max_value = 1.0
		r_socket.subtype = 'FACTOR'
		r_socket.attribute_domain = 'POINT'
		r_socket.default_input = 'VALUE'
		r_socket.structure_type = 'AUTO'

		#Socket G
		g_socket = node_tree.interface.new_socket(name = "G", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = blur_panel)
		g_socket.default_value = 0.15000000596046448
		g_socket.min_value = 0.0
		g_socket.max_value = 1.0
		g_socket.subtype = 'FACTOR'
		g_socket.attribute_domain = 'POINT'
		g_socket.default_input = 'VALUE'
		g_socket.structure_type = 'AUTO'

		#Socket B
		b_socket = node_tree.interface.new_socket(name = "B", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = blur_panel)
		b_socket.default_value = 0.25
		b_socket.min_value = 0.0
		b_socket.max_value = 1.0
		b_socket.subtype = 'FACTOR'
		b_socket.attribute_domain = 'POINT'
		b_socket.default_input = 'VALUE'
		b_socket.structure_type = 'AUTO'

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

		#node Translate.002
		translate_002 = node_tree.nodes.new("CompositorNodeTranslate")
		translate_002.name = "Translate.002"
		translate_002.interpolation = 'NEAREST'
		translate_002.wrap_axis = 'NONE'

		#node Reroute.001
		reroute_001 = node_tree.nodes.new("NodeReroute")
		reroute_001.name = "Reroute.001"
		reroute_001.socket_idname = "NodeSocketColor"
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

		#node Mix
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix"
		mix.blend_type = 'SCREEN'
		mix.clamp_factor = False
		mix.clamp_result = False
		mix.data_type = 'RGBA'
		mix.factor_mode = 'UNIFORM'
		#Factor_Float
		mix.inputs[0].default_value = 1.0
		#A_Color
		mix.inputs[6].default_value = (0.0, 0.0, 0.0, 1.0)

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

		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'SUBTRACT'
		math.use_clamp = False
		#Value
		math.inputs[0].default_value = 0.0

		#node Scale
		scale = node_tree.nodes.new("CompositorNodeScale")
		scale.name = "Scale"
		scale.frame_method = 'STRETCH'
		scale.interpolation = 'BILINEAR'
		scale.space = 'RELATIVE'

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'DIVIDE'
		math_001.use_clamp = False
		#Value_001
		math_001.inputs[1].default_value = 45.0

		#node Math.002
		math_002 = node_tree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MULTIPLY_ADD'
		math_002.use_clamp = False
		#Value
		math_002.inputs[0].default_value = 0.1
		#Value_002
		math_002.inputs[2].default_value = 1.0

		#node Math.003
		math_003 = node_tree.nodes.new("ShaderNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'MULTIPLY'
		math_003.use_clamp = False

		#node Blur
		blur = node_tree.nodes.new("CompositorNodeBlur")
		blur.name = "Blur"
		blur.filter_type = 'GAUSS'
		#Extend Bounds
		blur.inputs[2].default_value = False
		#Separable
		blur.inputs[3].default_value = True

		#node Group Input.001
		group_input_001 = node_tree.nodes.new("NodeGroupInput")
		group_input_001.name = "Group Input.001"

		#node Blur.001
		blur_001 = node_tree.nodes.new("CompositorNodeBlur")
		blur_001.name = "Blur.001"
		blur_001.filter_type = 'GAUSS'
		#Extend Bounds
		blur_001.inputs[2].default_value = False
		#Separable
		blur_001.inputs[3].default_value = True

		#node Blur.002
		blur_002 = node_tree.nodes.new("CompositorNodeBlur")
		blur_002.name = "Blur.002"
		blur_002.filter_type = 'GAUSS'
		#Extend Bounds
		blur_002.inputs[2].default_value = False
		#Separable
		blur_002.inputs[3].default_value = True

		#node Blur.003
		blur_003 = node_tree.nodes.new("CompositorNodeBlur")
		blur_003.name = "Blur.003"
		blur_003.filter_type = 'GAUSS'
		#Extend Bounds
		blur_003.inputs[2].default_value = False
		#Separable
		blur_003.inputs[3].default_value = True

		#node Math.004
		math_004 = node_tree.nodes.new("ShaderNodeMath")
		math_004.name = "Math.004"
		math_004.operation = 'MULTIPLY'
		math_004.use_clamp = False
		#Value_001
		math_004.inputs[1].default_value = 2.0

		#node Math.005
		math_005 = node_tree.nodes.new("ShaderNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'MULTIPLY'
		math_005.use_clamp = False
		#Value_001
		math_005.inputs[1].default_value = 300.0

		#node Math.006
		math_006 = node_tree.nodes.new("ShaderNodeMath")
		math_006.name = "Math.006"
		math_006.operation = 'MULTIPLY'
		math_006.use_clamp = False
		#Value_001
		math_006.inputs[1].default_value = 300.0

		#node Math.007
		math_007 = node_tree.nodes.new("ShaderNodeMath")
		math_007.name = "Math.007"
		math_007.operation = 'MULTIPLY'
		math_007.use_clamp = False
		#Value_001
		math_007.inputs[1].default_value = 300.0

		#node Separate XYZ
		separate_xyz = node_tree.nodes.new("ShaderNodeSeparateXYZ")
		separate_xyz.name = "Separate XYZ"

		#node Math.008
		math_008 = node_tree.nodes.new("ShaderNodeMath")
		math_008.name = "Math.008"
		math_008.operation = 'SUBTRACT'
		math_008.use_clamp = False
		#Value
		math_008.inputs[0].default_value = 0.0

		#node Vector Math
		vector_math = node_tree.nodes.new("ShaderNodeVectorMath")
		vector_math.name = "Vector Math"
		vector_math.operation = 'MULTIPLY'
		#Vector_001
		vector_math.inputs[1].default_value = (50.0, 50.0, 0.0)

		#node Math.009
		math_009 = node_tree.nodes.new("ShaderNodeMath")
		math_009.name = "Math.009"
		math_009.operation = 'DIVIDE'
		math_009.use_clamp = False
		#Value_001
		math_009.inputs[1].default_value = 45.0

		#node Math.010
		math_010 = node_tree.nodes.new("ShaderNodeMath")
		math_010.name = "Math.010"
		math_010.operation = 'MULTIPLY_ADD'
		math_010.use_clamp = False
		#Value
		math_010.inputs[0].default_value = 0.1
		#Value_002
		math_010.inputs[2].default_value = 1.0

		#node Math.011
		math_011 = node_tree.nodes.new("ShaderNodeMath")
		math_011.name = "Math.011"
		math_011.operation = 'MULTIPLY'
		math_011.use_clamp = False

		#node Separate XYZ.001
		separate_xyz_001 = node_tree.nodes.new("ShaderNodeSeparateXYZ")
		separate_xyz_001.name = "Separate XYZ.001"

		#node Math.012
		math_012 = node_tree.nodes.new("ShaderNodeMath")
		math_012.name = "Math.012"
		math_012.operation = 'ABSOLUTE'
		math_012.use_clamp = False

		#node Math.013
		math_013 = node_tree.nodes.new("ShaderNodeMath")
		math_013.name = "Math.013"
		math_013.operation = 'ABSOLUTE'
		math_013.use_clamp = False

		#initialize node_tree links
		#reroute_001.Output -> translate_002.Image
		node_tree.links.new(reroute_001.outputs[0], translate_002.inputs[0])
		#math_002.Value -> scale.X
		node_tree.links.new(math_002.outputs[0], scale.inputs[1])
		#blur_001.Image -> mix.B
		node_tree.links.new(blur_001.outputs[0], mix.inputs[7])
		#translate_002.Image -> rgb_curves_002.Image
		node_tree.links.new(translate_002.outputs[0], rgb_curves_002.inputs[1])
		#mix.Result -> mix_001.A
		node_tree.links.new(mix.outputs[2], mix_001.inputs[6])
		#reroute_001.Output -> rgb_curves_001.Image
		node_tree.links.new(reroute_001.outputs[0], rgb_curves_001.inputs[1])
		#mix_001.Result -> mix_002.A
		node_tree.links.new(mix_001.outputs[2], mix_002.inputs[6])
		#reroute_001.Output -> translate.Image
		node_tree.links.new(reroute_001.outputs[0], translate.inputs[0])
		#blur_002.Image -> mix_001.B
		node_tree.links.new(blur_002.outputs[0], mix_001.inputs[7])
		#math_001.Value -> math_002.Value
		node_tree.links.new(math_001.outputs[0], math_002.inputs[1])
		#translate.Image -> rgb_curves.Image
		node_tree.links.new(translate.outputs[0], rgb_curves.inputs[1])
		#scale.Image -> reroute_001.Input
		node_tree.links.new(scale.outputs[0], reroute_001.inputs[0])
		#blur_003.Image -> mix_002.B
		node_tree.links.new(blur_003.outputs[0], mix_002.inputs[7])
		#math.Value -> translate_002.X
		node_tree.links.new(math.outputs[0], translate_002.inputs[1])
		#group_input.Image -> scale.Image
		node_tree.links.new(group_input.outputs[0], scale.inputs[0])
		#blur.Image -> group_output.Image
		node_tree.links.new(blur.outputs[0], group_output.inputs[0])
		#mix_002.Result -> blur.Image
		node_tree.links.new(mix_002.outputs[2], blur.inputs[0])
		#rgb_curves.Image -> blur_001.Image
		node_tree.links.new(rgb_curves.outputs[0], blur_001.inputs[0])
		#rgb_curves_001.Image -> blur_002.Image
		node_tree.links.new(rgb_curves_001.outputs[0], blur_002.inputs[0])
		#rgb_curves_002.Image -> blur_003.Image
		node_tree.links.new(rgb_curves_002.outputs[0], blur_003.inputs[0])
		#math_004.Value -> blur.Size
		node_tree.links.new(math_004.outputs[0], blur.inputs[1])
		#math_007.Value -> blur_001.Size
		node_tree.links.new(math_007.outputs[0], blur_001.inputs[1])
		#math_006.Value -> blur_002.Size
		node_tree.links.new(math_006.outputs[0], blur_002.inputs[1])
		#math_005.Value -> blur_003.Size
		node_tree.links.new(math_005.outputs[0], blur_003.inputs[1])
		#group_input_001.Blur Amount -> math_004.Value
		node_tree.links.new(group_input_001.outputs[3], math_004.inputs[0])
		#group_input_001.B -> math_005.Value
		node_tree.links.new(group_input_001.outputs[6], math_005.inputs[0])
		#group_input_001.G -> math_006.Value
		node_tree.links.new(group_input_001.outputs[5], math_006.inputs[0])
		#group_input_001.R -> math_007.Value
		node_tree.links.new(group_input_001.outputs[4], math_007.inputs[0])
		#vector_math.Vector -> separate_xyz.Vector
		node_tree.links.new(vector_math.outputs[0], separate_xyz.inputs[0])
		#separate_xyz.X -> translate.X
		node_tree.links.new(separate_xyz.outputs[0], translate.inputs[1])
		#separate_xyz.Y -> math_008.Value
		node_tree.links.new(separate_xyz.outputs[1], math_008.inputs[1])
		#separate_xyz.X -> math.Value
		node_tree.links.new(separate_xyz.outputs[0], math.inputs[1])
		#separate_xyz.Y -> translate.Y
		node_tree.links.new(separate_xyz.outputs[1], translate.inputs[2])
		#math_008.Value -> translate_002.Y
		node_tree.links.new(math_008.outputs[0], translate_002.inputs[2])
		#group_input.Offset -> vector_math.Vector
		node_tree.links.new(group_input.outputs[1], vector_math.inputs[0])
		#group_input.Distortion -> math_003.Value
		node_tree.links.new(group_input.outputs[2], math_003.inputs[1])
		#math_003.Value -> math_001.Value
		node_tree.links.new(math_003.outputs[0], math_001.inputs[0])
		#math_009.Value -> math_010.Value
		node_tree.links.new(math_009.outputs[0], math_010.inputs[1])
		#math_011.Value -> math_009.Value
		node_tree.links.new(math_011.outputs[0], math_009.inputs[0])
		#math_010.Value -> scale.Y
		node_tree.links.new(math_010.outputs[0], scale.inputs[2])
		#group_input.Distortion -> math_011.Value
		node_tree.links.new(group_input.outputs[2], math_011.inputs[1])
		#group_input.Offset -> separate_xyz_001.Vector
		node_tree.links.new(group_input.outputs[1], separate_xyz_001.inputs[0])
		#math_012.Value -> math_003.Value
		node_tree.links.new(math_012.outputs[0], math_003.inputs[0])
		#math_013.Value -> math_011.Value
		node_tree.links.new(math_013.outputs[0], math_011.inputs[0])
		#separate_xyz_001.X -> math_012.Value
		node_tree.links.new(separate_xyz_001.outputs[0], math_012.inputs[0])
		#separate_xyz_001.Y -> math_013.Value
		node_tree.links.new(separate_xyz_001.outputs[1], math_013.inputs[0])
		return node_tree
