import bpy
from ..node import *

class CompositorNodeColorInnerShadowSingle(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeColorInnerShadowSingle'
	bl_label='Color Inner Shadow (Single)'
	bl_icon='ANTIALIASED'
	
	mode_items=(('STEP', 'Step', 'STEP'),
		('THRESHOLD', 'Threshould', 'THRESHOLD'),
		('DISTANCE', 'Distance', 'DISTANCE'),
		('FEATHER', 'Feather', 'FEATHER'))

	falloff_items=(('SMOOTH', 'Smooth', 'Smooth', 'SMOOTHCURVE', 0),
		('SPHERE', 'Sphere', 'Sphere', 'SPHERECURVE', 1),
		('ROOT', 'Root', 'Root', 'ROOTCURVE', 2),
		('INVERSE_SQUARE', 'Inverse Square', 'Inverse Square', 'INVERSESQUARECURVE', 3),
		('SHARP', 'Sharp', 'Sharp', 'SHARPCURVE', 4),
		('LINEAR', 'Linear', 'Linear', 'LINCURVE', 5))
		
	def update_mode(self, context):
		self.node_tree.nodes['Dilate/Erode'].mode = self.mode
	
	def update_falloff(self, context):
		self.node_tree.nodes['Dilate/Erode'].falloff = self.falloff

	mode : bpy.props.EnumProperty(default = 'FEATHER', items = mode_items, name = "Mode", update = update_mode)

	falloff : bpy.props.EnumProperty(default = 'SHARP', items = falloff_items, name = "Falloff", update = update_falloff)

	def init(self, context):
		self.getNodetree(context)
		self.mode = 'FEATHER'
		self.falloff = 'SHARP'
		self.inputs["Size"].default_value = 35
		self.inputs[6].default_value = True
		
		for input in self.inputs:
			if input.name == "Shadow Color":
				input.default_value = (0.92,0,0.059,1)
			if input.name == "Color":
				input.default_value = (0, 0.456, 0.9, 1.0)
			if input.name in ["Hue", "Saturation", "Value"]:
				input.default_value = 0.15


	def draw_buttons(self, context, layout):
		layout.prop(self, 'mode', text='Mode')
		if self.mode == "FEATHER":
			layout.prop(self, 'falloff', text='Falloff')

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"

		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (0.0, 0.0, 0.0, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'

		#Socket Matte
		matte_socket = node_tree.interface.new_socket(name = "Matte", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte_socket.default_value = 0.0
		matte_socket.min_value = -3.4028234663852886e+38
		matte_socket.max_value = 3.4028234663852886e+38
		matte_socket.subtype = 'NONE'
		matte_socket.attribute_domain = 'POINT'
		matte_socket.default_input = 'VALUE'
		matte_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Socket Shadow Color
		shadow_color_socket = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		shadow_color_socket.default_value = (0.921576976776123, 0.0, 0.05951099842786789, 1.0)
		shadow_color_socket.attribute_domain = 'POINT'
		shadow_color_socket.default_input = 'VALUE'
		shadow_color_socket.structure_type = 'AUTO'

		#Socket Size
		size_socket = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketInt')
		size_socket.default_value = 35
		size_socket.min_value = -2147483648
		size_socket.max_value = 2147483647
		size_socket.subtype = 'NONE'
		size_socket.attribute_domain = 'POINT'
		size_socket.default_input = 'VALUE'
		size_socket.structure_type = 'AUTO'

		#Socket Bias
		bias_socket = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat')
		bias_socket.default_value = 0.0
		bias_socket.min_value = 0.0
		bias_socket.max_value = 1.0
		bias_socket.subtype = 'FACTOR'
		bias_socket.attribute_domain = 'POINT'
		bias_socket.default_input = 'VALUE'
		bias_socket.structure_type = 'AUTO'

		#Socket Falloff Size
		falloff_size_socket = node_tree.interface.new_socket(name = "Falloff Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
		falloff_size_socket.default_value = 0.0
		falloff_size_socket.min_value = 0.0
		falloff_size_socket.max_value = 3.4028234663852886e+38
		falloff_size_socket.subtype = 'NONE'
		falloff_size_socket.attribute_domain = 'POINT'
		falloff_size_socket.default_input = 'VALUE'
		falloff_size_socket.structure_type = 'AUTO'

		#Socket Invert Color
		invert_color_socket = node_tree.interface.new_socket(name = "Invert Color", in_out='INPUT', socket_type = 'NodeSocketBool')
		invert_color_socket.default_value = False
		invert_color_socket.attribute_domain = 'POINT'
		invert_color_socket.default_input = 'VALUE'
		invert_color_socket.structure_type = 'AUTO'

		#Panel Color1
		color1_panel = node_tree.interface.new_panel("Color1")
		#Socket Enabled
		enabled_socket = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color1_panel)
		enabled_socket.default_value = True
		enabled_socket.attribute_domain = 'POINT'
		enabled_socket.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket.default_input = 'VALUE'
		enabled_socket.structure_type = 'AUTO'

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color1_panel)
		color_socket.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color_socket.attribute_domain = 'POINT'
		color_socket.default_input = 'VALUE'
		color_socket.structure_type = 'AUTO'

		#Socket Hue
		hue_socket = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel)
		hue_socket.default_value = 0.15000000596046448
		hue_socket.min_value = 0.0
		hue_socket.max_value = 1.0
		hue_socket.subtype = 'FACTOR'
		hue_socket.attribute_domain = 'POINT'
		hue_socket.default_input = 'VALUE'
		hue_socket.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel)
		saturation_socket.default_value = 0.15000000596046448
		saturation_socket.min_value = 0.0
		saturation_socket.max_value = 1.0
		saturation_socket.subtype = 'FACTOR'
		saturation_socket.attribute_domain = 'POINT'
		saturation_socket.default_input = 'VALUE'
		saturation_socket.structure_type = 'AUTO'

		#Socket Value
		value_socket = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel)
		value_socket.default_value = 0.15000000596046448
		value_socket.min_value = 0.0
		value_socket.max_value = 1.0
		value_socket.subtype = 'FACTOR'
		value_socket.attribute_domain = 'POINT'
		value_socket.default_input = 'VALUE'
		value_socket.structure_type = 'AUTO'


		#Panel Color2
		color2_panel = node_tree.interface.new_panel("Color2", default_closed=True)
		#Socket Enabled
		enabled_socket_1 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color2_panel)
		enabled_socket_1.default_value = False
		enabled_socket_1.attribute_domain = 'POINT'
		enabled_socket_1.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_1.default_input = 'VALUE'
		enabled_socket_1.structure_type = 'AUTO'

		#Socket Color
		color_socket_1 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color2_panel)
		color_socket_1.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color_socket_1.attribute_domain = 'POINT'
		color_socket_1.default_input = 'VALUE'
		color_socket_1.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_1 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel)
		hue_socket_1.default_value = 0.15000000596046448
		hue_socket_1.min_value = 0.0
		hue_socket_1.max_value = 1.0
		hue_socket_1.subtype = 'FACTOR'
		hue_socket_1.attribute_domain = 'POINT'
		hue_socket_1.default_input = 'VALUE'
		hue_socket_1.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_1 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel)
		saturation_socket_1.default_value = 0.15000000596046448
		saturation_socket_1.min_value = 0.0
		saturation_socket_1.max_value = 1.0
		saturation_socket_1.subtype = 'FACTOR'
		saturation_socket_1.attribute_domain = 'POINT'
		saturation_socket_1.default_input = 'VALUE'
		saturation_socket_1.structure_type = 'AUTO'

		#Socket Value
		value_socket_1 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel)
		value_socket_1.default_value = 0.15000000596046448
		value_socket_1.min_value = 0.0
		value_socket_1.max_value = 1.0
		value_socket_1.subtype = 'FACTOR'
		value_socket_1.attribute_domain = 'POINT'
		value_socket_1.default_input = 'VALUE'
		value_socket_1.structure_type = 'AUTO'


		#Panel Color3
		color3_panel = node_tree.interface.new_panel("Color3", default_closed=True)
		#Socket Enabled
		enabled_socket_2 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color3_panel)
		enabled_socket_2.default_value = False
		enabled_socket_2.attribute_domain = 'POINT'
		enabled_socket_2.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_2.default_input = 'VALUE'
		enabled_socket_2.structure_type = 'AUTO'

		#Socket Color
		color_socket_2 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color3_panel)
		color_socket_2.default_value = (0.0009089999948628247, 0.4564110040664673, 0.9130989909172058, 1.0)
		color_socket_2.attribute_domain = 'POINT'
		color_socket_2.default_input = 'VALUE'
		color_socket_2.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_2 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel)
		hue_socket_2.default_value = 0.15000000596046448
		hue_socket_2.min_value = 0.0
		hue_socket_2.max_value = 1.0
		hue_socket_2.subtype = 'FACTOR'
		hue_socket_2.attribute_domain = 'POINT'
		hue_socket_2.default_input = 'VALUE'
		hue_socket_2.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_2 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel)
		saturation_socket_2.default_value = 0.15000000596046448
		saturation_socket_2.min_value = 0.0
		saturation_socket_2.max_value = 1.0
		saturation_socket_2.subtype = 'FACTOR'
		saturation_socket_2.attribute_domain = 'POINT'
		saturation_socket_2.default_input = 'VALUE'
		saturation_socket_2.structure_type = 'AUTO'

		#Socket Value
		value_socket_2 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel)
		value_socket_2.default_value = 0.15000000596046448
		value_socket_2.min_value = 0.0
		value_socket_2.max_value = 1.0
		value_socket_2.subtype = 'FACTOR'
		value_socket_2.attribute_domain = 'POINT'
		value_socket_2.default_input = 'VALUE'
		value_socket_2.structure_type = 'AUTO'


		#Panel Color4
		color4_panel = node_tree.interface.new_panel("Color4", default_closed=True)
		#Socket Enabled
		enabled_socket_3 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color4_panel)
		enabled_socket_3.default_value = False
		enabled_socket_3.attribute_domain = 'POINT'
		enabled_socket_3.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_3.default_input = 'VALUE'
		enabled_socket_3.structure_type = 'AUTO'

		#Socket Color
		color_socket_3 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color4_panel)
		color_socket_3.default_value = (0.0009094758424907923, 0.4564112424850464, 0.9130989909172058, 1.0)
		color_socket_3.attribute_domain = 'POINT'
		color_socket_3.default_input = 'VALUE'
		color_socket_3.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_3 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel)
		hue_socket_3.default_value = 0.15000000596046448
		hue_socket_3.min_value = 0.0
		hue_socket_3.max_value = 1.0
		hue_socket_3.subtype = 'FACTOR'
		hue_socket_3.attribute_domain = 'POINT'
		hue_socket_3.default_input = 'VALUE'
		hue_socket_3.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_3 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel)
		saturation_socket_3.default_value = 0.15000000596046448
		saturation_socket_3.min_value = 0.0
		saturation_socket_3.max_value = 1.0
		saturation_socket_3.subtype = 'FACTOR'
		saturation_socket_3.attribute_domain = 'POINT'
		saturation_socket_3.default_input = 'VALUE'
		saturation_socket_3.structure_type = 'AUTO'

		#Socket Value
		value_socket_3 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel)
		value_socket_3.default_value = 0.15000000596046448
		value_socket_3.min_value = 0.0
		value_socket_3.max_value = 1.0
		value_socket_3.subtype = 'FACTOR'
		value_socket_3.attribute_domain = 'POINT'
		value_socket_3.default_input = 'VALUE'
		value_socket_3.structure_type = 'AUTO'



		#initialize node_tree nodes
		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Color Key
		color_key = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key.name = "Color Key"

		#node Dilate/Erode
		dilate_erode = node_tree.nodes.new("CompositorNodeDilateErode")
		dilate_erode.name = "Dilate/Erode"
		dilate_erode.falloff = 'SHARP'
		dilate_erode.mode = 'FEATHER'

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#node Mix
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.clamp_factor = True
		mix.clamp_result = False
		mix.data_type = 'RGBA'
		mix.factor_mode = 'UNIFORM'

		#node Math
		math = node_tree.nodes.new("CompositorNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = True

		#node Math.001
		math_001 = node_tree.nodes.new("CompositorNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'SUBTRACT'
		math_001.use_clamp = True

		#node Color Key.001
		color_key_001 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_001.name = "Color Key.001"

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"
		reroute.socket_idname = "NodeSocketColor"
		#node Color Key.002
		color_key_002 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_002.name = "Color Key.002"

		#node Color Key.003
		color_key_003 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_003.name = "Color Key.003"

		#node Mix.001
		mix_001 = node_tree.nodes.new("ShaderNodeMix")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MULTIPLY'
		mix_001.clamp_factor = False
		mix_001.clamp_result = False
		mix_001.data_type = 'RGBA'
		mix_001.factor_mode = 'UNIFORM'
		#A_Color
		mix_001.inputs[6].default_value = (1.0, 1.0, 1.0, 1.0)

		#node Mix.002
		mix_002 = node_tree.nodes.new("ShaderNodeMix")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MULTIPLY'
		mix_002.clamp_factor = False
		mix_002.clamp_result = False
		mix_002.data_type = 'RGBA'
		mix_002.factor_mode = 'UNIFORM'

		#node Mix.003
		mix_003 = node_tree.nodes.new("ShaderNodeMix")
		mix_003.name = "Mix.003"
		mix_003.blend_type = 'MULTIPLY'
		mix_003.clamp_factor = False
		mix_003.clamp_result = False
		mix_003.data_type = 'RGBA'
		mix_003.factor_mode = 'UNIFORM'

		#node Mix.004
		mix_004 = node_tree.nodes.new("ShaderNodeMix")
		mix_004.name = "Mix.004"
		mix_004.blend_type = 'MULTIPLY'
		mix_004.clamp_factor = False
		mix_004.clamp_result = False
		mix_004.data_type = 'RGBA'
		mix_004.factor_mode = 'UNIFORM'

		#node Reroute.001
		reroute_001 = node_tree.nodes.new("NodeReroute")
		reroute_001.name = "Reroute.001"
		reroute_001.socket_idname = "NodeSocketFloat"
		#node Map Range
		map_range = node_tree.nodes.new("ShaderNodeMapRange")
		map_range.name = "Map Range"
		map_range.clamp = True
		map_range.data_type = 'FLOAT'
		map_range.interpolation_type = 'LINEAR'
		#From Min
		map_range.inputs[1].default_value = 0.0
		#To Min
		map_range.inputs[3].default_value = 0.0
		#To Max
		map_range.inputs[4].default_value = 1.0

		#node Math.003
		math_003 = node_tree.nodes.new("CompositorNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'SUBTRACT'
		math_003.use_clamp = True
		#Value
		math_003.inputs[0].default_value = 1.0010000467300415

		#node Invert Color
		invert_color = node_tree.nodes.new("CompositorNodeInvert")
		invert_color.name = "Invert Color"
		#Fac
		invert_color.inputs[0].default_value = 1.0
		#Invert Alpha
		invert_color.inputs[3].default_value = False


		#Set locations
		group_input.location = (-743.43359375, 178.4457244873047)
		group_output.location = (2397.142333984375, -239.5004119873047)
		color_key.location = (-393.2270812988281, 108.9999008178711)
		dilate_erode.location = (742.0388793945312, 197.77940368652344)
		separate_color.location = (-388.5006103515625, 394.2288513183594)
		mix.location = (2035.61962890625, -214.9672088623047)
		math.location = (948.68798828125, 38.55568313598633)
		math_001.location = (1149.3056640625, -42.21436309814453)
		color_key_001.location = (-391.5237121582031, -108.18006134033203)
		reroute.location = (693.3333740234375, 1.5509834289550781)
		color_key_002.location = (-389.9678039550781, -329.57275390625)
		color_key_003.location = (-394.6355285644531, -533.5739135742188)
		mix_001.location = (-215.2241668701172, 70.15111541748047)
		mix_002.location = (-34.27775192260742, -5.57318115234375)
		mix_003.location = (162.6666717529297, -161.09974670410156)
		mix_004.location = (327.5274658203125, -206.5000457763672)
		reroute_001.location = (1590.478515625, -148.0016632080078)
		map_range.location = (1405.145263671875, -77.30054473876953)
		math_003.location = (891.78173828125, -270.00274658203125)
		invert_color.location = (507.9999694824219, -106.42691040039062)

		#Set dimensions
		group_input.width, group_input.height = 140.0, 100.0
		group_output.width, group_output.height = 140.0, 100.0
		color_key.width, color_key.height = 140.0, 100.0
		dilate_erode.width, dilate_erode.height = 140.0, 100.0
		separate_color.width, separate_color.height = 140.0, 100.0
		mix.width, mix.height = 140.0, 100.0
		math.width, math.height = 140.0, 100.0
		math_001.width, math_001.height = 140.0, 100.0
		color_key_001.width, color_key_001.height = 140.0, 100.0
		reroute.width, reroute.height = 8.0, 100.0
		color_key_002.width, color_key_002.height = 140.0, 100.0
		color_key_003.width, color_key_003.height = 140.0, 100.0
		mix_001.width, mix_001.height = 140.0, 100.0
		mix_002.width, mix_002.height = 140.0, 100.0
		mix_003.width, mix_003.height = 140.0, 100.0
		mix_004.width, mix_004.height = 140.0, 100.0
		reroute_001.width, reroute_001.height = 8.0, 100.0
		map_range.width, map_range.height = 140.0, 100.0
		math_003.width, math_003.height = 140.0, 100.0
		invert_color.width, invert_color.height = 140.0, 100.0

		#initialize node_tree links
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#group_input.Image -> color_key.Image
		node_tree.links.new(group_input.outputs[0], color_key.inputs[0])
		#group_input.Color -> color_key.Key Color
		node_tree.links.new(group_input.outputs[7], color_key.inputs[1])
		#group_input.Hue -> color_key.Hue
		node_tree.links.new(group_input.outputs[8], color_key.inputs[2])
		#group_input.Saturation -> color_key.Saturation
		node_tree.links.new(group_input.outputs[9], color_key.inputs[3])
		#group_input.Value -> color_key.Value
		node_tree.links.new(group_input.outputs[10], color_key.inputs[4])
		#reroute.Output -> dilate_erode.Mask
		node_tree.links.new(reroute.outputs[0], dilate_erode.inputs[0])
		#group_input.Size -> dilate_erode.Size
		node_tree.links.new(group_input.outputs[2], dilate_erode.inputs[1])
		#group_input.Falloff Size -> dilate_erode.Falloff Size
		node_tree.links.new(group_input.outputs[4], dilate_erode.inputs[2])
		#dilate_erode.Mask -> math.Value
		node_tree.links.new(dilate_erode.outputs[0], math.inputs[0])
		#separate_color.Alpha -> math.Value
		node_tree.links.new(separate_color.outputs[3], math.inputs[1])
		#math.Value -> math_001.Value
		node_tree.links.new(math.outputs[0], math_001.inputs[0])
		#reroute.Output -> math_001.Value
		node_tree.links.new(reroute.outputs[0], math_001.inputs[1])
		#reroute_001.Output -> mix.Factor
		node_tree.links.new(reroute_001.outputs[0], mix.inputs[0])
		#group_input.Image -> mix.A
		node_tree.links.new(group_input.outputs[0], mix.inputs[6])
		#group_input.Shadow Color -> mix.B
		node_tree.links.new(group_input.outputs[1], mix.inputs[7])
		#mix.Result -> group_output.Image
		node_tree.links.new(mix.outputs[2], group_output.inputs[0])
		#reroute_001.Output -> group_output.Matte
		node_tree.links.new(reroute_001.outputs[0], group_output.inputs[1])
		#group_input.Image -> color_key_001.Image
		node_tree.links.new(group_input.outputs[0], color_key_001.inputs[0])
		#invert_color.Color -> reroute.Input
		node_tree.links.new(invert_color.outputs[0], reroute.inputs[0])
		#group_input.Image -> color_key_002.Image
		node_tree.links.new(group_input.outputs[0], color_key_002.inputs[0])
		#group_input.Image -> color_key_003.Image
		node_tree.links.new(group_input.outputs[0], color_key_003.inputs[0])
		#color_key.Matte -> mix_001.B
		node_tree.links.new(color_key.outputs[1], mix_001.inputs[7])
		#group_input.Enabled -> mix_001.Factor
		node_tree.links.new(group_input.outputs[6], mix_001.inputs[0])
		#mix_001.Result -> mix_002.A
		node_tree.links.new(mix_001.outputs[2], mix_002.inputs[6])
		#group_input.Enabled -> mix_002.Factor
		node_tree.links.new(group_input.outputs[11], mix_002.inputs[0])
		#group_input.Color -> color_key_001.Key Color
		node_tree.links.new(group_input.outputs[12], color_key_001.inputs[1])
		#color_key_001.Matte -> mix_002.B
		node_tree.links.new(color_key_001.outputs[1], mix_002.inputs[7])
		#group_input.Hue -> color_key_001.Hue
		node_tree.links.new(group_input.outputs[13], color_key_001.inputs[2])
		#group_input.Saturation -> color_key_001.Saturation
		node_tree.links.new(group_input.outputs[14], color_key_001.inputs[3])
		#group_input.Value -> color_key_001.Value
		node_tree.links.new(group_input.outputs[15], color_key_001.inputs[4])
		#group_input.Color -> color_key_002.Key Color
		node_tree.links.new(group_input.outputs[17], color_key_002.inputs[1])
		#mix_002.Result -> mix_003.A
		node_tree.links.new(mix_002.outputs[2], mix_003.inputs[6])
		#color_key_002.Matte -> mix_003.B
		node_tree.links.new(color_key_002.outputs[1], mix_003.inputs[7])
		#group_input.Enabled -> mix_003.Factor
		node_tree.links.new(group_input.outputs[16], mix_003.inputs[0])
		#group_input.Hue -> color_key_002.Hue
		node_tree.links.new(group_input.outputs[18], color_key_002.inputs[2])
		#group_input.Saturation -> color_key_002.Saturation
		node_tree.links.new(group_input.outputs[19], color_key_002.inputs[3])
		#group_input.Value -> color_key_002.Value
		node_tree.links.new(group_input.outputs[20], color_key_002.inputs[4])
		#mix_003.Result -> mix_004.A
		node_tree.links.new(mix_003.outputs[2], mix_004.inputs[6])
		#group_input.Enabled -> mix_004.Factor
		node_tree.links.new(group_input.outputs[21], mix_004.inputs[0])
		#group_input.Color -> color_key_003.Key Color
		node_tree.links.new(group_input.outputs[22], color_key_003.inputs[1])
		#color_key_003.Matte -> mix_004.B
		node_tree.links.new(color_key_003.outputs[1], mix_004.inputs[7])
		#group_input.Hue -> color_key_003.Hue
		node_tree.links.new(group_input.outputs[23], color_key_003.inputs[2])
		#group_input.Saturation -> color_key_003.Saturation
		node_tree.links.new(group_input.outputs[24], color_key_003.inputs[3])
		#group_input.Value -> color_key_003.Value
		node_tree.links.new(group_input.outputs[25], color_key_003.inputs[4])
		#map_range.Result -> reroute_001.Input
		node_tree.links.new(map_range.outputs[0], reroute_001.inputs[0])
		#math_001.Value -> map_range.Value
		node_tree.links.new(math_001.outputs[0], map_range.inputs[0])
		#math_003.Value -> map_range.From Max
		node_tree.links.new(math_003.outputs[0], map_range.inputs[2])
		#group_input.Bias -> math_003.Value
		node_tree.links.new(group_input.outputs[3], math_003.inputs[1])
		#mix_004.Result -> invert_color.Color
		node_tree.links.new(mix_004.outputs[2], invert_color.inputs[1])
		#group_input.Invert Color -> invert_color.Invert Color
		node_tree.links.new(group_input.outputs[5], invert_color.inputs[2])
		return node_tree
		
class CompositorNodeColorInnerShadow(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeColorInnerShadow'
	bl_label='Color Inner Shadow'
	bl_icon='ANTIALIASED'
	
	mode_items=(('STEP', 'Step', 'STEP'),
		('THRESHOLD', 'Threshould', 'THRESHOLD'),
		('DISTANCE', 'Distance', 'DISTANCE'),
		('FEATHER', 'Feather', 'FEATHER'))

	falloff_items=(('SMOOTH', 'Smooth', 'Smooth', 'SMOOTHCURVE', 0),
		('SPHERE', 'Sphere', 'Sphere', 'SPHERECURVE', 1),
		('ROOT', 'Root', 'Root', 'ROOTCURVE', 2),
		('INVERSE_SQUARE', 'Inverse Square', 'Inverse Square', 'INVERSESQUARECURVE', 3),
		('SHARP', 'Sharp', 'Sharp', 'SHARPCURVE', 4),
		('LINEAR', 'Linear', 'Linear', 'LINCURVE', 5))
		
	def update_mode(self, context):
		for node in self.node_tree.nodes:
			if "Inner Shadow (Single)" in node.name:
				node.mode = self.mode
	
	def update_falloff(self, context):
		for node in self.node_tree.nodes:
			if "Inner Shadow (Single)" in node.name:
				node.falloff = self.falloff

	def update_count(self, context):
		if self.count >= 2:
			self.node_tree.nodes["Mix"].mute = False
			self.node_tree.nodes["Math"].mute = False
		else:
			self.node_tree.nodes["Mix"].mute = True
			self.node_tree.nodes["Math"].mute = True

		if self.count >= 3:
			self.node_tree.nodes["Mix.001"].mute = False
			self.node_tree.nodes["Math.001"].mute = False
		else:
			self.node_tree.nodes["Mix.001"].mute = True
			self.node_tree.nodes["Math.001"].mute = True

		if self.count >= 4:
			self.node_tree.nodes["Mix.002"].mute = False
			self.node_tree.nodes["Math.002"].mute = False
		else:
			self.node_tree.nodes["Mix.002"].mute = True
			self.node_tree.nodes["Math.002"].mute = True

	count : bpy.props.IntProperty(default = 1, name = "Count", update = update_count, min=1, max=4)

	mode : bpy.props.EnumProperty(default = 'FEATHER', items = mode_items, name = "Mode", update = update_mode)

	falloff : bpy.props.EnumProperty(default = 'SHARP', items = falloff_items, name = "Falloff", update = update_falloff)

	def init(self, context):
		self.getNodetree(context)
		self.count = 1
		self.mode = 'FEATHER'
		self.falloff = 'SHARP'
		self.inputs["Size"].default_value = 35
		self.inputs[6].default_value = True
		self.inputs[31].default_value = True
		self.inputs[56].default_value = True
		self.inputs[81].default_value = True
		
		for input in self.inputs:
			if input.name == "Shadow Color":
				input.default_value = (0.92,0,0.059,1)
			if input.name == "Color":
				input.default_value = (0, 0.456, 0.9, 1.0)
			if input.name in ["Hue", "Saturation", "Value"]:
				input.default_value = 0.15

	def draw_buttons(self, context, layout):
		layout.prop(self, 'mode', text='Mode')
		if self.mode == "FEATHER":
			layout.prop(self, 'falloff', text='Falloff')
		layout.prop(self, 'count')

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"

		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (0.0, 0.0, 0.0, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'

		#Socket Matte
		matte_socket = node_tree.interface.new_socket(name = "Matte", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte_socket.default_value = 0.0
		matte_socket.min_value = -3.4028234663852886e+38
		matte_socket.max_value = 3.4028234663852886e+38
		matte_socket.subtype = 'NONE'
		matte_socket.attribute_domain = 'POINT'
		matte_socket.default_input = 'VALUE'
		matte_socket.structure_type = 'AUTO'

		#Socket Matte1
		matte1_socket = node_tree.interface.new_socket(name = "Matte1", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte1_socket.default_value = 0.0
		matte1_socket.min_value = -3.4028234663852886e+38
		matte1_socket.max_value = 3.4028234663852886e+38
		matte1_socket.subtype = 'NONE'
		matte1_socket.attribute_domain = 'POINT'
		matte1_socket.default_input = 'VALUE'
		matte1_socket.structure_type = 'AUTO'

		#Socket Matte2
		matte2_socket = node_tree.interface.new_socket(name = "Matte2", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte2_socket.default_value = 0.0
		matte2_socket.min_value = -3.4028234663852886e+38
		matte2_socket.max_value = 3.4028234663852886e+38
		matte2_socket.subtype = 'NONE'
		matte2_socket.attribute_domain = 'POINT'
		matte2_socket.default_input = 'VALUE'
		matte2_socket.structure_type = 'AUTO'

		#Socket Matte3
		matte3_socket = node_tree.interface.new_socket(name = "Matte3", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte3_socket.default_value = 0.0
		matte3_socket.min_value = -3.4028234663852886e+38
		matte3_socket.max_value = 3.4028234663852886e+38
		matte3_socket.subtype = 'NONE'
		matte3_socket.attribute_domain = 'POINT'
		matte3_socket.default_input = 'VALUE'
		matte3_socket.structure_type = 'AUTO'

		#Socket Matte4
		matte4_socket = node_tree.interface.new_socket(name = "Matte4", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		matte4_socket.default_value = 0.0
		matte4_socket.min_value = -3.4028234663852886e+38
		matte4_socket.max_value = 3.4028234663852886e+38
		matte4_socket.subtype = 'NONE'
		matte4_socket.attribute_domain = 'POINT'
		matte4_socket.default_input = 'VALUE'
		matte4_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Panel Shadow1
		shadow1_panel = node_tree.interface.new_panel("Shadow1")
		#Socket Shadow Color
		shadow_color_socket = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = shadow1_panel)
		shadow_color_socket.default_value = (0.9200000166893005, 0.0, 0.05900000035762787, 1.0)
		shadow_color_socket.attribute_domain = 'POINT'
		shadow_color_socket.default_input = 'VALUE'
		shadow_color_socket.structure_type = 'AUTO'

		#Socket Size
		size_socket = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketInt', parent = shadow1_panel)
		size_socket.default_value = 35
		size_socket.min_value = -2147483648
		size_socket.max_value = 2147483647
		size_socket.subtype = 'NONE'
		size_socket.attribute_domain = 'POINT'
		size_socket.default_input = 'VALUE'
		size_socket.structure_type = 'AUTO'

		#Socket Bias
		bias_socket = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow1_panel)
		bias_socket.default_value = 0.0
		bias_socket.min_value = 0.0
		bias_socket.max_value = 1.0
		bias_socket.subtype = 'FACTOR'
		bias_socket.attribute_domain = 'POINT'
		bias_socket.default_input = 'VALUE'
		bias_socket.structure_type = 'AUTO'

		#Socket Falloff Size
		falloff_size_socket = node_tree.interface.new_socket(name = "Falloff Size", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow1_panel)
		falloff_size_socket.default_value = 0.0
		falloff_size_socket.min_value = 0.0
		falloff_size_socket.max_value = 3.4028234663852886e+38
		falloff_size_socket.subtype = 'NONE'
		falloff_size_socket.attribute_domain = 'POINT'
		falloff_size_socket.default_input = 'VALUE'
		falloff_size_socket.structure_type = 'AUTO'

		#Socket Invert Color
		invert_color_socket = node_tree.interface.new_socket(name = "Invert Color", in_out='INPUT', socket_type = 'NodeSocketBool', parent = shadow1_panel)
		invert_color_socket.default_value = False
		invert_color_socket.attribute_domain = 'POINT'
		invert_color_socket.default_input = 'VALUE'
		invert_color_socket.structure_type = 'AUTO'

		#Panel Color1
		color1_panel = node_tree.interface.new_panel("Color1")
		#Socket Enabled
		enabled_socket = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color1_panel)
		enabled_socket.default_value = True
		enabled_socket.attribute_domain = 'POINT'
		enabled_socket.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket.default_input = 'VALUE'
		enabled_socket.structure_type = 'AUTO'

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color1_panel)
		color_socket.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket.attribute_domain = 'POINT'
		color_socket.default_input = 'VALUE'
		color_socket.structure_type = 'AUTO'

		#Socket Hue
		hue_socket = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel)
		hue_socket.default_value = 0.15000000596046448
		hue_socket.min_value = 0.0
		hue_socket.max_value = 1.0
		hue_socket.subtype = 'FACTOR'
		hue_socket.attribute_domain = 'POINT'
		hue_socket.default_input = 'VALUE'
		hue_socket.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel)
		saturation_socket.default_value = 0.15000000596046448
		saturation_socket.min_value = 0.0
		saturation_socket.max_value = 1.0
		saturation_socket.subtype = 'FACTOR'
		saturation_socket.attribute_domain = 'POINT'
		saturation_socket.default_input = 'VALUE'
		saturation_socket.structure_type = 'AUTO'

		#Socket Value
		value_socket = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel)
		value_socket.default_value = 0.15000000596046448
		value_socket.min_value = 0.0
		value_socket.max_value = 1.0
		value_socket.subtype = 'FACTOR'
		value_socket.attribute_domain = 'POINT'
		value_socket.default_input = 'VALUE'
		value_socket.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color1_panel, shadow1_panel, 13)
		#Panel Color2
		color2_panel = node_tree.interface.new_panel("Color2", default_closed=True)
		#Socket Enabled
		enabled_socket_1 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color2_panel)
		enabled_socket_1.default_value = False
		enabled_socket_1.attribute_domain = 'POINT'
		enabled_socket_1.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_1.default_input = 'VALUE'
		enabled_socket_1.structure_type = 'AUTO'

		#Socket Color
		color_socket_1 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color2_panel)
		color_socket_1.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_1.attribute_domain = 'POINT'
		color_socket_1.default_input = 'VALUE'
		color_socket_1.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_1 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel)
		hue_socket_1.default_value = 0.15000000596046448
		hue_socket_1.min_value = 0.0
		hue_socket_1.max_value = 1.0
		hue_socket_1.subtype = 'FACTOR'
		hue_socket_1.attribute_domain = 'POINT'
		hue_socket_1.default_input = 'VALUE'
		hue_socket_1.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_1 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel)
		saturation_socket_1.default_value = 0.15000000596046448
		saturation_socket_1.min_value = 0.0
		saturation_socket_1.max_value = 1.0
		saturation_socket_1.subtype = 'FACTOR'
		saturation_socket_1.attribute_domain = 'POINT'
		saturation_socket_1.default_input = 'VALUE'
		saturation_socket_1.structure_type = 'AUTO'

		#Socket Value
		value_socket_1 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel)
		value_socket_1.default_value = 0.15000000596046448
		value_socket_1.min_value = 0.0
		value_socket_1.max_value = 1.0
		value_socket_1.subtype = 'FACTOR'
		value_socket_1.attribute_domain = 'POINT'
		value_socket_1.default_input = 'VALUE'
		value_socket_1.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color2_panel, shadow1_panel, 19)
		#Panel Color3
		color3_panel = node_tree.interface.new_panel("Color3", default_closed=True)
		#Socket Enabled
		enabled_socket_2 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color3_panel)
		enabled_socket_2.default_value = False
		enabled_socket_2.attribute_domain = 'POINT'
		enabled_socket_2.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_2.default_input = 'VALUE'
		enabled_socket_2.structure_type = 'AUTO'

		#Socket Color
		color_socket_2 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color3_panel)
		color_socket_2.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_2.attribute_domain = 'POINT'
		color_socket_2.default_input = 'VALUE'
		color_socket_2.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_2 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel)
		hue_socket_2.default_value = 0.15000000596046448
		hue_socket_2.min_value = 0.0
		hue_socket_2.max_value = 1.0
		hue_socket_2.subtype = 'FACTOR'
		hue_socket_2.attribute_domain = 'POINT'
		hue_socket_2.default_input = 'VALUE'
		hue_socket_2.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_2 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel)
		saturation_socket_2.default_value = 0.15000000596046448
		saturation_socket_2.min_value = 0.0
		saturation_socket_2.max_value = 1.0
		saturation_socket_2.subtype = 'FACTOR'
		saturation_socket_2.attribute_domain = 'POINT'
		saturation_socket_2.default_input = 'VALUE'
		saturation_socket_2.structure_type = 'AUTO'

		#Socket Value
		value_socket_2 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel)
		value_socket_2.default_value = 0.15000000596046448
		value_socket_2.min_value = 0.0
		value_socket_2.max_value = 1.0
		value_socket_2.subtype = 'FACTOR'
		value_socket_2.attribute_domain = 'POINT'
		value_socket_2.default_input = 'VALUE'
		value_socket_2.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color3_panel, shadow1_panel, 25)
		#Panel Color4
		color4_panel = node_tree.interface.new_panel("Color4", default_closed=True)
		#Socket Enabled
		enabled_socket_3 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color4_panel)
		enabled_socket_3.default_value = False
		enabled_socket_3.attribute_domain = 'POINT'
		enabled_socket_3.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_3.default_input = 'VALUE'
		enabled_socket_3.structure_type = 'AUTO'

		#Socket Color
		color_socket_3 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color4_panel)
		color_socket_3.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_3.attribute_domain = 'POINT'
		color_socket_3.default_input = 'VALUE'
		color_socket_3.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_3 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel)
		hue_socket_3.default_value = 0.15000000596046448
		hue_socket_3.min_value = 0.0
		hue_socket_3.max_value = 1.0
		hue_socket_3.subtype = 'FACTOR'
		hue_socket_3.attribute_domain = 'POINT'
		hue_socket_3.default_input = 'VALUE'
		hue_socket_3.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_3 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel)
		saturation_socket_3.default_value = 0.15000000596046448
		saturation_socket_3.min_value = 0.0
		saturation_socket_3.max_value = 1.0
		saturation_socket_3.subtype = 'FACTOR'
		saturation_socket_3.attribute_domain = 'POINT'
		saturation_socket_3.default_input = 'VALUE'
		saturation_socket_3.structure_type = 'AUTO'

		#Socket Value
		value_socket_3 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel)
		value_socket_3.default_value = 0.15000000596046448
		value_socket_3.min_value = 0.0
		value_socket_3.max_value = 1.0
		value_socket_3.subtype = 'FACTOR'
		value_socket_3.attribute_domain = 'POINT'
		value_socket_3.default_input = 'VALUE'
		value_socket_3.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color4_panel, shadow1_panel, 31)

		#Panel Shadow2
		shadow2_panel = node_tree.interface.new_panel("Shadow2", default_closed=True)
		#Socket Shadow Color
		shadow_color_socket_1 = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = shadow2_panel)
		shadow_color_socket_1.default_value = (0.9200000166893005, 0.0, 0.05900000035762787, 1.0)
		shadow_color_socket_1.attribute_domain = 'POINT'
		shadow_color_socket_1.default_input = 'VALUE'
		shadow_color_socket_1.structure_type = 'AUTO'

		#Socket Size
		size_socket_1 = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketInt', parent = shadow2_panel)
		size_socket_1.default_value = 35
		size_socket_1.min_value = -2147483648
		size_socket_1.max_value = 2147483647
		size_socket_1.subtype = 'NONE'
		size_socket_1.attribute_domain = 'POINT'
		size_socket_1.default_input = 'VALUE'
		size_socket_1.structure_type = 'AUTO'

		#Socket Bias
		bias_socket_1 = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow2_panel)
		bias_socket_1.default_value = 0.0
		bias_socket_1.min_value = 0.0
		bias_socket_1.max_value = 1.0
		bias_socket_1.subtype = 'FACTOR'
		bias_socket_1.attribute_domain = 'POINT'
		bias_socket_1.default_input = 'VALUE'
		bias_socket_1.structure_type = 'AUTO'

		#Socket Falloff Size
		falloff_size_socket_1 = node_tree.interface.new_socket(name = "Falloff Size", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow2_panel)
		falloff_size_socket_1.default_value = 0.0
		falloff_size_socket_1.min_value = 0.0
		falloff_size_socket_1.max_value = 3.4028234663852886e+38
		falloff_size_socket_1.subtype = 'NONE'
		falloff_size_socket_1.attribute_domain = 'POINT'
		falloff_size_socket_1.default_input = 'VALUE'
		falloff_size_socket_1.structure_type = 'AUTO'

		#Socket Invert Color
		invert_color_socket_1 = node_tree.interface.new_socket(name = "Invert Color", in_out='INPUT', socket_type = 'NodeSocketBool', parent = shadow2_panel)
		invert_color_socket_1.default_value = False
		invert_color_socket_1.attribute_domain = 'POINT'
		invert_color_socket_1.default_input = 'VALUE'
		invert_color_socket_1.structure_type = 'AUTO'

		#Panel Color1
		color1_panel_1 = node_tree.interface.new_panel("Color1")
		#Socket Enabled
		enabled_socket_4 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color1_panel_1)
		enabled_socket_4.default_value = True
		enabled_socket_4.attribute_domain = 'POINT'
		enabled_socket_4.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_4.default_input = 'VALUE'
		enabled_socket_4.structure_type = 'AUTO'

		#Socket Color
		color_socket_4 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color1_panel_1)
		color_socket_4.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_4.attribute_domain = 'POINT'
		color_socket_4.default_input = 'VALUE'
		color_socket_4.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_4 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel_1)
		hue_socket_4.default_value = 0.15000000596046448
		hue_socket_4.min_value = 0.0
		hue_socket_4.max_value = 1.0
		hue_socket_4.subtype = 'FACTOR'
		hue_socket_4.attribute_domain = 'POINT'
		hue_socket_4.default_input = 'VALUE'
		hue_socket_4.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_4 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel_1)
		saturation_socket_4.default_value = 0.15000000596046448
		saturation_socket_4.min_value = 0.0
		saturation_socket_4.max_value = 1.0
		saturation_socket_4.subtype = 'FACTOR'
		saturation_socket_4.attribute_domain = 'POINT'
		saturation_socket_4.default_input = 'VALUE'
		saturation_socket_4.structure_type = 'AUTO'

		#Socket Value
		value_socket_4 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel_1)
		value_socket_4.default_value = 0.15000000596046448
		value_socket_4.min_value = 0.0
		value_socket_4.max_value = 1.0
		value_socket_4.subtype = 'FACTOR'
		value_socket_4.attribute_domain = 'POINT'
		value_socket_4.default_input = 'VALUE'
		value_socket_4.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color1_panel_1, shadow2_panel, 43)
		#Panel Color2
		color2_panel_1 = node_tree.interface.new_panel("Color2", default_closed=True)
		#Socket Enabled
		enabled_socket_5 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color2_panel_1)
		enabled_socket_5.default_value = False
		enabled_socket_5.attribute_domain = 'POINT'
		enabled_socket_5.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_5.default_input = 'VALUE'
		enabled_socket_5.structure_type = 'AUTO'

		#Socket Color
		color_socket_5 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color2_panel_1)
		color_socket_5.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_5.attribute_domain = 'POINT'
		color_socket_5.default_input = 'VALUE'
		color_socket_5.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_5 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel_1)
		hue_socket_5.default_value = 0.15000000596046448
		hue_socket_5.min_value = 0.0
		hue_socket_5.max_value = 1.0
		hue_socket_5.subtype = 'FACTOR'
		hue_socket_5.attribute_domain = 'POINT'
		hue_socket_5.default_input = 'VALUE'
		hue_socket_5.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_5 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel_1)
		saturation_socket_5.default_value = 0.15000000596046448
		saturation_socket_5.min_value = 0.0
		saturation_socket_5.max_value = 1.0
		saturation_socket_5.subtype = 'FACTOR'
		saturation_socket_5.attribute_domain = 'POINT'
		saturation_socket_5.default_input = 'VALUE'
		saturation_socket_5.structure_type = 'AUTO'

		#Socket Value
		value_socket_5 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel_1)
		value_socket_5.default_value = 0.15000000596046448
		value_socket_5.min_value = 0.0
		value_socket_5.max_value = 1.0
		value_socket_5.subtype = 'FACTOR'
		value_socket_5.attribute_domain = 'POINT'
		value_socket_5.default_input = 'VALUE'
		value_socket_5.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color2_panel_1, shadow2_panel, 49)
		#Panel Color3
		color3_panel_1 = node_tree.interface.new_panel("Color3", default_closed=True)
		#Socket Enabled
		enabled_socket_6 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color3_panel_1)
		enabled_socket_6.default_value = False
		enabled_socket_6.attribute_domain = 'POINT'
		enabled_socket_6.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_6.default_input = 'VALUE'
		enabled_socket_6.structure_type = 'AUTO'

		#Socket Color
		color_socket_6 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color3_panel_1)
		color_socket_6.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_6.attribute_domain = 'POINT'
		color_socket_6.default_input = 'VALUE'
		color_socket_6.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_6 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel_1)
		hue_socket_6.default_value = 0.15000000596046448
		hue_socket_6.min_value = 0.0
		hue_socket_6.max_value = 1.0
		hue_socket_6.subtype = 'FACTOR'
		hue_socket_6.attribute_domain = 'POINT'
		hue_socket_6.default_input = 'VALUE'
		hue_socket_6.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_6 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel_1)
		saturation_socket_6.default_value = 0.15000000596046448
		saturation_socket_6.min_value = 0.0
		saturation_socket_6.max_value = 1.0
		saturation_socket_6.subtype = 'FACTOR'
		saturation_socket_6.attribute_domain = 'POINT'
		saturation_socket_6.default_input = 'VALUE'
		saturation_socket_6.structure_type = 'AUTO'

		#Socket Value
		value_socket_6 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel_1)
		value_socket_6.default_value = 0.15000000596046448
		value_socket_6.min_value = 0.0
		value_socket_6.max_value = 1.0
		value_socket_6.subtype = 'FACTOR'
		value_socket_6.attribute_domain = 'POINT'
		value_socket_6.default_input = 'VALUE'
		value_socket_6.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color3_panel_1, shadow2_panel, 55)
		#Panel Color4
		color4_panel_1 = node_tree.interface.new_panel("Color4", default_closed=True)
		#Socket Enabled
		enabled_socket_7 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color4_panel_1)
		enabled_socket_7.default_value = False
		enabled_socket_7.attribute_domain = 'POINT'
		enabled_socket_7.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_7.default_input = 'VALUE'
		enabled_socket_7.structure_type = 'AUTO'

		#Socket Color
		color_socket_7 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color4_panel_1)
		color_socket_7.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_7.attribute_domain = 'POINT'
		color_socket_7.default_input = 'VALUE'
		color_socket_7.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_7 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel_1)
		hue_socket_7.default_value = 0.15000000596046448
		hue_socket_7.min_value = 0.0
		hue_socket_7.max_value = 1.0
		hue_socket_7.subtype = 'FACTOR'
		hue_socket_7.attribute_domain = 'POINT'
		hue_socket_7.default_input = 'VALUE'
		hue_socket_7.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_7 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel_1)
		saturation_socket_7.default_value = 0.15000000596046448
		saturation_socket_7.min_value = 0.0
		saturation_socket_7.max_value = 1.0
		saturation_socket_7.subtype = 'FACTOR'
		saturation_socket_7.attribute_domain = 'POINT'
		saturation_socket_7.default_input = 'VALUE'
		saturation_socket_7.structure_type = 'AUTO'

		#Socket Value
		value_socket_7 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel_1)
		value_socket_7.default_value = 0.15000000596046448
		value_socket_7.min_value = 0.0
		value_socket_7.max_value = 1.0
		value_socket_7.subtype = 'FACTOR'
		value_socket_7.attribute_domain = 'POINT'
		value_socket_7.default_input = 'VALUE'
		value_socket_7.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color4_panel_1, shadow2_panel, 61)

		#Panel Shadow3
		shadow3_panel = node_tree.interface.new_panel("Shadow3", default_closed=True)
		#Socket Shadow Color
		shadow_color_socket_2 = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = shadow3_panel)
		shadow_color_socket_2.default_value = (0.9200000166893005, 0.0, 0.05900000035762787, 1.0)
		shadow_color_socket_2.attribute_domain = 'POINT'
		shadow_color_socket_2.default_input = 'VALUE'
		shadow_color_socket_2.structure_type = 'AUTO'

		#Socket Size
		size_socket_2 = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketInt', parent = shadow3_panel)
		size_socket_2.default_value = 35
		size_socket_2.min_value = -2147483648
		size_socket_2.max_value = 2147483647
		size_socket_2.subtype = 'NONE'
		size_socket_2.attribute_domain = 'POINT'
		size_socket_2.default_input = 'VALUE'
		size_socket_2.structure_type = 'AUTO'

		#Socket Bias
		bias_socket_2 = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow3_panel)
		bias_socket_2.default_value = 0.0
		bias_socket_2.min_value = 0.0
		bias_socket_2.max_value = 1.0
		bias_socket_2.subtype = 'FACTOR'
		bias_socket_2.attribute_domain = 'POINT'
		bias_socket_2.default_input = 'VALUE'
		bias_socket_2.structure_type = 'AUTO'

		#Socket Falloff Size
		falloff_size_socket_2 = node_tree.interface.new_socket(name = "Falloff Size", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow3_panel)
		falloff_size_socket_2.default_value = 0.0
		falloff_size_socket_2.min_value = 0.0
		falloff_size_socket_2.max_value = 3.4028234663852886e+38
		falloff_size_socket_2.subtype = 'NONE'
		falloff_size_socket_2.attribute_domain = 'POINT'
		falloff_size_socket_2.default_input = 'VALUE'
		falloff_size_socket_2.structure_type = 'AUTO'

		#Socket Invert Color
		invert_color_socket_2 = node_tree.interface.new_socket(name = "Invert Color", in_out='INPUT', socket_type = 'NodeSocketBool', parent = shadow3_panel)
		invert_color_socket_2.default_value = False
		invert_color_socket_2.attribute_domain = 'POINT'
		invert_color_socket_2.default_input = 'VALUE'
		invert_color_socket_2.structure_type = 'AUTO'

		#Panel Color1
		color1_panel_2 = node_tree.interface.new_panel("Color1")
		#Socket Enabled
		enabled_socket_8 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color1_panel_2)
		enabled_socket_8.default_value = True
		enabled_socket_8.attribute_domain = 'POINT'
		enabled_socket_8.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_8.default_input = 'VALUE'
		enabled_socket_8.structure_type = 'AUTO'

		#Socket Color
		color_socket_8 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color1_panel_2)
		color_socket_8.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_8.attribute_domain = 'POINT'
		color_socket_8.default_input = 'VALUE'
		color_socket_8.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_8 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel_2)
		hue_socket_8.default_value = 0.15000000596046448
		hue_socket_8.min_value = 0.0
		hue_socket_8.max_value = 1.0
		hue_socket_8.subtype = 'FACTOR'
		hue_socket_8.attribute_domain = 'POINT'
		hue_socket_8.default_input = 'VALUE'
		hue_socket_8.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_8 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel_2)
		saturation_socket_8.default_value = 0.15000000596046448
		saturation_socket_8.min_value = 0.0
		saturation_socket_8.max_value = 1.0
		saturation_socket_8.subtype = 'FACTOR'
		saturation_socket_8.attribute_domain = 'POINT'
		saturation_socket_8.default_input = 'VALUE'
		saturation_socket_8.structure_type = 'AUTO'

		#Socket Value
		value_socket_8 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel_2)
		value_socket_8.default_value = 0.15000000596046448
		value_socket_8.min_value = 0.0
		value_socket_8.max_value = 1.0
		value_socket_8.subtype = 'FACTOR'
		value_socket_8.attribute_domain = 'POINT'
		value_socket_8.default_input = 'VALUE'
		value_socket_8.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color1_panel_2, shadow3_panel, 73)
		#Panel Color2
		color2_panel_2 = node_tree.interface.new_panel("Color2", default_closed=True)
		#Socket Enabled
		enabled_socket_9 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color2_panel_2)
		enabled_socket_9.default_value = False
		enabled_socket_9.attribute_domain = 'POINT'
		enabled_socket_9.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_9.default_input = 'VALUE'
		enabled_socket_9.structure_type = 'AUTO'

		#Socket Color
		color_socket_9 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color2_panel_2)
		color_socket_9.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_9.attribute_domain = 'POINT'
		color_socket_9.default_input = 'VALUE'
		color_socket_9.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_9 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel_2)
		hue_socket_9.default_value = 0.15000000596046448
		hue_socket_9.min_value = 0.0
		hue_socket_9.max_value = 1.0
		hue_socket_9.subtype = 'FACTOR'
		hue_socket_9.attribute_domain = 'POINT'
		hue_socket_9.default_input = 'VALUE'
		hue_socket_9.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_9 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel_2)
		saturation_socket_9.default_value = 0.15000000596046448
		saturation_socket_9.min_value = 0.0
		saturation_socket_9.max_value = 1.0
		saturation_socket_9.subtype = 'FACTOR'
		saturation_socket_9.attribute_domain = 'POINT'
		saturation_socket_9.default_input = 'VALUE'
		saturation_socket_9.structure_type = 'AUTO'

		#Socket Value
		value_socket_9 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel_2)
		value_socket_9.default_value = 0.15000000596046448
		value_socket_9.min_value = 0.0
		value_socket_9.max_value = 1.0
		value_socket_9.subtype = 'FACTOR'
		value_socket_9.attribute_domain = 'POINT'
		value_socket_9.default_input = 'VALUE'
		value_socket_9.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color2_panel_2, shadow3_panel, 79)
		#Panel Color3
		color3_panel_2 = node_tree.interface.new_panel("Color3", default_closed=True)
		#Socket Enabled
		enabled_socket_10 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color3_panel_2)
		enabled_socket_10.default_value = False
		enabled_socket_10.attribute_domain = 'POINT'
		enabled_socket_10.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_10.default_input = 'VALUE'
		enabled_socket_10.structure_type = 'AUTO'

		#Socket Color
		color_socket_10 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color3_panel_2)
		color_socket_10.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_10.attribute_domain = 'POINT'
		color_socket_10.default_input = 'VALUE'
		color_socket_10.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_10 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel_2)
		hue_socket_10.default_value = 0.15000000596046448
		hue_socket_10.min_value = 0.0
		hue_socket_10.max_value = 1.0
		hue_socket_10.subtype = 'FACTOR'
		hue_socket_10.attribute_domain = 'POINT'
		hue_socket_10.default_input = 'VALUE'
		hue_socket_10.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_10 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel_2)
		saturation_socket_10.default_value = 0.15000000596046448
		saturation_socket_10.min_value = 0.0
		saturation_socket_10.max_value = 1.0
		saturation_socket_10.subtype = 'FACTOR'
		saturation_socket_10.attribute_domain = 'POINT'
		saturation_socket_10.default_input = 'VALUE'
		saturation_socket_10.structure_type = 'AUTO'

		#Socket Value
		value_socket_10 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel_2)
		value_socket_10.default_value = 0.15000000596046448
		value_socket_10.min_value = 0.0
		value_socket_10.max_value = 1.0
		value_socket_10.subtype = 'FACTOR'
		value_socket_10.attribute_domain = 'POINT'
		value_socket_10.default_input = 'VALUE'
		value_socket_10.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color3_panel_2, shadow3_panel, 85)
		#Panel Color4
		color4_panel_2 = node_tree.interface.new_panel("Color4", default_closed=True)
		#Socket Enabled
		enabled_socket_11 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color4_panel_2)
		enabled_socket_11.default_value = False
		enabled_socket_11.attribute_domain = 'POINT'
		enabled_socket_11.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_11.default_input = 'VALUE'
		enabled_socket_11.structure_type = 'AUTO'

		#Socket Color
		color_socket_11 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color4_panel_2)
		color_socket_11.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_11.attribute_domain = 'POINT'
		color_socket_11.default_input = 'VALUE'
		color_socket_11.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_11 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel_2)
		hue_socket_11.default_value = 0.15000000596046448
		hue_socket_11.min_value = 0.0
		hue_socket_11.max_value = 1.0
		hue_socket_11.subtype = 'FACTOR'
		hue_socket_11.attribute_domain = 'POINT'
		hue_socket_11.default_input = 'VALUE'
		hue_socket_11.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_11 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel_2)
		saturation_socket_11.default_value = 0.15000000596046448
		saturation_socket_11.min_value = 0.0
		saturation_socket_11.max_value = 1.0
		saturation_socket_11.subtype = 'FACTOR'
		saturation_socket_11.attribute_domain = 'POINT'
		saturation_socket_11.default_input = 'VALUE'
		saturation_socket_11.structure_type = 'AUTO'

		#Socket Value
		value_socket_11 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel_2)
		value_socket_11.default_value = 0.15000000596046448
		value_socket_11.min_value = 0.0
		value_socket_11.max_value = 1.0
		value_socket_11.subtype = 'FACTOR'
		value_socket_11.attribute_domain = 'POINT'
		value_socket_11.default_input = 'VALUE'
		value_socket_11.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color4_panel_2, shadow3_panel, 91)

		#Panel Shadow4
		shadow4_panel = node_tree.interface.new_panel("Shadow4", default_closed=True)
		#Socket Shadow Color
		shadow_color_socket_3 = node_tree.interface.new_socket(name = "Shadow Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = shadow4_panel)
		shadow_color_socket_3.default_value = (0.9200000166893005, 0.0, 0.05900000035762787, 1.0)
		shadow_color_socket_3.attribute_domain = 'POINT'
		shadow_color_socket_3.default_input = 'VALUE'
		shadow_color_socket_3.structure_type = 'AUTO'

		#Socket Size
		size_socket_3 = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketInt', parent = shadow4_panel)
		size_socket_3.default_value = 35
		size_socket_3.min_value = -2147483648
		size_socket_3.max_value = 2147483647
		size_socket_3.subtype = 'NONE'
		size_socket_3.attribute_domain = 'POINT'
		size_socket_3.default_input = 'VALUE'
		size_socket_3.structure_type = 'AUTO'

		#Socket Bias
		bias_socket_3 = node_tree.interface.new_socket(name = "Bias", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow4_panel)
		bias_socket_3.default_value = 0.0
		bias_socket_3.min_value = 0.0
		bias_socket_3.max_value = 1.0
		bias_socket_3.subtype = 'FACTOR'
		bias_socket_3.attribute_domain = 'POINT'
		bias_socket_3.default_input = 'VALUE'
		bias_socket_3.structure_type = 'AUTO'

		#Socket Falloff Size
		falloff_size_socket_3 = node_tree.interface.new_socket(name = "Falloff Size", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = shadow4_panel)
		falloff_size_socket_3.default_value = 0.0
		falloff_size_socket_3.min_value = 0.0
		falloff_size_socket_3.max_value = 3.4028234663852886e+38
		falloff_size_socket_3.subtype = 'NONE'
		falloff_size_socket_3.attribute_domain = 'POINT'
		falloff_size_socket_3.default_input = 'VALUE'
		falloff_size_socket_3.structure_type = 'AUTO'

		#Socket Invert Color
		invert_color_socket_3 = node_tree.interface.new_socket(name = "Invert Color", in_out='INPUT', socket_type = 'NodeSocketBool', parent = shadow4_panel)
		invert_color_socket_3.default_value = False
		invert_color_socket_3.attribute_domain = 'POINT'
		invert_color_socket_3.default_input = 'VALUE'
		invert_color_socket_3.structure_type = 'AUTO'

		#Panel Color1
		color1_panel_3 = node_tree.interface.new_panel("Color1")
		#Socket Enabled
		enabled_socket_12 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color1_panel_3)
		enabled_socket_12.default_value = True
		enabled_socket_12.attribute_domain = 'POINT'
		enabled_socket_12.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_12.default_input = 'VALUE'
		enabled_socket_12.structure_type = 'AUTO'

		#Socket Color
		color_socket_12 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color1_panel_3)
		color_socket_12.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_12.attribute_domain = 'POINT'
		color_socket_12.default_input = 'VALUE'
		color_socket_12.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_12 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel_3)
		hue_socket_12.default_value = 0.15000000596046448
		hue_socket_12.min_value = 0.0
		hue_socket_12.max_value = 1.0
		hue_socket_12.subtype = 'FACTOR'
		hue_socket_12.attribute_domain = 'POINT'
		hue_socket_12.default_input = 'VALUE'
		hue_socket_12.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_12 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel_3)
		saturation_socket_12.default_value = 0.15000000596046448
		saturation_socket_12.min_value = 0.0
		saturation_socket_12.max_value = 1.0
		saturation_socket_12.subtype = 'FACTOR'
		saturation_socket_12.attribute_domain = 'POINT'
		saturation_socket_12.default_input = 'VALUE'
		saturation_socket_12.structure_type = 'AUTO'

		#Socket Value
		value_socket_12 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color1_panel_3)
		value_socket_12.default_value = 0.15000000596046448
		value_socket_12.min_value = 0.0
		value_socket_12.max_value = 1.0
		value_socket_12.subtype = 'FACTOR'
		value_socket_12.attribute_domain = 'POINT'
		value_socket_12.default_input = 'VALUE'
		value_socket_12.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color1_panel_3, shadow4_panel, 103)
		#Panel Color2
		color2_panel_3 = node_tree.interface.new_panel("Color2", default_closed=True)
		#Socket Enabled
		enabled_socket_13 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color2_panel_3)
		enabled_socket_13.default_value = False
		enabled_socket_13.attribute_domain = 'POINT'
		enabled_socket_13.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_13.default_input = 'VALUE'
		enabled_socket_13.structure_type = 'AUTO'

		#Socket Color
		color_socket_13 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color2_panel_3)
		color_socket_13.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_13.attribute_domain = 'POINT'
		color_socket_13.default_input = 'VALUE'
		color_socket_13.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_13 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel_3)
		hue_socket_13.default_value = 0.15000000596046448
		hue_socket_13.min_value = 0.0
		hue_socket_13.max_value = 1.0
		hue_socket_13.subtype = 'FACTOR'
		hue_socket_13.attribute_domain = 'POINT'
		hue_socket_13.default_input = 'VALUE'
		hue_socket_13.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_13 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel_3)
		saturation_socket_13.default_value = 0.15000000596046448
		saturation_socket_13.min_value = 0.0
		saturation_socket_13.max_value = 1.0
		saturation_socket_13.subtype = 'FACTOR'
		saturation_socket_13.attribute_domain = 'POINT'
		saturation_socket_13.default_input = 'VALUE'
		saturation_socket_13.structure_type = 'AUTO'

		#Socket Value
		value_socket_13 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color2_panel_3)
		value_socket_13.default_value = 0.15000000596046448
		value_socket_13.min_value = 0.0
		value_socket_13.max_value = 1.0
		value_socket_13.subtype = 'FACTOR'
		value_socket_13.attribute_domain = 'POINT'
		value_socket_13.default_input = 'VALUE'
		value_socket_13.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color2_panel_3, shadow4_panel, 109)
		#Panel Color3
		color3_panel_3 = node_tree.interface.new_panel("Color3", default_closed=True)
		#Socket Enabled
		enabled_socket_14 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color3_panel_3)
		enabled_socket_14.default_value = False
		enabled_socket_14.attribute_domain = 'POINT'
		enabled_socket_14.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_14.default_input = 'VALUE'
		enabled_socket_14.structure_type = 'AUTO'

		#Socket Color
		color_socket_14 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color3_panel_3)
		color_socket_14.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_14.attribute_domain = 'POINT'
		color_socket_14.default_input = 'VALUE'
		color_socket_14.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_14 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel_3)
		hue_socket_14.default_value = 0.15000000596046448
		hue_socket_14.min_value = 0.0
		hue_socket_14.max_value = 1.0
		hue_socket_14.subtype = 'FACTOR'
		hue_socket_14.attribute_domain = 'POINT'
		hue_socket_14.default_input = 'VALUE'
		hue_socket_14.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_14 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel_3)
		saturation_socket_14.default_value = 0.15000000596046448
		saturation_socket_14.min_value = 0.0
		saturation_socket_14.max_value = 1.0
		saturation_socket_14.subtype = 'FACTOR'
		saturation_socket_14.attribute_domain = 'POINT'
		saturation_socket_14.default_input = 'VALUE'
		saturation_socket_14.structure_type = 'AUTO'

		#Socket Value
		value_socket_14 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color3_panel_3)
		value_socket_14.default_value = 0.15000000596046448
		value_socket_14.min_value = 0.0
		value_socket_14.max_value = 1.0
		value_socket_14.subtype = 'FACTOR'
		value_socket_14.attribute_domain = 'POINT'
		value_socket_14.default_input = 'VALUE'
		value_socket_14.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color3_panel_3, shadow4_panel, 115)
		#Panel Color4
		color4_panel_3 = node_tree.interface.new_panel("Color4", default_closed=True)
		#Socket Enabled
		enabled_socket_15 = node_tree.interface.new_socket(name = "Enabled", in_out='INPUT', socket_type = 'NodeSocketBool', parent = color4_panel_3)
		enabled_socket_15.default_value = False
		enabled_socket_15.attribute_domain = 'POINT'
		enabled_socket_15.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		enabled_socket_15.default_input = 'VALUE'
		enabled_socket_15.structure_type = 'AUTO'

		#Socket Color
		color_socket_15 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color4_panel_3)
		color_socket_15.default_value = (0.0, 0.4560000002384186, 0.8999999761581421, 1.0)
		color_socket_15.attribute_domain = 'POINT'
		color_socket_15.default_input = 'VALUE'
		color_socket_15.structure_type = 'AUTO'

		#Socket Hue
		hue_socket_15 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel_3)
		hue_socket_15.default_value = 0.15000000596046448
		hue_socket_15.min_value = 0.0
		hue_socket_15.max_value = 1.0
		hue_socket_15.subtype = 'FACTOR'
		hue_socket_15.attribute_domain = 'POINT'
		hue_socket_15.default_input = 'VALUE'
		hue_socket_15.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_15 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel_3)
		saturation_socket_15.default_value = 0.15000000596046448
		saturation_socket_15.min_value = 0.0
		saturation_socket_15.max_value = 1.0
		saturation_socket_15.subtype = 'FACTOR'
		saturation_socket_15.attribute_domain = 'POINT'
		saturation_socket_15.default_input = 'VALUE'
		saturation_socket_15.structure_type = 'AUTO'

		#Socket Value
		value_socket_15 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color4_panel_3)
		value_socket_15.default_value = 0.15000000596046448
		value_socket_15.min_value = 0.0
		value_socket_15.max_value = 1.0
		value_socket_15.subtype = 'FACTOR'
		value_socket_15.attribute_domain = 'POINT'
		value_socket_15.default_input = 'VALUE'
		value_socket_15.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(color4_panel_3, shadow4_panel, 121)


		#initialize node_tree nodes
		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Mix
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.clamp_factor = True
		mix.clamp_result = False
		mix.data_type = 'RGBA'
		mix.factor_mode = 'UNIFORM'

		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'ADD'
		math.use_clamp = False

		#node Inner Shadow (Single)
		inner_shadow__single_ = node_tree.nodes.new("CompositorNodeInnerShadowSingle")
		inner_shadow__single_.name = "Inner Shadow (Single)"

		#node Inner Shadow (Single).001
		inner_shadow__single__001 = node_tree.nodes.new("CompositorNodeInnerShadowSingle")
		inner_shadow__single__001.name = "Inner Shadow (Single).001"

		#node Inner Shadow (Single).002
		inner_shadow__single__002 = node_tree.nodes.new("CompositorNodeInnerShadowSingle")
		inner_shadow__single__002.name = "Inner Shadow (Single).002"

		#node Mix.001
		mix_001 = node_tree.nodes.new("ShaderNodeMix")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.clamp_factor = True
		mix_001.clamp_result = False
		mix_001.data_type = 'RGBA'
		mix_001.factor_mode = 'UNIFORM'

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'ADD'
		math_001.use_clamp = False

		#node Inner Shadow (Single).003
		inner_shadow__single__003 = node_tree.nodes.new("CompositorNodeInnerShadowSingle")
		inner_shadow__single__003.name = "Inner Shadow (Single).003"

		#node Mix.002
		mix_002 = node_tree.nodes.new("ShaderNodeMix")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MIX'
		mix_002.clamp_factor = True
		mix_002.clamp_result = False
		mix_002.data_type = 'RGBA'
		mix_002.factor_mode = 'UNIFORM'

		#node Math.002
		math_002 = node_tree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'ADD'
		math_002.use_clamp = False

		#initialize node_tree links
		#mix_002.Result -> group_output.Image
		node_tree.links.new(mix_002.outputs[2], group_output.inputs[0])
		#math_002.Value -> group_output.Matte
		node_tree.links.new(math_002.outputs[0], group_output.inputs[1])
		#group_input.Image -> inner_shadow__single_.Image
		node_tree.links.new(group_input.outputs[0], inner_shadow__single_.inputs[0])
		#group_input.Shadow Color -> inner_shadow__single_.Shadow Color
		node_tree.links.new(group_input.outputs[1], inner_shadow__single_.inputs[1])
		#group_input.Size -> inner_shadow__single_.Size
		node_tree.links.new(group_input.outputs[2], inner_shadow__single_.inputs[2])
		#group_input.Bias -> inner_shadow__single_.Bias
		node_tree.links.new(group_input.outputs[3], inner_shadow__single_.inputs[3])
		#group_input.Falloff Size -> inner_shadow__single_.Falloff Size
		node_tree.links.new(group_input.outputs[4], inner_shadow__single_.inputs[4])
		#group_input.Invert Color -> inner_shadow__single_.Invert Color
		node_tree.links.new(group_input.outputs[5], inner_shadow__single_.inputs[5])
		#group_input.Enabled -> inner_shadow__single_.Enabled
		node_tree.links.new(group_input.outputs[6], inner_shadow__single_.inputs[6])
		#group_input.Color -> inner_shadow__single_.Color
		node_tree.links.new(group_input.outputs[7], inner_shadow__single_.inputs[7])
		#group_input.Hue -> inner_shadow__single_.Hue
		node_tree.links.new(group_input.outputs[8], inner_shadow__single_.inputs[8])
		#group_input.Saturation -> inner_shadow__single_.Saturation
		node_tree.links.new(group_input.outputs[9], inner_shadow__single_.inputs[9])
		#group_input.Value -> inner_shadow__single_.Value
		node_tree.links.new(group_input.outputs[10], inner_shadow__single_.inputs[10])
		#group_input.Enabled -> inner_shadow__single_.Enabled
		node_tree.links.new(group_input.outputs[11], inner_shadow__single_.inputs[11])
		#group_input.Color -> inner_shadow__single_.Color
		node_tree.links.new(group_input.outputs[12], inner_shadow__single_.inputs[12])
		#group_input.Hue -> inner_shadow__single_.Hue
		node_tree.links.new(group_input.outputs[13], inner_shadow__single_.inputs[13])
		#group_input.Saturation -> inner_shadow__single_.Saturation
		node_tree.links.new(group_input.outputs[14], inner_shadow__single_.inputs[14])
		#group_input.Value -> inner_shadow__single_.Value
		node_tree.links.new(group_input.outputs[15], inner_shadow__single_.inputs[15])
		#group_input.Enabled -> inner_shadow__single_.Enabled
		node_tree.links.new(group_input.outputs[16], inner_shadow__single_.inputs[16])
		#group_input.Color -> inner_shadow__single_.Color
		node_tree.links.new(group_input.outputs[17], inner_shadow__single_.inputs[17])
		#group_input.Hue -> inner_shadow__single_.Hue
		node_tree.links.new(group_input.outputs[18], inner_shadow__single_.inputs[18])
		#group_input.Saturation -> inner_shadow__single_.Saturation
		node_tree.links.new(group_input.outputs[19], inner_shadow__single_.inputs[19])
		#group_input.Value -> inner_shadow__single_.Value
		node_tree.links.new(group_input.outputs[20], inner_shadow__single_.inputs[20])
		#group_input.Enabled -> inner_shadow__single_.Enabled
		node_tree.links.new(group_input.outputs[21], inner_shadow__single_.inputs[21])
		#group_input.Color -> inner_shadow__single_.Color
		node_tree.links.new(group_input.outputs[22], inner_shadow__single_.inputs[22])
		#group_input.Hue -> inner_shadow__single_.Hue
		node_tree.links.new(group_input.outputs[23], inner_shadow__single_.inputs[23])
		#group_input.Saturation -> inner_shadow__single_.Saturation
		node_tree.links.new(group_input.outputs[24], inner_shadow__single_.inputs[24])
		#group_input.Value -> inner_shadow__single_.Value
		node_tree.links.new(group_input.outputs[25], inner_shadow__single_.inputs[25])
		#inner_shadow__single_.Image -> mix.A
		node_tree.links.new(inner_shadow__single_.outputs[0], mix.inputs[6])
		#inner_shadow__single_.Matte -> math.Value
		node_tree.links.new(inner_shadow__single_.outputs[1], math.inputs[0])
		#group_input.Image -> inner_shadow__single__001.Image
		node_tree.links.new(group_input.outputs[0], inner_shadow__single__001.inputs[0])
		#group_input.Shadow Color -> inner_shadow__single__001.Shadow Color
		node_tree.links.new(group_input.outputs[26], inner_shadow__single__001.inputs[1])
		#group_input.Size -> inner_shadow__single__001.Size
		node_tree.links.new(group_input.outputs[27], inner_shadow__single__001.inputs[2])
		#group_input.Bias -> inner_shadow__single__001.Bias
		node_tree.links.new(group_input.outputs[28], inner_shadow__single__001.inputs[3])
		#group_input.Falloff Size -> inner_shadow__single__001.Falloff Size
		node_tree.links.new(group_input.outputs[29], inner_shadow__single__001.inputs[4])
		#group_input.Invert Color -> inner_shadow__single__001.Invert Color
		node_tree.links.new(group_input.outputs[30], inner_shadow__single__001.inputs[5])
		#group_input.Enabled -> inner_shadow__single__001.Enabled
		node_tree.links.new(group_input.outputs[31], inner_shadow__single__001.inputs[6])
		#group_input.Color -> inner_shadow__single__001.Color
		node_tree.links.new(group_input.outputs[32], inner_shadow__single__001.inputs[7])
		#group_input.Hue -> inner_shadow__single__001.Hue
		node_tree.links.new(group_input.outputs[33], inner_shadow__single__001.inputs[8])
		#group_input.Saturation -> inner_shadow__single__001.Saturation
		node_tree.links.new(group_input.outputs[34], inner_shadow__single__001.inputs[9])
		#group_input.Value -> inner_shadow__single__001.Value
		node_tree.links.new(group_input.outputs[35], inner_shadow__single__001.inputs[10])
		#group_input.Enabled -> inner_shadow__single__001.Enabled
		node_tree.links.new(group_input.outputs[36], inner_shadow__single__001.inputs[11])
		#group_input.Color -> inner_shadow__single__001.Color
		node_tree.links.new(group_input.outputs[37], inner_shadow__single__001.inputs[12])
		#group_input.Hue -> inner_shadow__single__001.Hue
		node_tree.links.new(group_input.outputs[38], inner_shadow__single__001.inputs[13])
		#group_input.Saturation -> inner_shadow__single__001.Saturation
		node_tree.links.new(group_input.outputs[39], inner_shadow__single__001.inputs[14])
		#group_input.Value -> inner_shadow__single__001.Value
		node_tree.links.new(group_input.outputs[40], inner_shadow__single__001.inputs[15])
		#group_input.Enabled -> inner_shadow__single__001.Enabled
		node_tree.links.new(group_input.outputs[41], inner_shadow__single__001.inputs[16])
		#group_input.Color -> inner_shadow__single__001.Color
		node_tree.links.new(group_input.outputs[42], inner_shadow__single__001.inputs[17])
		#group_input.Hue -> inner_shadow__single__001.Hue
		node_tree.links.new(group_input.outputs[43], inner_shadow__single__001.inputs[18])
		#group_input.Saturation -> inner_shadow__single__001.Saturation
		node_tree.links.new(group_input.outputs[44], inner_shadow__single__001.inputs[19])
		#group_input.Value -> inner_shadow__single__001.Value
		node_tree.links.new(group_input.outputs[45], inner_shadow__single__001.inputs[20])
		#group_input.Enabled -> inner_shadow__single__001.Enabled
		node_tree.links.new(group_input.outputs[46], inner_shadow__single__001.inputs[21])
		#group_input.Color -> inner_shadow__single__001.Color
		node_tree.links.new(group_input.outputs[47], inner_shadow__single__001.inputs[22])
		#group_input.Hue -> inner_shadow__single__001.Hue
		node_tree.links.new(group_input.outputs[48], inner_shadow__single__001.inputs[23])
		#group_input.Saturation -> inner_shadow__single__001.Saturation
		node_tree.links.new(group_input.outputs[49], inner_shadow__single__001.inputs[24])
		#group_input.Value -> inner_shadow__single__001.Value
		node_tree.links.new(group_input.outputs[50], inner_shadow__single__001.inputs[25])
		#inner_shadow__single__001.Image -> mix.B
		node_tree.links.new(inner_shadow__single__001.outputs[0], mix.inputs[7])
		#inner_shadow__single__001.Matte -> mix.Factor
		node_tree.links.new(inner_shadow__single__001.outputs[1], mix.inputs[0])
		#inner_shadow__single__001.Matte -> math.Value
		node_tree.links.new(inner_shadow__single__001.outputs[1], math.inputs[1])
		#group_input.Shadow Color -> inner_shadow__single__002.Shadow Color
		node_tree.links.new(group_input.outputs[51], inner_shadow__single__002.inputs[1])
		#group_input.Image -> inner_shadow__single__002.Image
		node_tree.links.new(group_input.outputs[0], inner_shadow__single__002.inputs[0])
		#group_input.Size -> inner_shadow__single__002.Size
		node_tree.links.new(group_input.outputs[52], inner_shadow__single__002.inputs[2])
		#group_input.Bias -> inner_shadow__single__002.Bias
		node_tree.links.new(group_input.outputs[53], inner_shadow__single__002.inputs[3])
		#group_input.Falloff Size -> inner_shadow__single__002.Falloff Size
		node_tree.links.new(group_input.outputs[54], inner_shadow__single__002.inputs[4])
		#group_input.Invert Color -> inner_shadow__single__002.Invert Color
		node_tree.links.new(group_input.outputs[55], inner_shadow__single__002.inputs[5])
		#group_input.Enabled -> inner_shadow__single__002.Enabled
		node_tree.links.new(group_input.outputs[56], inner_shadow__single__002.inputs[6])
		#group_input.Color -> inner_shadow__single__002.Color
		node_tree.links.new(group_input.outputs[57], inner_shadow__single__002.inputs[7])
		#group_input.Hue -> inner_shadow__single__002.Hue
		node_tree.links.new(group_input.outputs[58], inner_shadow__single__002.inputs[8])
		#group_input.Saturation -> inner_shadow__single__002.Saturation
		node_tree.links.new(group_input.outputs[59], inner_shadow__single__002.inputs[9])
		#group_input.Value -> inner_shadow__single__002.Value
		node_tree.links.new(group_input.outputs[60], inner_shadow__single__002.inputs[10])
		#group_input.Enabled -> inner_shadow__single__002.Enabled
		node_tree.links.new(group_input.outputs[61], inner_shadow__single__002.inputs[11])
		#group_input.Color -> inner_shadow__single__002.Color
		node_tree.links.new(group_input.outputs[62], inner_shadow__single__002.inputs[12])
		#group_input.Hue -> inner_shadow__single__002.Hue
		node_tree.links.new(group_input.outputs[63], inner_shadow__single__002.inputs[13])
		#group_input.Saturation -> inner_shadow__single__002.Saturation
		node_tree.links.new(group_input.outputs[64], inner_shadow__single__002.inputs[14])
		#group_input.Value -> inner_shadow__single__002.Value
		node_tree.links.new(group_input.outputs[65], inner_shadow__single__002.inputs[15])
		#group_input.Enabled -> inner_shadow__single__002.Enabled
		node_tree.links.new(group_input.outputs[66], inner_shadow__single__002.inputs[16])
		#group_input.Color -> inner_shadow__single__002.Color
		node_tree.links.new(group_input.outputs[67], inner_shadow__single__002.inputs[17])
		#group_input.Hue -> inner_shadow__single__002.Hue
		node_tree.links.new(group_input.outputs[68], inner_shadow__single__002.inputs[18])
		#group_input.Saturation -> inner_shadow__single__002.Saturation
		node_tree.links.new(group_input.outputs[69], inner_shadow__single__002.inputs[19])
		#group_input.Value -> inner_shadow__single__002.Value
		node_tree.links.new(group_input.outputs[70], inner_shadow__single__002.inputs[20])
		#group_input.Enabled -> inner_shadow__single__002.Enabled
		node_tree.links.new(group_input.outputs[71], inner_shadow__single__002.inputs[21])
		#group_input.Color -> inner_shadow__single__002.Color
		node_tree.links.new(group_input.outputs[72], inner_shadow__single__002.inputs[22])
		#group_input.Hue -> inner_shadow__single__002.Hue
		node_tree.links.new(group_input.outputs[73], inner_shadow__single__002.inputs[23])
		#group_input.Saturation -> inner_shadow__single__002.Saturation
		node_tree.links.new(group_input.outputs[74], inner_shadow__single__002.inputs[24])
		#group_input.Value -> inner_shadow__single__002.Value
		node_tree.links.new(group_input.outputs[75], inner_shadow__single__002.inputs[25])
		#mix.Result -> mix_001.A
		node_tree.links.new(mix.outputs[2], mix_001.inputs[6])
		#inner_shadow__single__002.Image -> mix_001.B
		node_tree.links.new(inner_shadow__single__002.outputs[0], mix_001.inputs[7])
		#inner_shadow__single__002.Matte -> mix_001.Factor
		node_tree.links.new(inner_shadow__single__002.outputs[1], mix_001.inputs[0])
		#math.Value -> math_001.Value
		node_tree.links.new(math.outputs[0], math_001.inputs[0])
		#inner_shadow__single__002.Matte -> math_001.Value
		node_tree.links.new(inner_shadow__single__002.outputs[1], math_001.inputs[1])
		#group_input.Image -> inner_shadow__single__003.Image
		node_tree.links.new(group_input.outputs[0], inner_shadow__single__003.inputs[0])
		#group_input.Shadow Color -> inner_shadow__single__003.Shadow Color
		node_tree.links.new(group_input.outputs[76], inner_shadow__single__003.inputs[1])
		#group_input.Size -> inner_shadow__single__003.Size
		node_tree.links.new(group_input.outputs[77], inner_shadow__single__003.inputs[2])
		#group_input.Bias -> inner_shadow__single__003.Bias
		node_tree.links.new(group_input.outputs[78], inner_shadow__single__003.inputs[3])
		#group_input.Falloff Size -> inner_shadow__single__003.Falloff Size
		node_tree.links.new(group_input.outputs[79], inner_shadow__single__003.inputs[4])
		#group_input.Invert Color -> inner_shadow__single__003.Invert Color
		node_tree.links.new(group_input.outputs[80], inner_shadow__single__003.inputs[5])
		#group_input.Enabled -> inner_shadow__single__003.Enabled
		node_tree.links.new(group_input.outputs[81], inner_shadow__single__003.inputs[6])
		#group_input.Color -> inner_shadow__single__003.Color
		node_tree.links.new(group_input.outputs[82], inner_shadow__single__003.inputs[7])
		#group_input.Hue -> inner_shadow__single__003.Hue
		node_tree.links.new(group_input.outputs[83], inner_shadow__single__003.inputs[8])
		#group_input.Saturation -> inner_shadow__single__003.Saturation
		node_tree.links.new(group_input.outputs[84], inner_shadow__single__003.inputs[9])
		#group_input.Value -> inner_shadow__single__003.Value
		node_tree.links.new(group_input.outputs[85], inner_shadow__single__003.inputs[10])
		#group_input.Enabled -> inner_shadow__single__003.Enabled
		node_tree.links.new(group_input.outputs[86], inner_shadow__single__003.inputs[11])
		#group_input.Color -> inner_shadow__single__003.Color
		node_tree.links.new(group_input.outputs[87], inner_shadow__single__003.inputs[12])
		#group_input.Hue -> inner_shadow__single__003.Hue
		node_tree.links.new(group_input.outputs[88], inner_shadow__single__003.inputs[13])
		#group_input.Saturation -> inner_shadow__single__003.Saturation
		node_tree.links.new(group_input.outputs[89], inner_shadow__single__003.inputs[14])
		#group_input.Value -> inner_shadow__single__003.Value
		node_tree.links.new(group_input.outputs[90], inner_shadow__single__003.inputs[15])
		#group_input.Enabled -> inner_shadow__single__003.Enabled
		node_tree.links.new(group_input.outputs[91], inner_shadow__single__003.inputs[16])
		#group_input.Color -> inner_shadow__single__003.Color
		node_tree.links.new(group_input.outputs[92], inner_shadow__single__003.inputs[17])
		#group_input.Hue -> inner_shadow__single__003.Hue
		node_tree.links.new(group_input.outputs[93], inner_shadow__single__003.inputs[18])
		#group_input.Saturation -> inner_shadow__single__003.Saturation
		node_tree.links.new(group_input.outputs[94], inner_shadow__single__003.inputs[19])
		#group_input.Value -> inner_shadow__single__003.Value
		node_tree.links.new(group_input.outputs[95], inner_shadow__single__003.inputs[20])
		#group_input.Color -> inner_shadow__single__003.Color
		node_tree.links.new(group_input.outputs[97], inner_shadow__single__003.inputs[22])
		#group_input.Enabled -> inner_shadow__single__003.Enabled
		node_tree.links.new(group_input.outputs[96], inner_shadow__single__003.inputs[21])
		#group_input.Hue -> inner_shadow__single__003.Hue
		node_tree.links.new(group_input.outputs[98], inner_shadow__single__003.inputs[23])
		#group_input.Saturation -> inner_shadow__single__003.Saturation
		node_tree.links.new(group_input.outputs[99], inner_shadow__single__003.inputs[24])
		#mix_001.Result -> mix_002.A
		node_tree.links.new(mix_001.outputs[2], mix_002.inputs[6])
		#math_001.Value -> math_002.Value
		node_tree.links.new(math_001.outputs[0], math_002.inputs[0])
		#inner_shadow__single__003.Matte -> math_002.Value
		node_tree.links.new(inner_shadow__single__003.outputs[1], math_002.inputs[1])
		#inner_shadow__single__003.Image -> mix_002.B
		node_tree.links.new(inner_shadow__single__003.outputs[0], mix_002.inputs[7])
		#inner_shadow__single__003.Matte -> mix_002.Factor
		node_tree.links.new(inner_shadow__single__003.outputs[1], mix_002.inputs[0])
		#group_input.Value -> inner_shadow__single__003.Value
		node_tree.links.new(group_input.outputs[100], inner_shadow__single__003.inputs[25])
		#inner_shadow__single_.Matte -> group_output.Matte1
		node_tree.links.new(inner_shadow__single_.outputs[1], group_output.inputs[2])
		#inner_shadow__single__001.Matte -> group_output.Matte2
		node_tree.links.new(inner_shadow__single__001.outputs[1], group_output.inputs[3])
		#inner_shadow__single__002.Matte -> group_output.Matte3
		node_tree.links.new(inner_shadow__single__002.outputs[1], group_output.inputs[4])
		#inner_shadow__single__003.Matte -> group_output.Matte4
		node_tree.links.new(inner_shadow__single__003.outputs[1], group_output.inputs[5])
		return node_tree
