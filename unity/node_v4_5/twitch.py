import bpy
from ..node import *

class CompositorNodeTwitch(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeTwitch'
	bl_label='Twitch'
	bl_icon='GHOST_ENABLED'

	def init(self, context):
		self.getNodetree(context)
		self.inputs[5].default_value = 3
		self.inputs[6].default_value = 0.5
		self.inputs[8].default_value = (1.0,0.361307,0.0,1)

		self.inputs[9].default_value = 3
		self.inputs[10].default_value = 2

		self.inputs[12].default_value = 3
		self.inputs[13].default_value = 50

		self.inputs[15].default_value = 3
		self.inputs[16].default_value = 15
		self.inputs[18].default_value = 1

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
		image_socket.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Panel Enabled
		enabled_panel = node_tree.interface.new_panel("Enabled")
		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketBool', parent = enabled_panel)
		color_socket.default_value = False
		color_socket.attribute_domain = 'POINT'
		color_socket.default_input = 'VALUE'
		color_socket.structure_type = 'AUTO'

		#Socket Light
		light_socket = node_tree.interface.new_socket(name = "Light", in_out='INPUT', socket_type = 'NodeSocketBool', parent = enabled_panel)
		light_socket.default_value = False
		light_socket.attribute_domain = 'POINT'
		light_socket.default_input = 'VALUE'
		light_socket.structure_type = 'AUTO'

		#Socket Blur
		blur_socket = node_tree.interface.new_socket(name = "Blur", in_out='INPUT', socket_type = 'NodeSocketBool', parent = enabled_panel)
		blur_socket.default_value = False
		blur_socket.attribute_domain = 'POINT'
		blur_socket.default_input = 'VALUE'
		blur_socket.structure_type = 'AUTO'

		#Socket Slide
		slide_socket = node_tree.interface.new_socket(name = "Slide", in_out='INPUT', socket_type = 'NodeSocketBool', parent = enabled_panel)
		slide_socket.default_value = False
		slide_socket.attribute_domain = 'POINT'
		slide_socket.default_input = 'VALUE'
		slide_socket.structure_type = 'AUTO'


		#Panel Color
		color_panel = node_tree.interface.new_panel("Color")
		#Socket Speed
		speed_socket = node_tree.interface.new_socket(name = "Speed", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color_panel)
		speed_socket.default_value = 3.0
		speed_socket.min_value = -1000.0
		speed_socket.max_value = 1000.0
		speed_socket.subtype = 'NONE'
		speed_socket.attribute_domain = 'POINT'
		speed_socket.default_input = 'VALUE'
		speed_socket.structure_type = 'AUTO'

		#Socket Amount
		amount_socket = node_tree.interface.new_socket(name = "Amount", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color_panel)
		amount_socket.default_value = 0.5
		amount_socket.min_value = 0.0
		amount_socket.max_value = 1.0
		amount_socket.subtype = 'NONE'
		amount_socket.attribute_domain = 'POINT'
		amount_socket.default_input = 'VALUE'
		amount_socket.structure_type = 'AUTO'

		#Socket Offset
		offset_socket = node_tree.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = color_panel)
		offset_socket.default_value = 0.0
		offset_socket.min_value = -10000.0
		offset_socket.max_value = 10000.0
		offset_socket.subtype = 'NONE'
		offset_socket.attribute_domain = 'POINT'
		offset_socket.default_input = 'VALUE'
		offset_socket.structure_type = 'AUTO'

		#Socket Color
		color_socket_1 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color_panel)
		color_socket_1.default_value = (1.0, 0.36130720376968384, 0.0, 1.0)
		color_socket_1.attribute_domain = 'POINT'
		color_socket_1.default_input = 'VALUE'
		color_socket_1.structure_type = 'AUTO'


		#Panel Light
		light_panel = node_tree.interface.new_panel("Light")
		#Socket Speed
		speed_socket_1 = node_tree.interface.new_socket(name = "Speed", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = light_panel)
		speed_socket_1.default_value = 3.0
		speed_socket_1.min_value = -1000.0
		speed_socket_1.max_value = 1000.0
		speed_socket_1.subtype = 'NONE'
		speed_socket_1.attribute_domain = 'POINT'
		speed_socket_1.default_input = 'VALUE'
		speed_socket_1.structure_type = 'AUTO'

		#Socket Amount
		amount_socket_1 = node_tree.interface.new_socket(name = "Amount", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = light_panel)
		amount_socket_1.default_value = 2.0
		amount_socket_1.min_value = 0.0
		amount_socket_1.max_value = 100.0
		amount_socket_1.subtype = 'NONE'
		amount_socket_1.attribute_domain = 'POINT'
		amount_socket_1.default_input = 'VALUE'
		amount_socket_1.structure_type = 'AUTO'

		#Socket Offset
		offset_socket_1 = node_tree.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = light_panel)
		offset_socket_1.default_value = 0.0
		offset_socket_1.min_value = -10000.0
		offset_socket_1.max_value = 10000.0
		offset_socket_1.subtype = 'NONE'
		offset_socket_1.attribute_domain = 'POINT'
		offset_socket_1.default_input = 'VALUE'
		offset_socket_1.structure_type = 'AUTO'


		#Panel Blur
		blur_panel = node_tree.interface.new_panel("Blur")
		#Socket Speed
		speed_socket_2 = node_tree.interface.new_socket(name = "Speed", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = blur_panel)
		speed_socket_2.default_value = 3.0
		speed_socket_2.min_value = -1000.0
		speed_socket_2.max_value = 1000.0
		speed_socket_2.subtype = 'NONE'
		speed_socket_2.attribute_domain = 'POINT'
		speed_socket_2.default_input = 'VALUE'
		speed_socket_2.structure_type = 'AUTO'

		#Socket Amount
		amount_socket_2 = node_tree.interface.new_socket(name = "Amount", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = blur_panel)
		amount_socket_2.default_value = 50.0
		amount_socket_2.min_value = 0.0
		amount_socket_2.max_value = 100.0
		amount_socket_2.subtype = 'NONE'
		amount_socket_2.attribute_domain = 'POINT'
		amount_socket_2.default_input = 'VALUE'
		amount_socket_2.structure_type = 'AUTO'

		#Socket Offset
		offset_socket_2 = node_tree.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = blur_panel)
		offset_socket_2.default_value = 0.0
		offset_socket_2.min_value = -10000.0
		offset_socket_2.max_value = 10000.0
		offset_socket_2.subtype = 'NONE'
		offset_socket_2.attribute_domain = 'POINT'
		offset_socket_2.default_input = 'VALUE'
		offset_socket_2.structure_type = 'AUTO'


		#Panel Slide
		slide_panel = node_tree.interface.new_panel("Slide")
		#Socket Speed
		speed_socket_3 = node_tree.interface.new_socket(name = "Speed", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = slide_panel)
		speed_socket_3.default_value = 3.0
		speed_socket_3.min_value = -1000.0
		speed_socket_3.max_value = 1000.0
		speed_socket_3.subtype = 'NONE'
		speed_socket_3.attribute_domain = 'POINT'
		speed_socket_3.default_input = 'VALUE'
		speed_socket_3.structure_type = 'AUTO'

		#Socket Amount
		amount_socket_3 = node_tree.interface.new_socket(name = "Amount", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = slide_panel)
		amount_socket_3.default_value = 15.0
		amount_socket_3.min_value = 0.0
		amount_socket_3.max_value = 100.0
		amount_socket_3.subtype = 'NONE'
		amount_socket_3.attribute_domain = 'POINT'
		amount_socket_3.default_input = 'VALUE'
		amount_socket_3.structure_type = 'AUTO'

		#Socket Offset
		offset_socket_3 = node_tree.interface.new_socket(name = "Offset", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = slide_panel)
		offset_socket_3.default_value = 0.0
		offset_socket_3.min_value = -10000.0
		offset_socket_3.max_value = 10000.0
		offset_socket_3.subtype = 'NONE'
		offset_socket_3.attribute_domain = 'POINT'
		offset_socket_3.default_input = 'VALUE'
		offset_socket_3.structure_type = 'AUTO'

		#Socket Shutter
		shutter_socket = node_tree.interface.new_socket(name = "Shutter", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = slide_panel)
		shutter_socket.default_value = 1.0
		shutter_socket.min_value = 0.0
		shutter_socket.max_value = 3.4028234663852886e+38
		shutter_socket.subtype = 'NONE'
		shutter_socket.attribute_domain = 'POINT'
		shutter_socket.description = "Time between shutter opening and closing in frames"
		shutter_socket.default_input = 'VALUE'
		shutter_socket.structure_type = 'AUTO'



		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Scene Time
		scene_time = node_tree.nodes.new("CompositorNodeSceneTime")
		scene_time.name = "Scene Time"

		#node Math.016
		math_016 = node_tree.nodes.new("ShaderNodeMath")
		math_016.name = "Math.016"
		math_016.operation = 'SINE'
		math_016.use_clamp = False

		#node Noise Texture
		noise_texture = node_tree.nodes.new("ShaderNodeTexNoise")
		noise_texture.name = "Noise Texture"
		noise_texture.noise_dimensions = '1D'
		noise_texture.noise_type = 'FBM'
		noise_texture.normalize = False
		#Detail
		noise_texture.inputs[3].default_value = 2.0
		#Roughness
		noise_texture.inputs[4].default_value = 0.0
		#Lacunarity
		noise_texture.inputs[5].default_value = 0.0
		#Distortion
		noise_texture.inputs[8].default_value = 0.0

		#node Mix.007
		mix_007 = node_tree.nodes.new("ShaderNodeMix")
		mix_007.name = "Mix.007"
		mix_007.blend_type = 'MIX'
		mix_007.clamp_factor = True
		mix_007.clamp_result = False
		mix_007.data_type = 'FLOAT'
		mix_007.factor_mode = 'UNIFORM'
		#A_Float
		mix_007.inputs[2].default_value = 0.0

		#node Exposure
		exposure = node_tree.nodes.new("CompositorNodeExposure")
		exposure.name = "Exposure"

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'MAXIMUM'
		math_001.use_clamp = False
		#Value_001
		math_001.inputs[1].default_value = 0.0

		#node Math.002
		math_002 = node_tree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MULTIPLY'
		math_002.use_clamp = False

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"
		reroute.socket_idname = "NodeSocketFloat"
		#node Math.018
		math_018 = node_tree.nodes.new("ShaderNodeMath")
		math_018.name = "Math.018"
		math_018.operation = 'SINE'
		math_018.use_clamp = False

		#node Noise Texture.001
		noise_texture_001 = node_tree.nodes.new("ShaderNodeTexNoise")
		noise_texture_001.name = "Noise Texture.001"
		noise_texture_001.noise_dimensions = '1D'
		noise_texture_001.noise_type = 'FBM'
		noise_texture_001.normalize = False
		#Detail
		noise_texture_001.inputs[3].default_value = 2.0
		#Roughness
		noise_texture_001.inputs[4].default_value = 0.0
		#Lacunarity
		noise_texture_001.inputs[5].default_value = 0.0
		#Distortion
		noise_texture_001.inputs[8].default_value = 0.0

		#node Mix.008
		mix_008 = node_tree.nodes.new("ShaderNodeMix")
		mix_008.name = "Mix.008"
		mix_008.blend_type = 'MIX'
		mix_008.clamp_factor = True
		mix_008.clamp_result = False
		mix_008.data_type = 'FLOAT'
		mix_008.factor_mode = 'UNIFORM'
		#A_Float
		mix_008.inputs[2].default_value = 0.0

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

		#node Translate
		translate = node_tree.nodes.new("CompositorNodeTranslate")
		translate.name = "Translate"
		translate.interpolation = 'NEAREST'
		translate.wrap_axis = 'NONE'

		#node Vector Blur
		vector_blur = node_tree.nodes.new("CompositorNodeVecBlur")
		vector_blur.name = "Vector Blur"
		#Z
		vector_blur.inputs[1].default_value = 0.0
		#Samples
		vector_blur.inputs[3].default_value = 32

		#node Math.020
		math_020 = node_tree.nodes.new("ShaderNodeMath")
		math_020.name = "Math.020"
		math_020.operation = 'SINE'
		math_020.use_clamp = False

		#node Noise Texture.002
		noise_texture_002 = node_tree.nodes.new("ShaderNodeTexNoise")
		noise_texture_002.name = "Noise Texture.002"
		noise_texture_002.noise_dimensions = '1D'
		noise_texture_002.noise_type = 'FBM'
		noise_texture_002.normalize = False
		#Detail
		noise_texture_002.inputs[3].default_value = 2.0
		#Roughness
		noise_texture_002.inputs[4].default_value = 0.5
		#Lacunarity
		noise_texture_002.inputs[5].default_value = 2.0
		#Distortion
		noise_texture_002.inputs[8].default_value = 0.0

		#node Mix.009
		mix_009 = node_tree.nodes.new("ShaderNodeMix")
		mix_009.name = "Mix.009"
		mix_009.blend_type = 'MIX'
		mix_009.clamp_factor = True
		mix_009.clamp_result = False
		mix_009.data_type = 'FLOAT'
		mix_009.factor_mode = 'UNIFORM'
		#A_Float
		mix_009.inputs[2].default_value = 0.0

		#node Math.004
		math_004 = node_tree.nodes.new("ShaderNodeMath")
		math_004.name = "Math.004"
		math_004.operation = 'MULTIPLY'
		math_004.use_clamp = False

		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'ADD'
		math.use_clamp = False

		#node Mix.010
		mix_010 = node_tree.nodes.new("ShaderNodeMix")
		mix_010.name = "Mix.010"
		mix_010.blend_type = 'MIX'
		mix_010.clamp_factor = True
		mix_010.clamp_result = False
		mix_010.data_type = 'FLOAT'
		mix_010.factor_mode = 'UNIFORM'
		#A_Float
		mix_010.inputs[2].default_value = 0.0

		#node Math.005
		math_005 = node_tree.nodes.new("ShaderNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'MULTIPLY'
		math_005.use_clamp = False
		#Value_001
		math_005.inputs[1].default_value = 5.0

		#node Combine XYZ
		combine_xyz = node_tree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz.name = "Combine XYZ"
		#Z
		combine_xyz.inputs[2].default_value = 0.0

		#node Math.021
		math_021 = node_tree.nodes.new("ShaderNodeMath")
		math_021.name = "Math.021"
		math_021.operation = 'SINE'
		math_021.use_clamp = False

		#node Math.006
		math_006 = node_tree.nodes.new("ShaderNodeMath")
		math_006.name = "Math.006"
		math_006.operation = 'MULTIPLY'
		math_006.use_clamp = False

		#node Math.007
		math_007 = node_tree.nodes.new("ShaderNodeMath")
		math_007.name = "Math.007"
		math_007.operation = 'MULTIPLY'
		math_007.use_clamp = False
		#Value_001
		math_007.inputs[1].default_value = 1.0

		#node Math.008
		math_008 = node_tree.nodes.new("ShaderNodeMath")
		math_008.name = "Math.008"
		math_008.operation = 'MULTIPLY'
		math_008.use_clamp = False
		#Value_001
		math_008.inputs[1].default_value = 1.0

		#node Math.017
		math_017 = node_tree.nodes.new("ShaderNodeMath")
		math_017.name = "Math.017"
		math_017.operation = 'SINE'
		math_017.use_clamp = False

		#node Noise Texture.003
		noise_texture_003 = node_tree.nodes.new("ShaderNodeTexNoise")
		noise_texture_003.name = "Noise Texture.003"
		noise_texture_003.noise_dimensions = '1D'
		noise_texture_003.noise_type = 'FBM'
		noise_texture_003.normalize = False
		#Detail
		noise_texture_003.inputs[3].default_value = 2.0
		#Roughness
		noise_texture_003.inputs[4].default_value = 0.0
		#Lacunarity
		noise_texture_003.inputs[5].default_value = 0.0
		#Distortion
		noise_texture_003.inputs[8].default_value = 0.0

		#node Mix.011
		mix_011 = node_tree.nodes.new("ShaderNodeMix")
		mix_011.name = "Mix.011"
		mix_011.blend_type = 'MIX'
		mix_011.clamp_factor = True
		mix_011.clamp_result = False
		mix_011.data_type = 'FLOAT'
		mix_011.factor_mode = 'UNIFORM'
		#A_Float
		mix_011.inputs[2].default_value = 0.0

		#node Math.010
		math_010 = node_tree.nodes.new("ShaderNodeMath")
		math_010.name = "Math.010"
		math_010.operation = 'MULTIPLY'
		math_010.use_clamp = False

		#node Mix
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix"
		mix.blend_type = 'COLOR'
		mix.clamp_factor = True
		mix.clamp_result = False
		mix.data_type = 'RGBA'
		mix.factor_mode = 'UNIFORM'

		#node Math.019
		math_019 = node_tree.nodes.new("ShaderNodeMath")
		math_019.name = "Math.019"
		math_019.operation = 'ADD'
		math_019.use_clamp = False

		#node Math.022
		math_022 = node_tree.nodes.new("ShaderNodeMath")
		math_022.name = "Math.022"
		math_022.operation = 'ADD'
		math_022.use_clamp = False

		#node Math.023
		math_023 = node_tree.nodes.new("ShaderNodeMath")
		math_023.name = "Math.023"
		math_023.operation = 'ADD'
		math_023.use_clamp = False

		#node Math.024
		math_024 = node_tree.nodes.new("ShaderNodeMath")
		math_024.name = "Math.024"
		math_024.operation = 'ADD'
		math_024.use_clamp = False

		#initialize node_tree links
		#math_022.Value -> noise_texture.W
		node_tree.links.new(math_022.outputs[0], noise_texture.inputs[1])
		#math_002.Value -> mix_007.B
		node_tree.links.new(math_002.outputs[0], mix_007.inputs[3])
		#group_input.Light -> mix_007.Factor
		node_tree.links.new(group_input.outputs[2], mix_007.inputs[0])
		#group_input.Speed -> noise_texture.Scale
		node_tree.links.new(group_input.outputs[9], noise_texture.inputs[2])
		#math_001.Value -> exposure.Exposure
		node_tree.links.new(math_001.outputs[0], exposure.inputs[1])
		#math_016.Value -> math_002.Value
		node_tree.links.new(math_016.outputs[0], math_002.inputs[0])
		#group_input.Amount -> math_002.Value
		node_tree.links.new(group_input.outputs[10], math_002.inputs[1])
		#scene_time.Seconds -> reroute.Input
		node_tree.links.new(scene_time.outputs[0], reroute.inputs[0])
		#math_003.Value -> mix_008.B
		node_tree.links.new(math_003.outputs[0], mix_008.inputs[3])
		#math_018.Value -> math_003.Value
		node_tree.links.new(math_018.outputs[0], math_003.inputs[0])
		#group_input.Blur -> mix_008.Factor
		node_tree.links.new(group_input.outputs[3], mix_008.inputs[0])
		#group_input.Speed -> noise_texture_001.Scale
		node_tree.links.new(group_input.outputs[12], noise_texture_001.inputs[2])
		#math_023.Value -> noise_texture_001.W
		node_tree.links.new(math_023.outputs[0], noise_texture_001.inputs[1])
		#group_input.Amount -> math_003.Value
		node_tree.links.new(group_input.outputs[13], math_003.inputs[1])
		#mix_008.Result -> blur.Size
		node_tree.links.new(mix_008.outputs[0], blur.inputs[1])
		#mix_007.Result -> math_001.Value
		node_tree.links.new(mix_007.outputs[0], math_001.inputs[0])
		#translate.Image -> vector_blur.Image
		node_tree.links.new(translate.outputs[0], vector_blur.inputs[0])
		#vector_blur.Image -> group_output.Image
		node_tree.links.new(vector_blur.outputs[0], group_output.inputs[0])
		#math_004.Value -> mix_009.B
		node_tree.links.new(math_004.outputs[0], mix_009.inputs[3])
		#math_020.Value -> math_004.Value
		node_tree.links.new(math_020.outputs[0], math_004.inputs[0])
		#math_024.Value -> noise_texture_002.W
		node_tree.links.new(math_024.outputs[0], noise_texture_002.inputs[1])
		#group_input.Slide -> mix_009.Factor
		node_tree.links.new(group_input.outputs[4], mix_009.inputs[0])
		#group_input.Speed -> noise_texture_002.Scale
		node_tree.links.new(group_input.outputs[15], noise_texture_002.inputs[2])
		#noise_texture_002.Fac -> math_020.Value
		node_tree.links.new(noise_texture_002.outputs[0], math_020.inputs[0])
		#noise_texture_001.Fac -> math_018.Value
		node_tree.links.new(noise_texture_001.outputs[0], math_018.inputs[0])
		#noise_texture.Fac -> math_016.Value
		node_tree.links.new(noise_texture.outputs[0], math_016.inputs[0])
		#math_005.Value -> math_004.Value
		node_tree.links.new(math_005.outputs[0], math_004.inputs[1])
		#group_input.Slide -> mix_010.Factor
		node_tree.links.new(group_input.outputs[4], mix_010.inputs[0])
		#mix_009.Result -> translate.X
		node_tree.links.new(mix_009.outputs[0], translate.inputs[1])
		#mix_010.Result -> translate.Y
		node_tree.links.new(mix_010.outputs[0], translate.inputs[2])
		#group_input.Amount -> math_005.Value
		node_tree.links.new(group_input.outputs[16], math_005.inputs[0])
		#combine_xyz.Vector -> vector_blur.Speed
		node_tree.links.new(combine_xyz.outputs[0], vector_blur.inputs[2])
		#math_007.Value -> combine_xyz.X
		node_tree.links.new(math_007.outputs[0], combine_xyz.inputs[0])
		#math_008.Value -> combine_xyz.Y
		node_tree.links.new(math_008.outputs[0], combine_xyz.inputs[1])
		#group_input.Shutter -> vector_blur.Shutter
		node_tree.links.new(group_input.outputs[18], vector_blur.inputs[4])
		#noise_texture_002.Fac -> math.Value
		node_tree.links.new(noise_texture_002.outputs[0], math.inputs[0])
		#math.Value -> math_021.Value
		node_tree.links.new(math.outputs[0], math_021.inputs[0])
		#math_006.Value -> mix_010.B
		node_tree.links.new(math_006.outputs[0], mix_010.inputs[3])
		#math_021.Value -> math_006.Value
		node_tree.links.new(math_021.outputs[0], math_006.inputs[0])
		#math_005.Value -> math_006.Value
		node_tree.links.new(math_005.outputs[0], math_006.inputs[1])
		#reroute.Output -> math.Value
		node_tree.links.new(reroute.outputs[0], math.inputs[1])
		#mix_009.Result -> math_007.Value
		node_tree.links.new(mix_009.outputs[0], math_007.inputs[0])
		#mix_010.Result -> math_008.Value
		node_tree.links.new(mix_010.outputs[0], math_008.inputs[0])
		#exposure.Image -> translate.Image
		node_tree.links.new(exposure.outputs[0], translate.inputs[0])
		#mix.Result -> blur.Image
		node_tree.links.new(mix.outputs[2], blur.inputs[0])
		#blur.Image -> exposure.Image
		node_tree.links.new(blur.outputs[0], exposure.inputs[0])
		#math_010.Value -> mix_011.B
		node_tree.links.new(math_010.outputs[0], mix_011.inputs[3])
		#math_017.Value -> math_010.Value
		node_tree.links.new(math_017.outputs[0], math_010.inputs[0])
		#noise_texture_003.Fac -> math_017.Value
		node_tree.links.new(noise_texture_003.outputs[0], math_017.inputs[0])
		#math_019.Value -> noise_texture_003.W
		node_tree.links.new(math_019.outputs[0], noise_texture_003.inputs[1])
		#group_input.Amount -> math_010.Value
		node_tree.links.new(group_input.outputs[6], math_010.inputs[1])
		#group_input.Speed -> noise_texture_003.Scale
		node_tree.links.new(group_input.outputs[5], noise_texture_003.inputs[2])
		#group_input.Color -> mix_011.Factor
		node_tree.links.new(group_input.outputs[1], mix_011.inputs[0])
		#group_input.Image -> mix.A
		node_tree.links.new(group_input.outputs[0], mix.inputs[6])
		#mix_011.Result -> mix.Factor
		node_tree.links.new(mix_011.outputs[0], mix.inputs[0])
		#group_input.Color -> mix.B
		node_tree.links.new(group_input.outputs[8], mix.inputs[7])
		#reroute.Output -> math_019.Value
		node_tree.links.new(reroute.outputs[0], math_019.inputs[0])
		#reroute.Output -> math_022.Value
		node_tree.links.new(reroute.outputs[0], math_022.inputs[0])
		#reroute.Output -> math_023.Value
		node_tree.links.new(reroute.outputs[0], math_023.inputs[0])
		#reroute.Output -> math_024.Value
		node_tree.links.new(reroute.outputs[0], math_024.inputs[0])
		#group_input.Offset -> math_019.Value
		node_tree.links.new(group_input.outputs[7], math_019.inputs[1])
		#group_input.Offset -> math_022.Value
		node_tree.links.new(group_input.outputs[11], math_022.inputs[1])
		#group_input.Offset -> math_023.Value
		node_tree.links.new(group_input.outputs[14], math_023.inputs[1])
		#group_input.Offset -> math_024.Value
		node_tree.links.new(group_input.outputs[17], math_024.inputs[1])
		return node_tree
