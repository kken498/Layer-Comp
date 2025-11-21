import bpy
from ..node import *

class CompositorNodeWiggleTransfrom(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeWiggleTransfrom'
	bl_label='Wiggle Transfrom'
	bl_icon='CON_ROTLIKE'

	def init(self, context):
		self.getNodetree(context)
		self.inputs[2].default_value = 5
		self.inputs[3].default_value = 20

		self.inputs[5].default_value = 5
		self.inputs[6].default_value = 0.087266

		self.inputs[8].default_value = 5
		self.inputs[9].default_value = 1.1

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
		image_socket.default_value = (1, 1, 1, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1, 1, 1, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Socket Position
		position_socket = node_tree.interface.new_socket(name = "Position", in_out='INPUT', socket_type = 'NodeSocketBool')
		position_socket.default_value = False
		position_socket.attribute_domain = 'POINT'
		position_socket.default_input = 'VALUE'
		position_socket.structure_type = 'AUTO'

		#Socket Speed
		speed_socket = node_tree.interface.new_socket(name = "Speed", in_out='INPUT', socket_type = 'NodeSocketFloat')
		speed_socket.default_value = 5.0
		speed_socket.min_value = -1000.0
		speed_socket.max_value = 1000.0
		speed_socket.subtype = 'NONE'
		speed_socket.attribute_domain = 'POINT'
		speed_socket.default_input = 'VALUE'
		speed_socket.structure_type = 'AUTO'

		#Socket Amount
		amount_socket = node_tree.interface.new_socket(name = "Amount", in_out='INPUT', socket_type = 'NodeSocketFloat')
		amount_socket.default_value = 20.0
		amount_socket.min_value = -10000.0
		amount_socket.max_value = 10000.0
		amount_socket.subtype = 'NONE'
		amount_socket.attribute_domain = 'POINT'
		amount_socket.default_input = 'VALUE'
		amount_socket.structure_type = 'AUTO'

		#Socket Rotation
		rotation_socket = node_tree.interface.new_socket(name = "Rotation", in_out='INPUT', socket_type = 'NodeSocketBool')
		rotation_socket.default_value = False
		rotation_socket.attribute_domain = 'POINT'
		rotation_socket.default_input = 'VALUE'
		rotation_socket.structure_type = 'AUTO'

		#Socket Speed
		speed_socket_1 = node_tree.interface.new_socket(name = "Speed", in_out='INPUT', socket_type = 'NodeSocketFloat')
		speed_socket_1.default_value = 5.0
		speed_socket_1.min_value = -1000.0
		speed_socket_1.max_value = 1000.0
		speed_socket_1.subtype = 'NONE'
		speed_socket_1.attribute_domain = 'POINT'
		speed_socket_1.default_input = 'VALUE'
		speed_socket_1.structure_type = 'AUTO'

		#Socket Amount
		amount_socket_1 = node_tree.interface.new_socket(name = "Amount", in_out='INPUT', socket_type = 'NodeSocketFloat')
		amount_socket_1.default_value = 0.08726644515991211
		amount_socket_1.min_value = -10000.0
		amount_socket_1.max_value = 10000.0
		amount_socket_1.subtype = 'ANGLE'
		amount_socket_1.attribute_domain = 'POINT'
		amount_socket_1.default_input = 'VALUE'
		amount_socket_1.structure_type = 'AUTO'

		#Socket Scale
		scale_socket = node_tree.interface.new_socket(name = "Scale", in_out='INPUT', socket_type = 'NodeSocketBool')
		scale_socket.default_value = False
		scale_socket.attribute_domain = 'POINT'
		scale_socket.default_input = 'VALUE'
		scale_socket.structure_type = 'AUTO'

		#Socket Speed
		speed_socket_2 = node_tree.interface.new_socket(name = "Speed", in_out='INPUT', socket_type = 'NodeSocketFloat')
		speed_socket_2.default_value = 5.0
		speed_socket_2.min_value = -1000.0
		speed_socket_2.max_value = 1000.0
		speed_socket_2.subtype = 'NONE'
		speed_socket_2.attribute_domain = 'POINT'
		speed_socket_2.default_input = 'VALUE'
		speed_socket_2.structure_type = 'AUTO'

		#Socket Amount
		amount_socket_2 = node_tree.interface.new_socket(name = "Amount", in_out='INPUT', socket_type = 'NodeSocketFloat')
		amount_socket_2.default_value = 1.1
		amount_socket_2.min_value = -10000.0
		amount_socket_2.max_value = 10000.0
		amount_socket_2.subtype = 'NONE'
		amount_socket_2.attribute_domain = 'POINT'
		amount_socket_2.default_input = 'VALUE'
		amount_socket_2.structure_type = 'AUTO'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Transform
		transform = node_tree.nodes.new("CompositorNodeTransform")
		transform.name = "Transform"
		transform.filter_type = 'NEAREST'

		#node Scene Time
		scene_time = node_tree.nodes.new("CompositorNodeSceneTime")
		scene_time.name = "Scene Time"

		#node Math.016
		math_016 = node_tree.nodes.new("ShaderNodeMath")
		math_016.name = "Math.016"
		math_016.operation = 'SINE'
		math_016.use_clamp = False

		#node Math.017
		math_017 = node_tree.nodes.new("ShaderNodeMath")
		math_017.name = "Math.017"
		math_017.operation = 'MULTIPLY_ADD'
		math_017.use_clamp = False

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
		noise_texture.inputs[5].default_value = 2.0
		#Distortion
		noise_texture.inputs[8].default_value = 0.0

		#node Math.019
		math_019 = node_tree.nodes.new("ShaderNodeMath")
		math_019.name = "Math.019"
		math_019.operation = 'MULTIPLY'
		math_019.use_clamp = False

		#node Math.020
		math_020 = node_tree.nodes.new("ShaderNodeMath")
		math_020.name = "Math.020"
		math_020.operation = 'MULTIPLY_ADD'
		math_020.use_clamp = False
		#Value_002
		math_020.inputs[2].default_value = 1.0

		#node Math.021
		math_021 = node_tree.nodes.new("ShaderNodeMath")
		math_021.name = "Math.021"
		math_021.operation = 'MULTIPLY_ADD'
		math_021.use_clamp = False
		#Value_002
		math_021.inputs[2].default_value = 25.0

		#node Math.022
		math_022 = node_tree.nodes.new("ShaderNodeMath")
		math_022.name = "Math.022"
		math_022.operation = 'SINE'
		math_022.use_clamp = False

		#node Math.023
		math_023 = node_tree.nodes.new("ShaderNodeMath")
		math_023.name = "Math.023"
		math_023.operation = 'MULTIPLY'
		math_023.use_clamp = False

		#node Math.024
		math_024 = node_tree.nodes.new("ShaderNodeMath")
		math_024.name = "Math.024"
		math_024.operation = 'MULTIPLY_ADD'
		math_024.use_clamp = False

		#node Math.025
		math_025 = node_tree.nodes.new("ShaderNodeMath")
		math_025.name = "Math.025"
		math_025.operation = 'SINE'
		math_025.use_clamp = False

		#node Math.018
		math_018 = node_tree.nodes.new("ShaderNodeMath")
		math_018.name = "Math.018"
		math_018.operation = 'SINE'
		math_018.use_clamp = False

		#node Math.026
		math_026 = node_tree.nodes.new("ShaderNodeMath")
		math_026.name = "Math.026"
		math_026.operation = 'MULTIPLY'
		math_026.use_clamp = False

		#node Math.027
		math_027 = node_tree.nodes.new("ShaderNodeMath")
		math_027.name = "Math.027"
		math_027.operation = 'MULTIPLY'
		math_027.use_clamp = False

		#node Mix.004
		mix_004 = node_tree.nodes.new("ShaderNodeMix")
		mix_004.name = "Mix.004"
		mix_004.blend_type = 'MIX'
		mix_004.clamp_factor = True
		mix_004.clamp_result = False
		mix_004.data_type = 'FLOAT'
		mix_004.factor_mode = 'UNIFORM'
		#A_Float
		mix_004.inputs[2].default_value = 0.0

		#node Mix.005
		mix_005 = node_tree.nodes.new("ShaderNodeMix")
		mix_005.name = "Mix.005"
		mix_005.blend_type = 'MIX'
		mix_005.clamp_factor = True
		mix_005.clamp_result = False
		mix_005.data_type = 'FLOAT'
		mix_005.factor_mode = 'UNIFORM'
		#A_Float
		mix_005.inputs[2].default_value = 0.0

		#node Mix.006
		mix_006 = node_tree.nodes.new("ShaderNodeMix")
		mix_006.name = "Mix.006"
		mix_006.blend_type = 'MIX'
		mix_006.clamp_factor = True
		mix_006.clamp_result = False
		mix_006.data_type = 'FLOAT'
		mix_006.factor_mode = 'UNIFORM'
		#A_Float
		mix_006.inputs[2].default_value = 0.0

		#node Mix.007
		mix_007 = node_tree.nodes.new("ShaderNodeMix")
		mix_007.name = "Mix.007"
		mix_007.blend_type = 'MIX'
		mix_007.clamp_factor = True
		mix_007.clamp_result = False
		mix_007.data_type = 'FLOAT'
		mix_007.factor_mode = 'UNIFORM'
		#A_Float
		mix_007.inputs[2].default_value = 1.0

		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = False
		#Value_001
		math.inputs[1].default_value = 0.1

		#node Math.028
		math_028 = node_tree.nodes.new("ShaderNodeMath")
		math_028.name = "Math.028"
		math_028.operation = 'SUBTRACT'
		math_028.use_clamp = False
		#Value_001
		math_028.inputs[1].default_value = 1.0

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
		noise_texture_001.inputs[5].default_value = 2.0
		#Distortion
		noise_texture_001.inputs[8].default_value = 0.0

		#node Noise Texture.002
		noise_texture_002 = node_tree.nodes.new("ShaderNodeTexNoise")
		noise_texture_002.name = "Noise Texture.002"
		noise_texture_002.noise_dimensions = '1D'
		noise_texture_002.noise_type = 'FBM'
		noise_texture_002.normalize = False
		#Detail
		noise_texture_002.inputs[3].default_value = 2.0
		#Roughness
		noise_texture_002.inputs[4].default_value = 0.0
		#Lacunarity
		noise_texture_002.inputs[5].default_value = 2.0
		#Distortion
		noise_texture_002.inputs[8].default_value = 0.0

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'MULTIPLY'
		math_001.use_clamp = False
		#Value_001
		math_001.inputs[1].default_value = 0.1

		#node Math.002
		math_002 = node_tree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MULTIPLY'
		math_002.use_clamp = False
		#Value_001
		math_002.inputs[1].default_value = 0.1

		#initialize node_tree links
		#math_023.Value -> mix_005.B
		node_tree.links.new(math_023.outputs[0], mix_005.inputs[3])
		#math_025.Value -> math_023.Value
		node_tree.links.new(math_025.outputs[0], math_023.inputs[0])
		#scene_time.Seconds -> noise_texture.W
		node_tree.links.new(scene_time.outputs[0], noise_texture.inputs[1])
		#mix_005.Result -> transform.Y
		node_tree.links.new(mix_005.outputs[0], transform.inputs[2])
		#scene_time.Seconds -> math_026.Value
		node_tree.links.new(scene_time.outputs[0], math_026.inputs[0])
		#scene_time.Seconds -> math_024.Value
		node_tree.links.new(scene_time.outputs[0], math_024.inputs[0])
		#mix_007.Result -> transform.Scale
		node_tree.links.new(mix_007.outputs[0], transform.inputs[4])
		#scene_time.Seconds -> math_024.Value
		node_tree.links.new(scene_time.outputs[0], math_024.inputs[2])
		#math_017.Value -> math_016.Value
		node_tree.links.new(math_017.outputs[0], math_016.inputs[0])
		#math_027.Value -> mix_006.B
		node_tree.links.new(math_027.outputs[0], mix_006.inputs[3])
		#scene_time.Seconds -> math_017.Value
		node_tree.links.new(scene_time.outputs[0], math_017.inputs[0])
		#math_019.Value -> mix_004.B
		node_tree.links.new(math_019.outputs[0], mix_004.inputs[3])
		#mix_006.Result -> transform.Angle
		node_tree.links.new(mix_006.outputs[0], transform.inputs[3])
		#math_020.Value -> mix_007.B
		node_tree.links.new(math_020.outputs[0], mix_007.inputs[3])
		#mix_004.Result -> transform.X
		node_tree.links.new(mix_004.outputs[0], transform.inputs[1])
		#math_021.Value -> math_022.Value
		node_tree.links.new(math_021.outputs[0], math_022.inputs[0])
		#math_026.Value -> math_018.Value
		node_tree.links.new(math_026.outputs[0], math_018.inputs[0])
		#math_016.Value -> math_020.Value
		node_tree.links.new(math_016.outputs[0], math_020.inputs[0])
		#math_022.Value -> math_019.Value
		node_tree.links.new(math_022.outputs[0], math_019.inputs[0])
		#math_024.Value -> math_025.Value
		node_tree.links.new(math_024.outputs[0], math_025.inputs[0])
		#noise_texture.Fac -> math_017.Value
		node_tree.links.new(noise_texture.outputs[0], math_017.inputs[1])
		#scene_time.Seconds -> math_017.Value
		node_tree.links.new(scene_time.outputs[0], math_017.inputs[2])
		#scene_time.Seconds -> math_021.Value
		node_tree.links.new(scene_time.outputs[0], math_021.inputs[0])
		#group_input.Image -> transform.Image
		node_tree.links.new(group_input.outputs[0], transform.inputs[0])
		#transform.Image -> group_output.Image
		node_tree.links.new(transform.outputs[0], group_output.inputs[0])
		#group_input.Position -> mix_004.Factor
		node_tree.links.new(group_input.outputs[1], mix_004.inputs[0])
		#group_input.Position -> mix_005.Factor
		node_tree.links.new(group_input.outputs[1], mix_005.inputs[0])
		#group_input.Rotation -> mix_006.Factor
		node_tree.links.new(group_input.outputs[4], mix_006.inputs[0])
		#group_input.Scale -> mix_007.Factor
		node_tree.links.new(group_input.outputs[7], mix_007.inputs[0])
		#math.Value -> noise_texture.Scale
		node_tree.links.new(math.outputs[0], noise_texture.inputs[2])
		#group_input.Amount -> math_023.Value
		node_tree.links.new(group_input.outputs[3], math_023.inputs[1])
		#group_input.Amount -> math_019.Value
		node_tree.links.new(group_input.outputs[3], math_019.inputs[1])
		#math_018.Value -> math_027.Value
		node_tree.links.new(math_018.outputs[0], math_027.inputs[0])
		#group_input.Amount -> math_027.Value
		node_tree.links.new(group_input.outputs[6], math_027.inputs[1])
		#math_028.Value -> math_020.Value
		node_tree.links.new(math_028.outputs[0], math_020.inputs[1])
		#group_input.Amount -> math_028.Value
		node_tree.links.new(group_input.outputs[9], math_028.inputs[0])
		#scene_time.Seconds -> noise_texture_001.W
		node_tree.links.new(scene_time.outputs[0], noise_texture_001.inputs[1])
		#noise_texture_001.Fac -> math_026.Value
		node_tree.links.new(noise_texture_001.outputs[0], math_026.inputs[1])
		#noise_texture_002.Fac -> math_024.Value
		node_tree.links.new(noise_texture_002.outputs[0], math_024.inputs[1])
		#noise_texture_002.Fac -> math_021.Value
		node_tree.links.new(noise_texture_002.outputs[0], math_021.inputs[1])
		#scene_time.Seconds -> noise_texture_002.W
		node_tree.links.new(scene_time.outputs[0], noise_texture_002.inputs[1])
		#group_input.Speed -> math.Value
		node_tree.links.new(group_input.outputs[8], math.inputs[0])
		#group_input.Speed -> math_001.Value
		node_tree.links.new(group_input.outputs[5], math_001.inputs[0])
		#math_001.Value -> noise_texture_001.Scale
		node_tree.links.new(math_001.outputs[0], noise_texture_001.inputs[2])
		#group_input.Speed -> math_002.Value
		node_tree.links.new(group_input.outputs[2], math_002.inputs[0])
		#math_002.Value -> noise_texture_002.Scale
		node_tree.links.new(math_002.outputs[0], noise_texture_002.inputs[2])
		return node_tree
