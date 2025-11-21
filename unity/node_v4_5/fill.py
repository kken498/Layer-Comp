import bpy
from ..node import *

class CompositorNodeFill(bpy.types.CompositorNodeCustomGroup, Node, Mix_Node):
	bl_name='CompositorNodeFill'
	bl_label='Fill'
	bl_icon='SNAP_FACE'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Fill"].default_value = (1.0, 0.0, 0.0, 1.0)
		self.inputs["Strength"].default_value = 1

	def draw_buttons(self, context, layout):
		layout.prop(self, 'blend_type', text='')

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
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

		#Socket Fill
		fill_socket = node_tree.interface.new_socket(name = "Fill", in_out='INPUT', socket_type = 'NodeSocketColor')
		fill_socket.default_value = (1.0, 0.01140127144753933, 0.01140127144753933, 1.0)
		fill_socket.attribute_domain = 'POINT'
		fill_socket.default_input = 'VALUE'
		fill_socket.structure_type = 'AUTO'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 1.0
		strength_socket.subtype = 'FACTOR'
		strength_socket.attribute_domain = 'POINT'
		strength_socket.description = "Amount of mixing between the A and B inputs"
		strength_socket.default_input = 'VALUE'
		strength_socket.structure_type = 'AUTO'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Mix
		mix_004 = node_tree.nodes.new("ShaderNodeMix")
		mix_004.name = "Mix"
		mix_004.blend_type = 'MIX'
		mix_004.clamp_factor = True
		mix_004.clamp_result = False
		mix_004.data_type = 'RGBA'
		mix_004.factor_mode = 'UNIFORM'

		#node Separate Color.001
		separate_color_001 = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color_001.name = "Separate Color.001"
		separate_color_001.mode = 'RGB'
		separate_color_001.ycc_mode = 'ITUBT709'

		#node Mix.004
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix.004"
		mix.blend_type = 'MIX'
		mix.clamp_factor = True
		mix.clamp_result = False
		mix.data_type = 'FLOAT'
		mix.factor_mode = 'UNIFORM'
		#A_Float
		mix.inputs[2].default_value = 0.0

		#initialize node_tree links
		#mix_004.Result -> group_output.Result
		node_tree.links.new(mix_004.outputs[2], group_output.inputs[0])
		#group_input.Image -> separate_color_001.Image
		node_tree.links.new(group_input.outputs[0], separate_color_001.inputs[0])
		#group_input.Fill -> mix_004.B
		node_tree.links.new(group_input.outputs[1], mix_004.inputs[7])
		#mix.Result -> mix_004.Factor
		node_tree.links.new(mix.outputs[0], mix_004.inputs[0])
		#separate_color_001.Alpha -> mix.B
		node_tree.links.new(separate_color_001.outputs[3], mix.inputs[3])
		#group_input.Strength -> mix.Factor
		node_tree.links.new(group_input.outputs[2], mix.inputs[0])
		#group_input.Image -> mix_004.A
		node_tree.links.new(group_input.outputs[0], mix_004.inputs[6])
		return node_tree

