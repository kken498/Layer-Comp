import bpy
from ..node import *

class CompositorNodeShutterStreak(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeShutterStreak'
	bl_label='Shutter Streak'
	bl_icon='CAMERA_STEREO'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Size"].default_value = 1
		self.inputs["Boost"].default_value = 1
		self.inputs["Falloff"].default_value = 1

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

		#Socket Streak
		streak_socket = node_tree.interface.new_socket(name = "Streak", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		streak_socket.default_value = (1, 1, 1, 1.0)
		streak_socket.attribute_domain = 'POINT'
		streak_socket.default_input = 'VALUE'
		streak_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Socket Size
		size_socket = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
		size_socket.default_value = 1.0
		size_socket.min_value = 0.0
		size_socket.max_value = 5.0
		size_socket.subtype = 'NONE'
		size_socket.attribute_domain = 'POINT'
		size_socket.description = "The brightness level at which pixels are considered part of the highlights that produce a glare"
		size_socket.default_input = 'VALUE'
		size_socket.structure_type = 'AUTO'

		#Socket Boost
		boost_socket = node_tree.interface.new_socket(name = "Boost", in_out='INPUT', socket_type = 'NodeSocketFloat')
		boost_socket.default_value = 1.0
		boost_socket.min_value = 0.0
		boost_socket.max_value = 10.0
		boost_socket.subtype = 'NONE'
		boost_socket.attribute_domain = 'POINT'
		boost_socket.description = "The brightness level at which pixels are considered part of the highlights that produce a glare"
		boost_socket.default_input = 'VALUE'
		boost_socket.structure_type = 'AUTO'

		#Socket Falloff
		falloff_socket = node_tree.interface.new_socket(name = "Falloff", in_out='INPUT', socket_type = 'NodeSocketFloat')
		falloff_socket.default_value = 1.0
		falloff_socket.min_value = 0.0
		falloff_socket.max_value = 1.0
		falloff_socket.subtype = 'FACTOR'
		falloff_socket.attribute_domain = 'POINT'
		falloff_socket.description = "The smoothness of the extracted highlights"
		falloff_socket.default_input = 'VALUE'
		falloff_socket.structure_type = 'AUTO'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Glare
		glare = node_tree.nodes.new("CompositorNodeGlare")
		glare.name = "Glare"
		glare.glare_type = 'STREAKS'
		glare.quality = 'LOW'
		#Clamp Highlights
		glare.inputs[3].default_value = False
		#Maximum Highlights
		glare.inputs[4].default_value = 10.0
		#Strength
		glare.inputs[5].default_value = 1.0
		#Saturation
		glare.inputs[6].default_value = 1.0
		#Tint
		glare.inputs[7].default_value = (1.0, 1.0, 1.0, 1.0)
		#Streaks
		glare.inputs[9].default_value = 2
		#Streaks Angle
		glare.inputs[10].default_value = 1.5707963705062866
		#Iterations
		glare.inputs[11].default_value = 4
		#Fade
		glare.inputs[12].default_value = 1.0
		#Color Modulation
		glare.inputs[13].default_value = 0.25

		#node Glare.001
		glare_001 = node_tree.nodes.new("CompositorNodeGlare")
		glare_001.name = "Glare.001"
		glare_001.glare_type = 'FOG_GLOW'
		glare_001.quality = 'MEDIUM'
		#Clamp Highlights
		glare_001.inputs[3].default_value = False
		#Maximum Highlights
		glare_001.inputs[4].default_value = 10.0
		#Strength
		glare_001.inputs[5].default_value = 1.0
		#Saturation
		glare_001.inputs[6].default_value = 0.0
		#Tint
		glare_001.inputs[7].default_value = (1.0, 1.0, 1.0, 1.0)
		#Size
		glare_001.inputs[8].default_value = 1.0

		#node Mix.004
		mix_004 = node_tree.nodes.new("ShaderNodeMix")
		mix_004.name = "Mix.004"
		mix_004.blend_type = 'MIX'
		mix_004.clamp_factor = True
		mix_004.clamp_result = False
		mix_004.data_type = 'RGBA'
		mix_004.factor_mode = 'UNIFORM'

		#node Color Ramp
		color_ramp = node_tree.nodes.new("ShaderNodeValToRGB")
		color_ramp.name = "Color Ramp"
		color_ramp.color_ramp.color_mode = 'RGB'
		color_ramp.color_ramp.hue_interpolation = 'NEAR'
		color_ramp.color_ramp.interpolation = 'B_SPLINE'

		#initialize color ramp elements
		color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
		color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
		color_ramp_cre_0.position = 0.0
		color_ramp_cre_0.alpha = 1.0
		color_ramp_cre_0.color = (1.0, 1.0, 1.0, 1.0)

		color_ramp_cre_1 = color_ramp.color_ramp.elements.new(0.38414642214775085)
		color_ramp_cre_1.alpha = 1.0
		color_ramp_cre_1.color = (0.0, 0.0, 0.0, 1.0)

		color_ramp_cre_2 = color_ramp.color_ramp.elements.new(0.8414634466171265)
		color_ramp_cre_2.alpha = 1.0
		color_ramp_cre_2.color = (0.000310726958559826, 0.000310726958559826, 0.000310726958559826, 1.0)


		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'SUBTRACT'
		math.use_clamp = False
		#Value
		math.inputs[0].default_value = 1.0

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'MULTIPLY'
		math_001.use_clamp = False
		#Value_001
		math_001.inputs[1].default_value = 0.25

		#node Math.002
		math_002 = node_tree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'MULTIPLY'
		math_002.use_clamp = False
		#Value_001
		math_002.inputs[1].default_value = 0.1

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

		#initialize node_tree links
		#glare_001.Glare -> color_ramp.Fac
		node_tree.links.new(glare_001.outputs[1], color_ramp.inputs[0])
		#color_ramp.Color -> mix_004.Factor
		node_tree.links.new(color_ramp.outputs[0], mix_004.inputs[0])
		#glare.Image -> mix_004.B
		node_tree.links.new(glare.outputs[0], mix_004.inputs[7])
		#group_input.Image -> glare.Image
		node_tree.links.new(group_input.outputs[0], glare.inputs[0])
		#group_input.Image -> glare_001.Image
		node_tree.links.new(group_input.outputs[0], glare_001.inputs[0])
		#group_input.Image -> mix_004.A
		node_tree.links.new(group_input.outputs[0], mix_004.inputs[6])
		#mix_004.Result -> group_output.Image
		node_tree.links.new(mix_004.outputs[2], group_output.inputs[0])
		#math.Value -> glare.Threshold
		node_tree.links.new(math.outputs[0], glare.inputs[1])
		#math_002.Value -> math.Value
		node_tree.links.new(math_002.outputs[0], math.inputs[1])
		#group_input.Size -> math_001.Value
		node_tree.links.new(group_input.outputs[1], math_001.inputs[0])
		#group_input.Boost -> math_002.Value
		node_tree.links.new(group_input.outputs[2], math_002.inputs[0])
		#math_001.Value -> glare_001.Threshold
		node_tree.links.new(math_001.outputs[0], glare_001.inputs[1])
		#group_input.Falloff -> glare.Smoothness
		node_tree.links.new(group_input.outputs[3], glare.inputs[2])
		#group_input.Falloff -> glare_001.Smoothness
		node_tree.links.new(group_input.outputs[3], glare_001.inputs[2])
		#glare.Glare -> mix_005.B
		node_tree.links.new(glare.outputs[1], mix_005.inputs[7])
		#color_ramp.Color -> mix_005.Factor
		node_tree.links.new(color_ramp.outputs[0], mix_005.inputs[0])
		#mix_005.Result -> group_output.Streak
		node_tree.links.new(mix_005.outputs[2], group_output.inputs[1])
		return node_tree
