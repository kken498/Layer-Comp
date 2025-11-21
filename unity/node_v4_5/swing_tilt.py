import bpy
from ..node import *

class CompositorNodeSwingTilt(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeEdgeSoftness'
	bl_label='Swing-Tilt'
	bl_icon='AREA_SWAP'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Blur Size"].default_value = 35

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
		image_socket_1.hide_value = True
		image_socket_1.default_input = 'VALUE'
		image_socket_1.structure_type = 'AUTO'

		#Socket Blur Size
		blur_size_socket = node_tree.interface.new_socket(name = "Blur Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
		blur_size_socket.default_value = 35.0
		blur_size_socket.min_value = 0.0
		blur_size_socket.max_value = 200.0
		blur_size_socket.subtype = 'NONE'
		blur_size_socket.attribute_domain = 'POINT'
		blur_size_socket.default_input = 'VALUE'
		blur_size_socket.structure_type = 'AUTO'

		#Socket X1
		x1_socket = node_tree.interface.new_socket(name = "X1", in_out='INPUT', socket_type = 'NodeSocketFloat')
		x1_socket.default_value = 0.0
		x1_socket.min_value = -1.0
		x1_socket.max_value = 1.0
		x1_socket.subtype = 'FACTOR'
		x1_socket.attribute_domain = 'POINT'
		x1_socket.default_input = 'VALUE'
		x1_socket.structure_type = 'AUTO'

		#Socket Y1
		y1_socket = node_tree.interface.new_socket(name = "Y1", in_out='INPUT', socket_type = 'NodeSocketFloat')
		y1_socket.default_value = 0.0
		y1_socket.min_value = -1.0
		y1_socket.max_value = 1.0
		y1_socket.subtype = 'FACTOR'
		y1_socket.attribute_domain = 'POINT'
		y1_socket.default_input = 'VALUE'
		y1_socket.structure_type = 'AUTO'

		#Socket X2
		x2_socket = node_tree.interface.new_socket(name = "X2", in_out='INPUT', socket_type = 'NodeSocketFloat')
		x2_socket.default_value = 0.0
		x2_socket.min_value = -1.0
		x2_socket.max_value = 1.0
		x2_socket.subtype = 'FACTOR'
		x2_socket.attribute_domain = 'POINT'
		x2_socket.default_input = 'VALUE'
		x2_socket.structure_type = 'AUTO'

		#Socket Y2
		y2_socket = node_tree.interface.new_socket(name = "Y2", in_out='INPUT', socket_type = 'NodeSocketFloat')
		y2_socket.default_value = 0.0
		y2_socket.min_value = -1.0
		y2_socket.max_value = 1.0
		y2_socket.subtype = 'FACTOR'
		y2_socket.attribute_domain = 'POINT'
		y2_socket.default_input = 'VALUE'
		y2_socket.structure_type = 'AUTO'

		#Socket Center
		center_socket = node_tree.interface.new_socket(name = "Center", in_out='INPUT', socket_type = 'NodeSocketFloat')
		center_socket.default_value = 0.0
		center_socket.min_value = -1.0
		center_socket.max_value = 1.0
		center_socket.subtype = 'FACTOR'
		center_socket.attribute_domain = 'POINT'
		center_socket.default_input = 'VALUE'
		center_socket.structure_type = 'AUTO'


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Vector Math.009
		vector_math_009 = node_tree.nodes.new("ShaderNodeVectorMath")
		vector_math_009.name = "Vector Math.009"
		vector_math_009.operation = 'DOT_PRODUCT'

		#node Vector Math.010
		vector_math_010 = node_tree.nodes.new("ShaderNodeVectorMath")
		vector_math_010.name = "Vector Math.010"
		vector_math_010.operation = 'SUBTRACT'

		#node Vector Math.011
		vector_math_011 = node_tree.nodes.new("ShaderNodeVectorMath")
		vector_math_011.name = "Vector Math.011"
		vector_math_011.operation = 'SUBTRACT'

		#node Image Coordinates.002
		image_coordinates_002 = node_tree.nodes.new("CompositorNodeImageCoordinates")
		image_coordinates_002.name = "Image Coordinates.002"

		#node Combine XYZ
		combine_xyz = node_tree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz.name = "Combine XYZ"
		#Z
		combine_xyz.inputs[2].default_value = 0.0

		#node Combine XYZ.001
		combine_xyz_001 = node_tree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz_001.name = "Combine XYZ.001"
		#Y
		combine_xyz_001.inputs[1].default_value = 0.0
		#Z
		combine_xyz_001.inputs[2].default_value = 0.0

		#node Combine XYZ.002
		combine_xyz_002 = node_tree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz_002.name = "Combine XYZ.002"
		#X
		combine_xyz_002.inputs[0].default_value = 0.0
		#Z
		combine_xyz_002.inputs[2].default_value = 0.0

		#node Vector Math.012
		vector_math_012 = node_tree.nodes.new("ShaderNodeVectorMath")
		vector_math_012.name = "Vector Math.012"
		vector_math_012.operation = 'DOT_PRODUCT'

		#node Vector Math.013
		vector_math_013 = node_tree.nodes.new("ShaderNodeVectorMath")
		vector_math_013.name = "Vector Math.013"
		vector_math_013.operation = 'SUBTRACT'

		#node Combine XYZ.003
		combine_xyz_003 = node_tree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz_003.name = "Combine XYZ.003"
		#Z
		combine_xyz_003.inputs[2].default_value = 0.0

		#node Combine XYZ.004
		combine_xyz_004 = node_tree.nodes.new("ShaderNodeCombineXYZ")
		combine_xyz_004.name = "Combine XYZ.004"
		#Y
		combine_xyz_004.inputs[1].default_value = 0.0
		#Z
		combine_xyz_004.inputs[2].default_value = 0.0

		#node Math
		math = node_tree.nodes.new("ShaderNodeMath")
		math.name = "Math"
		math.operation = 'MULTIPLY'
		math.use_clamp = False
		#Value_001
		math.inputs[1].default_value = 0.75

		#node Math.003
		math_003 = node_tree.nodes.new("ShaderNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'MAXIMUM'
		math_003.use_clamp = False

		#node Map Range
		map_range = node_tree.nodes.new("ShaderNodeMapRange")
		map_range.name = "Map Range"
		map_range.clamp = False
		map_range.data_type = 'FLOAT'
		map_range.interpolation_type = 'LINEAR'
		#Value
		map_range.inputs[0].default_value = 0.0
		#From Max
		map_range.inputs[2].default_value = 1.0099999904632568
		#To Min
		map_range.inputs[3].default_value = 1.0
		#To Max
		map_range.inputs[4].default_value = -1.0

		#node Map Range.001
		map_range_001 = node_tree.nodes.new("ShaderNodeMapRange")
		map_range_001.name = "Map Range.001"
		map_range_001.clamp = False
		map_range_001.data_type = 'FLOAT'
		map_range_001.interpolation_type = 'LINEAR'
		#Value
		map_range_001.inputs[0].default_value = 0.0
		#From Max
		map_range_001.inputs[2].default_value = 1.0099999904632568
		#To Min
		map_range_001.inputs[3].default_value = -1.0
		#To Max
		map_range_001.inputs[4].default_value = 1.0

		#node Blur.001
		blur_001 = node_tree.nodes.new("CompositorNodeBlur")
		blur_001.name = "Blur.001"
		blur_001.filter_type = 'FAST_GAUSS'
		#Extend Bounds
		blur_001.inputs[2].default_value = False
		#Separable
		blur_001.inputs[3].default_value = True

		#node Math.001
		math_001 = node_tree.nodes.new("ShaderNodeMath")
		math_001.name = "Math.001"
		math_001.operation = 'MULTIPLY'
		math_001.use_clamp = False

		#node Clamp
		clamp = node_tree.nodes.new("ShaderNodeClamp")
		clamp.name = "Clamp"
		clamp.clamp_type = 'MINMAX'
		#Min
		clamp.inputs[1].default_value = 0.0
		#Max
		clamp.inputs[2].default_value = 1.0

		#initialize node_tree links
		#vector_math_011.Vector -> vector_math_009.Vector
		node_tree.links.new(vector_math_011.outputs[0], vector_math_009.inputs[1])
		#image_coordinates_002.Uniform -> vector_math_010.Vector
		node_tree.links.new(image_coordinates_002.outputs[0], vector_math_010.inputs[0])
		#vector_math_010.Vector -> vector_math_009.Vector
		node_tree.links.new(vector_math_010.outputs[0], vector_math_009.inputs[0])
		#group_input.Image -> image_coordinates_002.Image
		node_tree.links.new(group_input.outputs[0], image_coordinates_002.inputs[0])
		#combine_xyz_001.Vector -> vector_math_011.Vector
		node_tree.links.new(combine_xyz_001.outputs[0], vector_math_011.inputs[1])
		#combine_xyz.Vector -> vector_math_011.Vector
		node_tree.links.new(combine_xyz.outputs[0], vector_math_011.inputs[0])
		#combine_xyz_002.Vector -> vector_math_010.Vector
		node_tree.links.new(combine_xyz_002.outputs[0], vector_math_010.inputs[1])
		#vector_math_010.Vector -> vector_math_012.Vector
		node_tree.links.new(vector_math_010.outputs[0], vector_math_012.inputs[0])
		#combine_xyz_003.Vector -> vector_math_013.Vector
		node_tree.links.new(combine_xyz_003.outputs[0], vector_math_013.inputs[0])
		#combine_xyz_004.Vector -> vector_math_013.Vector
		node_tree.links.new(combine_xyz_004.outputs[0], vector_math_013.inputs[1])
		#vector_math_013.Vector -> vector_math_012.Vector
		node_tree.links.new(vector_math_013.outputs[0], vector_math_012.inputs[1])
		#group_input.X1 -> combine_xyz_001.X
		node_tree.links.new(group_input.outputs[2], combine_xyz_001.inputs[0])
		#group_input.X1 -> combine_xyz_003.X
		node_tree.links.new(group_input.outputs[2], combine_xyz_003.inputs[0])
		#group_input.X2 -> combine_xyz.X
		node_tree.links.new(group_input.outputs[4], combine_xyz.inputs[0])
		#group_input.X2 -> combine_xyz_004.X
		node_tree.links.new(group_input.outputs[4], combine_xyz_004.inputs[0])
		#group_input.Center -> math.Value
		node_tree.links.new(group_input.outputs[6], math.inputs[0])
		#math.Value -> combine_xyz_002.Y
		node_tree.links.new(math.outputs[0], combine_xyz_002.inputs[1])
		#vector_math_009.Value -> math_003.Value
		node_tree.links.new(vector_math_009.outputs[1], math_003.inputs[0])
		#vector_math_012.Value -> math_003.Value
		node_tree.links.new(vector_math_012.outputs[1], math_003.inputs[1])
		#map_range_001.Result -> combine_xyz.Y
		node_tree.links.new(map_range_001.outputs[0], combine_xyz.inputs[1])
		#group_input.Y2 -> map_range_001.From Min
		node_tree.links.new(group_input.outputs[5], map_range_001.inputs[1])
		#map_range.Result -> combine_xyz_003.Y
		node_tree.links.new(map_range.outputs[0], combine_xyz_003.inputs[1])
		#group_input.Y1 -> map_range.From Min
		node_tree.links.new(group_input.outputs[3], map_range.inputs[1])
		#math_001.Value -> blur_001.Size
		node_tree.links.new(math_001.outputs[0], blur_001.inputs[1])
		#group_input.Image -> blur_001.Image
		node_tree.links.new(group_input.outputs[0], blur_001.inputs[0])
		#blur_001.Image -> group_output.Image
		node_tree.links.new(blur_001.outputs[0], group_output.inputs[0])
		#clamp.Result -> math_001.Value
		node_tree.links.new(clamp.outputs[0], math_001.inputs[0])
		#group_input.Blur Size -> math_001.Value
		node_tree.links.new(group_input.outputs[1], math_001.inputs[1])
		#math_003.Value -> clamp.Value
		node_tree.links.new(math_003.outputs[0], clamp.inputs[0])
		return node_tree