class CompositorNodeSpotFill(bpy.types.CompositorNodeCustomGroup, Node, Mix_Node):
	bl_name='CompositorNodeSpotFill'
	bl_label='Spot Fill'
	bl_icon='SURFACE_NCIRCLE'

	def init(self, context):
		self.getNodetree(context)
		self.blend_type = 'MIX'
		self.inputs["Fill"].default_value = (1.0, 0.0, 0.0, 1.0)
		self.inputs["Position"].default_value[0] = 0.5
		self.inputs["Position"].default_value[1] = 0.5
		self.inputs["Size"].default_value[0] = 0.5
		self.inputs["Size"].default_value[1] = 0.5
		self.inputs["Falloff"].default_value = 3.5
		self.inputs["Strength"].default_value = 1

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

		#Socket Fill
		fill_socket = node_tree.interface.new_socket(name = "Fill", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		fill_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		fill_socket.attribute_domain = 'POINT'
		fill_socket.default_input = 'VALUE'
		fill_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True
		image_socket_1.description = "Value of the first color input"
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Socket Fill
		fill_socket_1 = node_tree.interface.new_socket(name = "Fill", in_out='INPUT', socket_type = 'NodeSocketColor')
		fill_socket_1.default_value = (1.0, 0.0, 0.0, 1.0)
		fill_socket_1.attribute_domain = 'POINT'
		fill_socket_1.description = "Value of the first color input"
		fill_socket_1.default_input = 'VALUE'
		fill_socket_1.structure_type = 'AUTO'

		#Socket Position
		position_socket = node_tree.interface.new_socket(name = "Position", in_out='INPUT', socket_type = 'NodeSocketVector')
		position_socket.default_value = (0.5, 0.5, 0.0)
		position_socket.min_value = -0.5
		position_socket.max_value = 1.5
		position_socket.subtype = 'FACTOR'
		position_socket.attribute_domain = 'POINT'
		position_socket.default_input = 'VALUE'
		position_socket.structure_type = 'AUTO'
		position_socket.dimensions = 2

		#Socket Size
		size_socket = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketVector')
		size_socket.default_value = (0.5, 0.5, 0.0)
		size_socket.min_value = 0.0
		size_socket.max_value = 1.0
		size_socket.subtype = 'FACTOR'
		size_socket.attribute_domain = 'POINT'
		size_socket.default_input = 'VALUE'
		size_socket.structure_type = 'AUTO'
		size_socket.dimensions = 2
		
		#Socket Falloff
		falloff_socket = node_tree.interface.new_socket(name = "Falloff", in_out='INPUT', socket_type = 'NodeSocketFloat')
		falloff_socket.default_value = 3.5
		falloff_socket.min_value = 0.0
		falloff_socket.max_value = 10.0
		falloff_socket.subtype = 'FACTOR'
		falloff_socket.attribute_domain = 'POINT'
		falloff_socket.default_input = 'VALUE'
		falloff_socket.structure_type = 'AUTO'

		#Socket Invert Color
		invert_color_socket = node_tree.interface.new_socket(name = "Invert Color", in_out='INPUT', socket_type = 'NodeSocketBool')
		invert_color_socket.default_value = False
		invert_color_socket.attribute_domain = 'POINT'
		invert_color_socket.default_input = 'VALUE'
		invert_color_socket.structure_type = 'AUTO'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 1.0
		strength_socket.subtype = 'FACTOR'
		strength_socket.attribute_domain = 'POINT'
		strength_socket.description = "Amount of mixing between the A and B inputs"
		strength_socket.default_input = 'VALUE'
		strength_socket.structure_type = 'AUTO'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Ellipse Mask
		ellipse_mask = node_tree.nodes.new("CompositorNodeEllipseMask")
		ellipse_mask.name = "Ellipse Mask"
		ellipse_mask.mask_type = 'MULTIPLY'
		#Value
		ellipse_mask.inputs[1].default_value = 1.0
		#Rotation
		ellipse_mask.inputs[4].default_value = 0.0

		#node Blur
		blur = node_tree.nodes.new("CompositorNodeBlur")
		blur.name = "Blur"
		blur.filter_type = 'FAST_GAUSS'
		#Extend Bounds
		blur.inputs[2].default_value = False
		#Separable
		blur.inputs[3].default_value = True

		#node Combine XYZ
		combine_xyz = node_tree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz.name = "Combine XYZ"
		#Z
		combine_xyz.inputs[2].default_value = 0.0

		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = False
		#Value_001
		math.inputs[1].default_value = 0.550000011920929

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'MULTIPLY'
		math_001.use_clamp = False
		#Value_001
		math_001.inputs[1].default_value = 100.0

		#node Separate XYZ
		separate_xyz = node_tree.nodes.new("ShaderNodeSeparateXYZ")
		separate_xyz.name = "Separate XYZ"

		#node Mix
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.clamp_factor = True
		mix.clamp_result = False
		mix.data_type = 'RGBA'
		mix.factor_mode = 'UNIFORM'

		#node Mix.001
		mix_001 = node_tree.nodes.new("ShaderNodeMix")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.clamp_factor = True
		mix_001.clamp_result = False
		mix_001.data_type = 'RGBA'
		mix_001.factor_mode = 'UNIFORM'
		#A_Color
		mix_001.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)

		#node Invert Color
		invert_color = node_tree.nodes.new("CompositorNodeInvert")
		invert_color.name = "Invert Color"
		#Fac
		invert_color.inputs[0].default_value = 1.0
		#Invert Alpha
		invert_color.inputs[3].default_value = False

		#initialize node_tree links
		#ellipse_mask.Mask -> blur.Image
		node_tree.links.new(ellipse_mask.outputs[0], blur.inputs[0])
		#math.Value -> combine_xyz.Y
		node_tree.links.new(math.outputs[0], combine_xyz.inputs[1])
		#group_input.Position -> ellipse_mask.Position
		node_tree.links.new(group_input.outputs[2], ellipse_mask.inputs[2])
		#group_input.Falloff -> math_001.Value
		node_tree.links.new(group_input.outputs[4], math_001.inputs[0])
		#math_001.Value -> blur.Size
		node_tree.links.new(math_001.outputs[0], blur.inputs[1])
		#combine_xyz.Vector -> ellipse_mask.Size
		node_tree.links.new(combine_xyz.outputs[0], ellipse_mask.inputs[3])
		#group_input.Size -> separate_xyz.Vector
		node_tree.links.new(group_input.outputs[3], separate_xyz.inputs[0])
		#separate_xyz.X -> combine_xyz.X
		node_tree.links.new(separate_xyz.outputs[0], combine_xyz.inputs[0])
		#separate_xyz.Y -> math.Value
		node_tree.links.new(separate_xyz.outputs[1], math.inputs[0])
		#invert_color.Color -> mix.Factor
		node_tree.links.new(invert_color.outputs[0], mix.inputs[0])
		#mix.Result -> group_output.Image
		node_tree.links.new(mix.outputs[2], group_output.inputs[0])
		#mix_001.Result -> group_output.Fill
		node_tree.links.new(mix_001.outputs[2], group_output.inputs[1])
		#group_input.Image -> mix.A
		node_tree.links.new(group_input.outputs[0], mix.inputs[6])
		#group_input.Fill -> mix.B
		node_tree.links.new(group_input.outputs[1], mix.inputs[7])
		#blur.Image -> invert_color.Color
		node_tree.links.new(blur.outputs[0], invert_color.inputs[1])
		#group_input.Invert Color -> invert_color.Invert Color
		node_tree.links.new(group_input.outputs[5], invert_color.inputs[2])
		#group_input.Strength -> ellipse_mask.Mask
		node_tree.links.new(group_input.outputs[6], ellipse_mask.inputs[0])
		#invert_color.Color -> mix_001.Factor
		node_tree.links.new(invert_color.outputs[0], mix_001.inputs[0])
		#group_input.Fill -> mix_001.B
		node_tree.links.new(group_input.outputs[1], mix_001.inputs[7])
		return node_tree