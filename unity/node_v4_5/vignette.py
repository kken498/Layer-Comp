import bpy
from ..node import *

class CompositorNodeVignette(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeVignette'
	bl_label='Vignette'
	bl_icon='MOD_MASK'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Strength"].default_value = 1
		self.inputs["Position"].default_value[0] = 0.5
		self.inputs["Position"].default_value[1] = 0.5
		self.inputs["Size"].default_value[0] = 0.75
		self.inputs["Size"].default_value[1] = 0.75
		self.inputs["Falloff"].default_value = 2

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
		image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'
		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.description = "Value of the first color input"
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'
		image_socket_1.hide_value = True

		#Socket Color
		color_socket = node_tree.interface.new_socket(name = "Color", in_out='INPUT', socket_type = 'NodeSocketColor')
		color_socket.default_value = (0.0, 0.0, 0.0, 1.0)
		color_socket.attribute_domain = 'POINT'
		color_socket.description = "Value of the second color input"
		color_socket.default_input = 'VALUE'
		color_socket.structure_type = 'AUTO'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat')
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 1.0
		strength_socket.subtype = 'FACTOR'
		strength_socket.attribute_domain = 'POINT'
		strength_socket.default_input = 'VALUE'
		strength_socket.structure_type = 'AUTO'

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
		size_socket.default_value = (0.75, 0.75, 0.0)
		size_socket.min_value = 0.0
		size_socket.max_value = 1.0
		size_socket.subtype = 'FACTOR'
		size_socket.attribute_domain = 'POINT'
		size_socket.default_input = 'VALUE'
		size_socket.structure_type = 'AUTO'
		size_socket.dimensions = 2

		#Socket Falloff
		falloff_socket = node_tree.interface.new_socket(name = "Falloff", in_out='INPUT', socket_type = 'NodeSocketFloat')
		falloff_socket.default_value = 2.0
		falloff_socket.min_value = 0.0
		falloff_socket.max_value = 10.0
		falloff_socket.subtype = 'FACTOR'
		falloff_socket.attribute_domain = 'POINT'
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

		#node Mix
		mix = node_tree.nodes.new("ShaderNodeMix")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.clamp_factor = True
		mix.clamp_result = False
		mix.data_type = 'RGBA'
		mix.factor_mode = 'UNIFORM'

		#node Ellipse Mask
		ellipse_mask = node_tree.nodes.new("CompositorNodeEllipseMask")
		ellipse_mask.name = "Ellipse Mask"
		ellipse_mask.mask_type = 'SUBTRACT'
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

		#initialize node_tree links
		#ellipse_mask.Mask -> blur.Image
		node_tree.links.new(ellipse_mask.outputs[0], blur.inputs[0])
		#math.Value -> combine_xyz.Y
		node_tree.links.new(math.outputs[0], combine_xyz.inputs[1])
		#blur.Image -> mix.Factor
		node_tree.links.new(blur.outputs[0], mix.inputs[0])
		#group_input.Image -> mix.A
		node_tree.links.new(group_input.outputs[0], mix.inputs[6])
		#mix.Result -> group_output.Image
		node_tree.links.new(mix.outputs[2], group_output.inputs[0])
		#group_input.Strength -> ellipse_mask.Mask
		node_tree.links.new(group_input.outputs[2], ellipse_mask.inputs[0])
		#group_input.Color -> mix.B
		node_tree.links.new(group_input.outputs[1], mix.inputs[7])
		#group_input.Position -> ellipse_mask.Position
		node_tree.links.new(group_input.outputs[3], ellipse_mask.inputs[2])
		#group_input.Falloff -> math_001.Value
		node_tree.links.new(group_input.outputs[5], math_001.inputs[0])
		#math_001.Value -> blur.Size
		node_tree.links.new(math_001.outputs[0], blur.inputs[1])
		#combine_xyz.Vector -> ellipse_mask.Size
		node_tree.links.new(combine_xyz.outputs[0], ellipse_mask.inputs[3])
		#separate_xyz.X -> combine_xyz.X
		node_tree.links.new(separate_xyz.outputs[0], combine_xyz.inputs[0])
		#separate_xyz.Y -> math.Value
		node_tree.links.new(separate_xyz.outputs[1], math.inputs[0])
		#group_input.Size -> separate_xyz.Vector
		node_tree.links.new(group_input.outputs[4], separate_xyz.inputs[0])

		return node_tree
