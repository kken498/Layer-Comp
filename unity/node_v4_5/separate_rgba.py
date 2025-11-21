import bpy
from ..node import *

class CompositorNodeSeparateRGBA(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeSeparateRGBA'
	bl_label='Separate RGBA'
	bl_icon='PARTICLES'

	def init(self, context):
		self.getNodetree(context)

	def draw_buttons(self, context, layout):
		return

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"	

		#node_tree interface
		#Socket R
		r_socket = node_tree.interface.new_socket(name = "R", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		r_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		r_socket.attribute_domain = 'POINT'
		r_socket.default_input = 'VALUE'
		r_socket.structure_type = 'AUTO'

		#Socket G
		g_socket = node_tree.interface.new_socket(name = "G", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		g_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		g_socket.attribute_domain = 'POINT'
		g_socket.default_input = 'VALUE'
		g_socket.structure_type = 'AUTO'

		#Socket B
		b_socket = node_tree.interface.new_socket(name = "B", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		b_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		b_socket.attribute_domain = 'POINT'
		b_socket.default_input = 'VALUE'
		b_socket.structure_type = 'AUTO'

		#Socket Alpha
		alpha_socket = node_tree.interface.new_socket(name = "Alpha", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		alpha_socket.default_value = 0.0
		alpha_socket.min_value = -3.4028234663852886e+38
		alpha_socket.max_value = 3.4028234663852886e+38
		alpha_socket.subtype = 'NONE'
		alpha_socket.attribute_domain = 'POINT'
		alpha_socket.default_input = 'VALUE'
		alpha_socket.structure_type = 'AUTO'

		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.hide_value = True
		image_socket.default_input = 'VALUE'
		image_socket.structure_type = 'AUTO'


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

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#initialize node_tree links
		#group_input.Image -> rgb_curves_001.Image
		node_tree.links.new(group_input.outputs[0], rgb_curves_001.inputs[1])
		#group_input.Image -> rgb_curves_002.Image
		node_tree.links.new(group_input.outputs[0], rgb_curves_002.inputs[1])
		#rgb_curves_001.Image -> group_output.G
		node_tree.links.new(rgb_curves_001.outputs[0], group_output.inputs[1])
		#rgb_curves_002.Image -> group_output.b
		node_tree.links.new(rgb_curves_002.outputs[0], group_output.inputs[2])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		#separate_color.Alpha -> group_output.Alpha
		node_tree.links.new(separate_color.outputs[3], group_output.inputs[3])
		#group_input.Image -> rgb_curves.Image
		node_tree.links.new(group_input.outputs[0], rgb_curves.inputs[1])
		#rgb_curves.Image -> group_output.R
		node_tree.links.new(rgb_curves.outputs[0], group_output.inputs[0])
		return node_tree
