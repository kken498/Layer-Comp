import bpy
from ..node import *

class CompositorNodeOuterGlow(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeOuterGlow'
	bl_label='Outer Glow'
	bl_icon='LIGHT_SUN'
	
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
		self.falloff = 'SMOOTH'
		self.inputs[1].default_value = (1.000000, 0.996410, 0.763167, 1.000000)
		self.inputs["Size"].default_value = 35
		self.inputs[5].default_value = 1
		
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
		image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'

		#Socket Outer
		outer_socket = node_tree.interface.new_socket(name = "Outer", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		outer_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		outer_socket.attribute_domain = 'POINT'
		outer_socket.default_input = 'VALUE'
		outer_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'
		image_socket_1.hide_value = True

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (1.000000, 0.996410, 0.763167, 1.000000)
		color_socket.attribute_domain = 'POINT'
		color_socket.default_input = 'VALUE'
		color_socket.structure_type = 'AUTO'

		#Socket Size
		size_socket = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketInt')
		size_socket.default_value = 35
		size_socket.min_value = 0
		size_socket.max_value = 2147483647
		size_socket.subtype = 'NONE'
		size_socket.attribute_domain = 'POINT'
		size_socket.default_input = 'VALUE'
		size_socket.structure_type = 'AUTO'

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
		color_socket_1 = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
		color_socket_1.attribute_domain = 'POINT'
		color_socket_1.default_input = 'VALUE'
		color_socket_1.structure_type = 'AUTO'

		#Socket Opacity
		opacity_socket = node_tree.interface.new_socket(name = "Opacity", in_out='INPUT', socket_type = 'NodeSocketFloat')
		opacity_socket.default_value = 1.0
		opacity_socket.min_value = 0.0
		opacity_socket.max_value = 1.0
		opacity_socket.subtype = 'FACTOR'
		opacity_socket.attribute_domain = 'POINT'
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

		#node Alpha Over.002
		alpha_over_002 = node_tree.nodes.new("CompositorNodeAlphaOver")
		alpha_over_002.name = "Alpha Over.002"
		#Fac
		alpha_over_002.inputs[0].default_value = 1.0
		#Straight Alpha
		alpha_over_002.inputs[3].default_value = False

		#node Set Alpha
		set_alpha = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha.name = "Set Alpha"
		set_alpha.mode = 'APPLY'

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#node Dilate/Erode
		dilate_erode = node_tree.nodes.new("CompositorNodeDilateErode")
		dilate_erode.name = "Dilate/Erode"
		dilate_erode.falloff = 'SMOOTH'
		dilate_erode.mode = 'FEATHER'

		#node Set Alpha.001
		set_alpha_001 = node_tree.nodes.new("CompositorNodeSetAlpha")
		set_alpha_001.name = "Set Alpha.001"
		set_alpha_001.mode = 'APPLY'

		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'SUBTRACT'
		math.use_clamp = False
		#Value
		math.inputs[0].default_value = 1.0

		#node Mix
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.clamp_factor = True
		mix.clamp_result = False
		mix.data_type = 'FLOAT'
		mix.factor_mode = 'UNIFORM'
		#A_Float
		mix.inputs[2].default_value = 0.0

		#node Mix.001
		mix_001 = node_tree.nodes.new("ShaderNodeMix")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.clamp_factor = True
		mix_001.clamp_result = False
		mix_001.data_type = 'RGBA'
		mix_001.factor_mode = 'UNIFORM'

		#initialize node_tree links
		#mix_001.Result -> alpha_over_002.Image
		node_tree.links.new(mix_001.outputs[2], alpha_over_002.inputs[2])
		#alpha_over_002.Image -> group_output.Image
		node_tree.links.new(alpha_over_002.outputs[0], group_output.inputs[0])
		#group_input.Color -> set_alpha.Image
		node_tree.links.new(group_input.outputs[1], set_alpha.inputs[0])
		#set_alpha.Image -> alpha_over_002.Image
		node_tree.links.new(set_alpha.outputs[0], alpha_over_002.inputs[1])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#dilate_erode.Mask -> set_alpha.Alpha
		node_tree.links.new(dilate_erode.outputs[0], set_alpha.inputs[1])
		#mix.Result -> dilate_erode.Mask
		node_tree.links.new(mix.outputs[0], dilate_erode.inputs[0])
		#group_input.Size -> dilate_erode.Size
		node_tree.links.new(group_input.outputs[2], dilate_erode.inputs[1])
		#set_alpha.Image -> set_alpha_001.Image
		node_tree.links.new(set_alpha.outputs[0], set_alpha_001.inputs[0])
		#math.Value -> set_alpha_001.Alpha
		node_tree.links.new(math.outputs[0], set_alpha_001.inputs[1])
		#set_alpha_001.Image -> group_output.Outer
		node_tree.links.new(set_alpha_001.outputs[0], group_output.inputs[1])
		#separate_color.Alpha -> math.Value
		node_tree.links.new(separate_color.outputs[3], math.inputs[1])
		#separate_color.Alpha -> mix.B
		node_tree.links.new(separate_color.outputs[3], mix.inputs[3])
		#group_input.Opacity -> mix.Factor
		node_tree.links.new(group_input.outputs[5], mix.inputs[0])
		#group_input.Image -> mix_001.A
		node_tree.links.new(group_input.outputs[0], mix_001.inputs[6])
		#group_input.Fill -> mix_001.Factor
		node_tree.links.new(group_input.outputs[3], mix_001.inputs[0])
		#group_input.Color -> mix_001.B
		node_tree.links.new(group_input.outputs[4], mix_001.inputs[7])
		return node_tree
