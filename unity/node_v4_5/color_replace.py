import bpy
from ..node import *

class CompositorNodeColorReplace(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeColorReplace'
	bl_label='Color Replace'
	bl_icon='OVERLAY'

	def update_count(self, context):
		if self.count >= 2:
			self.node_tree.nodes["Mix.002"].mute = False
			self.node_tree.nodes["Math.002"].mute = False
		else:
			self.node_tree.nodes["Mix.002"].mute = True
			self.node_tree.nodes["Math.002"].mute = True

		if self.count >= 3:
			self.node_tree.nodes["Mix.003"].mute = False
			self.node_tree.nodes["Math.003"].mute = False
		else:
			self.node_tree.nodes["Mix.003"].mute = True
			self.node_tree.nodes["Math.003"].mute = True

		if self.count >= 4:
			self.node_tree.nodes["Mix.004"].mute = False
			self.node_tree.nodes["Math.004"].mute = False
		else:
			self.node_tree.nodes["Mix.004"].mute = True
			self.node_tree.nodes["Math.004"].mute = True

		if self.count >= 5:
			self.node_tree.nodes["Mix.005"].mute = False
			self.node_tree.nodes["Math.005"].mute = False
		else:
			self.node_tree.nodes["Mix.005"].mute = True
			self.node_tree.nodes["Math.005"].mute = True

		if self.count >= 6:
			self.node_tree.nodes["Mix.006"].mute = False
			self.node_tree.nodes["Math.006"].mute = False
		else:
			self.node_tree.nodes["Mix.006"].mute = True
			self.node_tree.nodes["Math.006"].mute = True

		if self.count >= 7:
			self.node_tree.nodes["Mix.007"].mute = False
			self.node_tree.nodes["Math.007"].mute = False
		else:
			self.node_tree.nodes["Mix.007"].mute = True
			self.node_tree.nodes["Math.007"].mute = True

		if self.count >= 8:
			self.node_tree.nodes["Mix.008"].mute = False
			self.node_tree.nodes["Math.008"].mute = False
		else:
			self.node_tree.nodes["Mix.008"].mute = True
			self.node_tree.nodes["Math.008"].mute = True

	count : bpy.props.IntProperty(default = 1, name = "Count", update = update_count, min=1, max=8)

	def init(self, context):
		self.getNodetree(context)
		self.count = 1
		for input in self.inputs:
			if input.name == "Key Color":
				input.default_value = (0.92,0,0.059,1)
			if input.name == "Replace Color":
				input.default_value = (0, 0.456, 0.9, 1.0)
			if input.name in ["Hue", "Saturation", "Value"]:
				input.default_value = 0.15

	def draw_buttons(self, context, layout):
		layout.prop(self, "count")
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

		#Panel Color1
		color1_panel = node_tree.interface.new_panel("Color1")
		#Socket Key Color
		key_color_socket = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color1_panel)
		key_color_socket.default_value = (0.92,0,0.059,1)
		key_color_socket.attribute_domain = 'POINT'
		key_color_socket.default_input = 'VALUE'
		key_color_socket.structure_type = 'AUTO'

		#Socket Replace Color
		node_tree_socket = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color1_panel)
		node_tree_socket.default_value = (0, 0.456, 0.9, 1.0)
		node_tree_socket.attribute_domain = 'POINT'
		node_tree_socket.description = "Value of the first color input"
		node_tree_socket.default_input = 'VALUE'
		node_tree_socket.structure_type = 'AUTO'

		#Panel Bias Range
		bias_range_panel = node_tree.interface.new_panel("Bias Range")
		#Socket Hue
		hue_socket = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel)
		hue_socket.default_value = 0.15000000596046448
		hue_socket.min_value = 0.0
		hue_socket.max_value = 1.0
		hue_socket.subtype = 'FACTOR'
		hue_socket.attribute_domain = 'POINT'
		hue_socket.description = "If the difference in hue between the color and key color is less than this threshold, it is keyed"
		hue_socket.default_input = 'VALUE'
		hue_socket.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel)
		saturation_socket.default_value = 0.15000000596046448
		saturation_socket.min_value = 0.0
		saturation_socket.max_value = 1.0
		saturation_socket.subtype = 'FACTOR'
		saturation_socket.attribute_domain = 'POINT'
		saturation_socket.description = "If the difference in saturation between the color and key color is less than this threshold, it is keyed"
		saturation_socket.default_input = 'VALUE'
		saturation_socket.structure_type = 'AUTO'

		#Socket Value
		value_socket = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel)
		value_socket.default_value = 0.15000000596046448
		value_socket.min_value = 0.0
		value_socket.max_value = 1.0
		value_socket.subtype = 'FACTOR'
		value_socket.attribute_domain = 'POINT'
		value_socket.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		value_socket.default_input = 'VALUE'
		value_socket.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(bias_range_panel, color1_panel, 6)

		#Panel Color2
		color2_panel = node_tree.interface.new_panel("Color2", default_closed = True)
		#Socket Key Color
		key_color_socket_1 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color2_panel)
		key_color_socket_1.default_value = (0.92,0,0.059,1)
		key_color_socket_1.attribute_domain = 'POINT'
		key_color_socket_1.default_input = 'VALUE'
		key_color_socket_1.structure_type = 'AUTO'

		#Socket Replace Color
		node_tree_socket_1 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color2_panel)
		node_tree_socket_1.default_value = (0, 0.456, 0.9, 1.0)
		node_tree_socket_1.attribute_domain = 'POINT'
		node_tree_socket_1.description = "Value of the first color input"
		node_tree_socket_1.default_input = 'VALUE'
		node_tree_socket_1.structure_type = 'AUTO'

		#Panel Bias Range
		bias_range_panel_1 = node_tree.interface.new_panel("Bias Range")
		#Socket Hue
		hue_socket_1 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_1)
		hue_socket_1.default_value = 0.15000000596046448
		hue_socket_1.min_value = 0.0
		hue_socket_1.max_value = 1.0
		hue_socket_1.subtype = 'FACTOR'
		hue_socket_1.attribute_domain = 'POINT'
		hue_socket_1.description = "If the difference in hue between the color and key color is less than this threshold, it is keyed"
		hue_socket_1.default_input = 'VALUE'
		hue_socket_1.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_1 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_1)
		saturation_socket_1.default_value = 0.15000000596046448
		saturation_socket_1.min_value = 0.0
		saturation_socket_1.max_value = 1.0
		saturation_socket_1.subtype = 'FACTOR'
		saturation_socket_1.attribute_domain = 'POINT'
		saturation_socket_1.description = "If the difference in saturation between the color and key color is less than this threshold, it is keyed"
		saturation_socket_1.default_input = 'VALUE'
		saturation_socket_1.structure_type = 'AUTO'

		#Socket Value
		value_socket_1 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_1)
		value_socket_1.default_value = 0.15000000596046448
		value_socket_1.min_value = 0.0
		value_socket_1.max_value = 1.0
		value_socket_1.subtype = 'FACTOR'
		value_socket_1.attribute_domain = 'POINT'
		value_socket_1.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		value_socket_1.default_input = 'VALUE'
		value_socket_1.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(bias_range_panel_1, color2_panel, 13)

		#Panel Color3
		color3_panel = node_tree.interface.new_panel("Color3", default_closed = True)
		#Socket Key Color
		key_color_socket_2 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color3_panel)
		key_color_socket_2.default_value = (0.92,0,0.059,1)
		key_color_socket_2.attribute_domain = 'POINT'
		key_color_socket_2.default_input = 'VALUE'
		key_color_socket_2.structure_type = 'AUTO'

		#Socket Replace Color
		node_tree_socket_2 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color3_panel)
		node_tree_socket_2.default_value = (0, 0.456, 0.9, 1.0)
		node_tree_socket_2.attribute_domain = 'POINT'
		node_tree_socket_2.description = "Value of the first color input"
		node_tree_socket_2.default_input = 'VALUE'
		node_tree_socket_2.structure_type = 'AUTO'

		#Panel Bias Range
		bias_range_panel_2 = node_tree.interface.new_panel("Bias Range")
		#Socket Hue
		hue_socket_2 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_2)
		hue_socket_2.default_value = 0.15000000596046448
		hue_socket_2.min_value = 0.0
		hue_socket_2.max_value = 1.0
		hue_socket_2.subtype = 'FACTOR'
		hue_socket_2.attribute_domain = 'POINT'
		hue_socket_2.description = "If the difference in hue between the color and key color is less than this threshold, it is keyed"
		hue_socket_2.default_input = 'VALUE'
		hue_socket_2.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_2 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_2)
		saturation_socket_2.default_value = 0.15000000596046448
		saturation_socket_2.min_value = 0.0
		saturation_socket_2.max_value = 1.0
		saturation_socket_2.subtype = 'FACTOR'
		saturation_socket_2.attribute_domain = 'POINT'
		saturation_socket_2.description = "If the difference in saturation between the color and key color is less than this threshold, it is keyed"
		saturation_socket_2.default_input = 'VALUE'
		saturation_socket_2.structure_type = 'AUTO'

		#Socket Value
		value_socket_2 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_2)
		value_socket_2.default_value = 0.15000000596046448
		value_socket_2.min_value = 0.0
		value_socket_2.max_value = 1.0
		value_socket_2.subtype = 'FACTOR'
		value_socket_2.attribute_domain = 'POINT'
		value_socket_2.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		value_socket_2.default_input = 'VALUE'
		value_socket_2.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(bias_range_panel_2, color3_panel, 20)

		#Panel Color4
		color4_panel = node_tree.interface.new_panel("Color4", default_closed = True)
		#Socket Key Color
		key_color_socket_3 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color4_panel)
		key_color_socket_3.default_value = (0.92,0,0.059,1)
		key_color_socket_3.attribute_domain = 'POINT'
		key_color_socket_3.default_input = 'VALUE'
		key_color_socket_3.structure_type = 'AUTO'

		#Socket Replace Color
		node_tree_socket_3 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color4_panel)
		node_tree_socket_3.default_value = (0, 0.456, 0.9, 1.0)
		node_tree_socket_3.attribute_domain = 'POINT'
		node_tree_socket_3.description = "Value of the first color input"
		node_tree_socket_3.default_input = 'VALUE'
		node_tree_socket_3.structure_type = 'AUTO'

		#Panel Bias Range
		bias_range_panel_3 = node_tree.interface.new_panel("Bias Range")
		#Socket Hue
		hue_socket_3 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_3)
		hue_socket_3.default_value = 0.15000000596046448
		hue_socket_3.min_value = 0.0
		hue_socket_3.max_value = 1.0
		hue_socket_3.subtype = 'FACTOR'
		hue_socket_3.attribute_domain = 'POINT'
		hue_socket_3.description = "If the difference in hue between the color and key color is less than this threshold, it is keyed"
		hue_socket_3.default_input = 'VALUE'
		hue_socket_3.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_3 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_3)
		saturation_socket_3.default_value = 0.15000000596046448
		saturation_socket_3.min_value = 0.0
		saturation_socket_3.max_value = 1.0
		saturation_socket_3.subtype = 'FACTOR'
		saturation_socket_3.attribute_domain = 'POINT'
		saturation_socket_3.description = "If the difference in saturation between the color and key color is less than this threshold, it is keyed"
		saturation_socket_3.default_input = 'VALUE'
		saturation_socket_3.structure_type = 'AUTO'

		#Socket Value
		value_socket_3 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_3)
		value_socket_3.default_value = 0.15000000596046448
		value_socket_3.min_value = 0.0
		value_socket_3.max_value = 1.0
		value_socket_3.subtype = 'FACTOR'
		value_socket_3.attribute_domain = 'POINT'
		value_socket_3.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		value_socket_3.default_input = 'VALUE'
		value_socket_3.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(bias_range_panel_3, color4_panel, 27)

		#Panel Color5
		color5_panel = node_tree.interface.new_panel("Color5", default_closed = True)
		#Socket Key Color
		key_color_socket_4 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color5_panel)
		key_color_socket_4.default_value = (0.92,0,0.059,1)
		key_color_socket_4.attribute_domain = 'POINT'
		key_color_socket_4.default_input = 'VALUE'
		key_color_socket_4.structure_type = 'AUTO'

		#Socket Replace Color
		node_tree_socket_4 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color5_panel)
		node_tree_socket_4.default_value = (0, 0.456, 0.9, 1.0)
		node_tree_socket_4.attribute_domain = 'POINT'
		node_tree_socket_4.description = "Value of the first color input"
		node_tree_socket_4.default_input = 'VALUE'
		node_tree_socket_4.structure_type = 'AUTO'

		#Panel Bias Range
		bias_range_panel_4 = node_tree.interface.new_panel("Bias Range")
		#Socket Hue
		hue_socket_4 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_4)
		hue_socket_4.default_value = 0.15000000596046448
		hue_socket_4.min_value = 0.0
		hue_socket_4.max_value = 1.0
		hue_socket_4.subtype = 'FACTOR'
		hue_socket_4.attribute_domain = 'POINT'
		hue_socket_4.description = "If the difference in hue between the color and key color is less than this threshold, it is keyed"
		hue_socket_4.default_input = 'VALUE'
		hue_socket_4.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_4 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_4)
		saturation_socket_4.default_value = 0.15000000596046448
		saturation_socket_4.min_value = 0.0
		saturation_socket_4.max_value = 1.0
		saturation_socket_4.subtype = 'FACTOR'
		saturation_socket_4.attribute_domain = 'POINT'
		saturation_socket_4.description = "If the difference in saturation between the color and key color is less than this threshold, it is keyed"
		saturation_socket_4.default_input = 'VALUE'
		saturation_socket_4.structure_type = 'AUTO'

		#Socket Value
		value_socket_4 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_4)
		value_socket_4.default_value = 0.15000000596046448
		value_socket_4.min_value = 0.0
		value_socket_4.max_value = 1.0
		value_socket_4.subtype = 'FACTOR'
		value_socket_4.attribute_domain = 'POINT'
		value_socket_4.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		value_socket_4.default_input = 'VALUE'
		value_socket_4.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(bias_range_panel_4, color5_panel, 34)

		#Panel Color6
		color6_panel = node_tree.interface.new_panel("Color6", default_closed = True)
		#Socket Key Color
		key_color_socket_5 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color6_panel)
		key_color_socket_5.default_value = (0.92,0,0.059,1)
		key_color_socket_5.attribute_domain = 'POINT'
		key_color_socket_5.default_input = 'VALUE'
		key_color_socket_5.structure_type = 'AUTO'

		#Socket Replace Color
		node_tree_socket_5 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color6_panel)
		node_tree_socket_5.default_value = (0, 0.456, 0.9, 1.0)
		node_tree_socket_5.attribute_domain = 'POINT'
		node_tree_socket_5.description = "Value of the first color input"
		node_tree_socket_5.default_input = 'VALUE'
		node_tree_socket_5.structure_type = 'AUTO'

		#Panel Bias Range
		bias_range_panel_5 = node_tree.interface.new_panel("Bias Range")
		#Socket Hue
		hue_socket_5 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_5)
		hue_socket_5.default_value = 0.15000000596046448
		hue_socket_5.min_value = 0.0
		hue_socket_5.max_value = 1.0
		hue_socket_5.subtype = 'FACTOR'
		hue_socket_5.attribute_domain = 'POINT'
		hue_socket_5.description = "If the difference in hue between the color and key color is less than this threshold, it is keyed"
		hue_socket_5.default_input = 'VALUE'
		hue_socket_5.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_5 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_5)
		saturation_socket_5.default_value = 0.15000000596046448
		saturation_socket_5.min_value = 0.0
		saturation_socket_5.max_value = 1.0
		saturation_socket_5.subtype = 'FACTOR'
		saturation_socket_5.attribute_domain = 'POINT'
		saturation_socket_5.description = "If the difference in saturation between the color and key color is less than this threshold, it is keyed"
		saturation_socket_5.default_input = 'VALUE'
		saturation_socket_5.structure_type = 'AUTO'

		#Socket Value
		value_socket_5 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_5)
		value_socket_5.default_value = 0.15000000596046448
		value_socket_5.min_value = 0.0
		value_socket_5.max_value = 1.0
		value_socket_5.subtype = 'FACTOR'
		value_socket_5.attribute_domain = 'POINT'
		value_socket_5.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		value_socket_5.default_input = 'VALUE'
		value_socket_5.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(bias_range_panel_5, color6_panel, 41)

		#Panel Color7
		color7_panel = node_tree.interface.new_panel("Color7", default_closed = True)
		#Socket Key Color
		key_color_socket_6 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color7_panel)
		key_color_socket_6.default_value = (0.92,0,0.059,1)
		key_color_socket_6.attribute_domain = 'POINT'
		key_color_socket_6.default_input = 'VALUE'
		key_color_socket_6.structure_type = 'AUTO'

		#Socket Replace Color
		node_tree_socket_6 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color7_panel)
		node_tree_socket_6.default_value = (0, 0.456, 0.9, 1.0)
		node_tree_socket_6.attribute_domain = 'POINT'
		node_tree_socket_6.description = "Value of the first color input"
		node_tree_socket_6.default_input = 'VALUE'
		node_tree_socket_6.structure_type = 'AUTO'

		#Panel Bias Range
		bias_range_panel_6 = node_tree.interface.new_panel("Bias Range")
		#Socket Hue
		hue_socket_6 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_6)
		hue_socket_6.default_value = 0.15000000596046448
		hue_socket_6.min_value = 0.0
		hue_socket_6.max_value = 1.0
		hue_socket_6.subtype = 'FACTOR'
		hue_socket_6.attribute_domain = 'POINT'
		hue_socket_6.description = "If the difference in hue between the color and key color is less than this threshold, it is keyed"
		hue_socket_6.default_input = 'VALUE'
		hue_socket_6.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_6 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_6)
		saturation_socket_6.default_value = 0.15000000596046448
		saturation_socket_6.min_value = 0.0
		saturation_socket_6.max_value = 1.0
		saturation_socket_6.subtype = 'FACTOR'
		saturation_socket_6.attribute_domain = 'POINT'
		saturation_socket_6.description = "If the difference in saturation between the color and key color is less than this threshold, it is keyed"
		saturation_socket_6.default_input = 'VALUE'
		saturation_socket_6.structure_type = 'AUTO'

		#Socket Value
		value_socket_6 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_6)
		value_socket_6.default_value = 0.15000000596046448
		value_socket_6.min_value = 0.0
		value_socket_6.max_value = 1.0
		value_socket_6.subtype = 'FACTOR'
		value_socket_6.attribute_domain = 'POINT'
		value_socket_6.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		value_socket_6.default_input = 'VALUE'
		value_socket_6.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(bias_range_panel_6, color7_panel, 48)

		#Panel Color8
		color8_panel = node_tree.interface.new_panel("Color8", default_closed = True)
		#Socket Key Color
		key_color_socket_7 = node_tree.interface.new_socket(name = "Key Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color8_panel)
		key_color_socket_7.default_value = (0.92,0,0.059,1)
		key_color_socket_7.attribute_domain = 'POINT'
		key_color_socket_7.default_input = 'VALUE'
		key_color_socket_7.structure_type = 'AUTO'

		#Socket Replace Color
		node_tree_socket_7 = node_tree.interface.new_socket(name = "Replace Color", in_out='INPUT', socket_type = 'NodeSocketColor', parent = color8_panel)
		node_tree_socket_7.default_value = (0, 0.456, 0.9, 1.0)
		node_tree_socket_7.attribute_domain = 'POINT'
		node_tree_socket_7.description = "Value of the first color input"
		node_tree_socket_7.default_input = 'VALUE'
		node_tree_socket_7.structure_type = 'AUTO'

		#Panel Bias Range
		bias_range_panel_7 = node_tree.interface.new_panel("Bias Range")
		#Socket Hue
		hue_socket_7 = node_tree.interface.new_socket(name = "Hue", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_7)
		hue_socket_7.default_value = 0.15000000596046448
		hue_socket_7.min_value = 0.0
		hue_socket_7.max_value = 1.0
		hue_socket_7.subtype = 'FACTOR'
		hue_socket_7.attribute_domain = 'POINT'
		hue_socket_7.description = "If the difference in hue between the color and key color is less than this threshold, it is keyed"
		hue_socket_7.default_input = 'VALUE'
		hue_socket_7.structure_type = 'AUTO'

		#Socket Saturation
		saturation_socket_7 = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_7)
		saturation_socket_7.default_value = 0.15000000596046448
		saturation_socket_7.min_value = 0.0
		saturation_socket_7.max_value = 1.0
		saturation_socket_7.subtype = 'FACTOR'
		saturation_socket_7.attribute_domain = 'POINT'
		saturation_socket_7.description = "If the difference in saturation between the color and key color is less than this threshold, it is keyed"
		saturation_socket_7.default_input = 'VALUE'
		saturation_socket_7.structure_type = 'AUTO'

		#Socket Value
		value_socket_7 = node_tree.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bias_range_panel_7)
		value_socket_7.default_value = 0.15000000596046448
		value_socket_7.min_value = 0.0
		value_socket_7.max_value = 1.0
		value_socket_7.subtype = 'FACTOR'
		value_socket_7.attribute_domain = 'POINT'
		value_socket_7.description = "If the difference in value between the color and key color is less than this threshold, it is keyed"
		value_socket_7.default_input = 'VALUE'
		value_socket_7.structure_type = 'AUTO'


		node_tree.interface.move_to_parent(bias_range_panel_7, color8_panel, 55)


		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Color Key
		color_key = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key.name = "Color Key"

		#node Alpha
		alpha = node_tree.nodes.new("ShaderNodeMix")
		alpha.name = "Alpha"
		alpha.blend_type = 'MIX'
		alpha.clamp_factor = True
		alpha.clamp_result = False
		alpha.data_type = 'RGBA'
		alpha.factor_mode = 'UNIFORM'

		#node Alpha.001
		alpha_001 = node_tree.nodes.new("ShaderNodeMath")
		alpha_001.name = "Alpha.001"
		alpha_001.operation = 'SUBTRACT'
		alpha_001.use_clamp = False

		#node Mix.002
		mix_002 = node_tree.nodes.new("ShaderNodeMix")
		mix_002.name = "Mix.002"
		mix_002.blend_type = 'MIX'
		mix_002.clamp_factor = True
		mix_002.clamp_result = False
		mix_002.data_type = 'RGBA'
		mix_002.factor_mode = 'UNIFORM'

		#node Color Key.001
		color_key_001 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_001.name = "Color Key.001"

		#node Alpha.002
		alpha_002 = node_tree.nodes.new("ShaderNodeMath")
		alpha_002.name = "Alpha.002"
		alpha_002.operation = 'SUBTRACT'
		alpha_002.use_clamp = False

		#node Math.002
		math_002 = node_tree.nodes.new("ShaderNodeMath")
		math_002.name = "Math.002"
		math_002.operation = 'ADD'
		math_002.use_clamp = False

		#node Color Key.002
		color_key_002 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_002.name = "Color Key.002"

		#node Alpha.003
		alpha_003 = node_tree.nodes.new("ShaderNodeMath")
		alpha_003.name = "Alpha.003"
		alpha_003.operation = 'SUBTRACT'
		alpha_003.use_clamp = False

		#node Mix.003
		mix_003 = node_tree.nodes.new("ShaderNodeMix")
		mix_003.name = "Mix.003"
		mix_003.blend_type = 'MIX'
		mix_003.clamp_factor = True
		mix_003.clamp_result = False
		mix_003.data_type = 'RGBA'
		mix_003.factor_mode = 'UNIFORM'

		#node Math.003
		math_003 = node_tree.nodes.new("ShaderNodeMath")
		math_003.name = "Math.003"
		math_003.operation = 'ADD'
		math_003.use_clamp = False

		#node Color Key.003
		color_key_003 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_003.name = "Color Key.003"

		#node Alpha.004
		alpha_004 = node_tree.nodes.new("ShaderNodeMath")
		alpha_004.name = "Alpha.004"
		alpha_004.operation = 'SUBTRACT'
		alpha_004.use_clamp = False

		#node Math.004
		math_004 = node_tree.nodes.new("ShaderNodeMath")
		math_004.name = "Math.004"
		math_004.operation = 'ADD'
		math_004.use_clamp = False

		#node Mix.004
		mix_004 = node_tree.nodes.new("ShaderNodeMix")
		mix_004.name = "Mix.004"
		mix_004.blend_type = 'MIX'
		mix_004.clamp_factor = True
		mix_004.clamp_result = False
		mix_004.data_type = 'RGBA'
		mix_004.factor_mode = 'UNIFORM'

		#node Color Key.004
		color_key_004 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_004.name = "Color Key.004"

		#node Alpha.005
		alpha_005 = node_tree.nodes.new("ShaderNodeMath")
		alpha_005.name = "Alpha.005"
		alpha_005.operation = 'SUBTRACT'
		alpha_005.use_clamp = False

		#node Color Key.005
		color_key_005 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_005.name = "Color Key.005"

		#node Alpha.006
		alpha_006 = node_tree.nodes.new("ShaderNodeMath")
		alpha_006.name = "Alpha.006"
		alpha_006.operation = 'SUBTRACT'
		alpha_006.use_clamp = False

		#node Color Key.006
		color_key_006 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_006.name = "Color Key.006"

		#node Alpha.007
		alpha_007 = node_tree.nodes.new("ShaderNodeMath")
		alpha_007.name = "Alpha.007"
		alpha_007.operation = 'SUBTRACT'
		alpha_007.use_clamp = False

		#node Color Key.007
		color_key_007 = node_tree.nodes.new("CompositorNodeColorMatte")
		color_key_007.name = "Color Key.007"

		#node Alpha.008
		alpha_008 = node_tree.nodes.new("ShaderNodeMath")
		alpha_008.name = "Alpha.008"
		alpha_008.operation = 'SUBTRACT'
		alpha_008.use_clamp = False

		#node Mix.005
		mix_005 = node_tree.nodes.new("ShaderNodeMix")
		mix_005.name = "Mix.005"
		mix_005.blend_type = 'MIX'
		mix_005.clamp_factor = True
		mix_005.clamp_result = False
		mix_005.data_type = 'RGBA'
		mix_005.factor_mode = 'UNIFORM'

		#node Mix.006
		mix_006 = node_tree.nodes.new("ShaderNodeMix")
		mix_006.name = "Mix.006"
		mix_006.blend_type = 'MIX'
		mix_006.clamp_factor = True
		mix_006.clamp_result = False
		mix_006.data_type = 'RGBA'
		mix_006.factor_mode = 'UNIFORM'

		#node Mix.007
		mix_007 = node_tree.nodes.new("ShaderNodeMix")
		mix_007.name = "Mix.007"
		mix_007.blend_type = 'MIX'
		mix_007.clamp_factor = True
		mix_007.clamp_result = False
		mix_007.data_type = 'RGBA'
		mix_007.factor_mode = 'UNIFORM'

		#node Mix.008
		mix_008 = node_tree.nodes.new("ShaderNodeMix")
		mix_008.name = "Mix.008"
		mix_008.blend_type = 'MIX'
		mix_008.clamp_factor = True
		mix_008.clamp_result = False
		mix_008.data_type = 'RGBA'
		mix_008.factor_mode = 'UNIFORM'

		#node Math.005
		math_005 = node_tree.nodes.new("ShaderNodeMath")
		math_005.name = "Math.005"
		math_005.operation = 'ADD'
		math_005.use_clamp = False

		#node Math.006
		math_006 = node_tree.nodes.new("ShaderNodeMath")
		math_006.name = "Math.006"
		math_006.operation = 'ADD'
		math_006.use_clamp = False

		#node Math.007
		math_007 = node_tree.nodes.new("ShaderNodeMath")
		math_007.name = "Math.007"
		math_007.operation = 'ADD'
		math_007.use_clamp = False

		#node Math.008
		math_008 = node_tree.nodes.new("ShaderNodeMath")
		math_008.name = "Math.008"
		math_008.operation = 'ADD'
		math_008.use_clamp = False

		#node Separate Color
		separate_color = node_tree.nodes.new("CompositorNodeSeparateColor")
		separate_color.name = "Separate Color"
		separate_color.mode = 'RGB'
		separate_color.ycc_mode = 'ITUBT709'

		#node Reroute
		reroute = node_tree.nodes.new("NodeReroute")
		reroute.name = "Reroute"
		reroute.socket_idname = "NodeSocketFloat"

		#initialize node_tree links
		#group_input.Image -> color_key.Image
		node_tree.links.new(group_input.outputs[0], color_key.inputs[0])
		#group_input.Key Color -> color_key.Key Color
		node_tree.links.new(group_input.outputs[1], color_key.inputs[1])
		#group_input.Hue -> color_key.Hue
		node_tree.links.new(group_input.outputs[3], color_key.inputs[2])
		#group_input.Saturation -> color_key.Saturation
		node_tree.links.new(group_input.outputs[4], color_key.inputs[3])
		#group_input.Value -> color_key.Value
		node_tree.links.new(group_input.outputs[5], color_key.inputs[4])
		#math_008.Value -> group_output.Matte
		node_tree.links.new(math_008.outputs[0], group_output.inputs[1])
		#alpha_001.Value -> alpha.Factor
		node_tree.links.new(alpha_001.outputs[0], alpha.inputs[0])
		#color_key.Matte -> alpha_001.Value
		node_tree.links.new(color_key.outputs[1], alpha_001.inputs[1])
		#reroute.Output -> alpha_001.Value
		node_tree.links.new(reroute.outputs[0], alpha_001.inputs[0])
		#group_input.Image -> alpha.A
		node_tree.links.new(group_input.outputs[0], alpha.inputs[6])
		#group_input.Replace Color -> alpha.B
		node_tree.links.new(group_input.outputs[2], alpha.inputs[7])
		#alpha.Result -> mix_002.A
		node_tree.links.new(alpha.outputs[2], mix_002.inputs[6])
		#color_key_001.Matte -> alpha_002.Value
		node_tree.links.new(color_key_001.outputs[1], alpha_002.inputs[1])
		#reroute.Output -> alpha_002.Value
		node_tree.links.new(reroute.outputs[0], alpha_002.inputs[0])
		#group_input.Image -> color_key_001.Image
		node_tree.links.new(group_input.outputs[0], color_key_001.inputs[0])
		#alpha_002.Value -> mix_002.Factor
		node_tree.links.new(alpha_002.outputs[0], mix_002.inputs[0])
		#group_input.Key Color -> color_key_001.Key Color
		node_tree.links.new(group_input.outputs[6], color_key_001.inputs[1])
		#group_input.Replace Color -> mix_002.B
		node_tree.links.new(group_input.outputs[7], mix_002.inputs[7])
		#group_input.Hue -> color_key_001.Hue
		node_tree.links.new(group_input.outputs[8], color_key_001.inputs[2])
		#group_input.Saturation -> color_key_001.Saturation
		node_tree.links.new(group_input.outputs[9], color_key_001.inputs[3])
		#group_input.Value -> color_key_001.Value
		node_tree.links.new(group_input.outputs[10], color_key_001.inputs[4])
		#alpha_001.Value -> math_002.Value
		node_tree.links.new(alpha_001.outputs[0], math_002.inputs[0])
		#alpha_002.Value -> math_002.Value
		node_tree.links.new(alpha_002.outputs[0], math_002.inputs[1])
		#color_key_002.Matte -> alpha_003.Value
		node_tree.links.new(color_key_002.outputs[1], alpha_003.inputs[1])
		#reroute.Output -> alpha_003.Value
		node_tree.links.new(reroute.outputs[0], alpha_003.inputs[0])
		#group_input.Image -> color_key_002.Image
		node_tree.links.new(group_input.outputs[0], color_key_002.inputs[0])
		#group_input.Key Color -> color_key_002.Key Color
		node_tree.links.new(group_input.outputs[11], color_key_002.inputs[1])
		#group_input.Hue -> color_key_002.Hue
		node_tree.links.new(group_input.outputs[13], color_key_002.inputs[2])
		#group_input.Saturation -> color_key_002.Saturation
		node_tree.links.new(group_input.outputs[14], color_key_002.inputs[3])
		#group_input.Value -> color_key_002.Value
		node_tree.links.new(group_input.outputs[15], color_key_002.inputs[4])
		#alpha_003.Value -> mix_003.Factor
		node_tree.links.new(alpha_003.outputs[0], mix_003.inputs[0])
		#mix_002.Result -> mix_003.A
		node_tree.links.new(mix_002.outputs[2], mix_003.inputs[6])
		#mix_008.Result -> group_output.Image
		node_tree.links.new(mix_008.outputs[2], group_output.inputs[0])
		#group_input.Replace Color -> mix_003.B
		node_tree.links.new(group_input.outputs[12], mix_003.inputs[7])
		#math_002.Value -> math_003.Value
		node_tree.links.new(math_002.outputs[0], math_003.inputs[0])
		#alpha_003.Value -> math_003.Value
		node_tree.links.new(alpha_003.outputs[0], math_003.inputs[1])
		#color_key_003.Matte -> alpha_004.Value
		node_tree.links.new(color_key_003.outputs[1], alpha_004.inputs[1])
		#reroute.Output -> alpha_004.Value
		node_tree.links.new(reroute.outputs[0], alpha_004.inputs[0])
		#group_input.Image -> color_key_003.Image
		node_tree.links.new(group_input.outputs[0], color_key_003.inputs[0])
		#group_input.Key Color -> color_key_003.Key Color
		node_tree.links.new(group_input.outputs[16], color_key_003.inputs[1])
		#group_input.Hue -> color_key_003.Hue
		node_tree.links.new(group_input.outputs[18], color_key_003.inputs[2])
		#group_input.Saturation -> color_key_003.Saturation
		node_tree.links.new(group_input.outputs[19], color_key_003.inputs[3])
		#group_input.Value -> color_key_003.Value
		node_tree.links.new(group_input.outputs[20], color_key_003.inputs[4])
		#math_003.Value -> math_004.Value
		node_tree.links.new(math_003.outputs[0], math_004.inputs[0])
		#alpha_004.Value -> math_004.Value
		node_tree.links.new(alpha_004.outputs[0], math_004.inputs[1])
		#mix_003.Result -> mix_004.A
		node_tree.links.new(mix_003.outputs[2], mix_004.inputs[6])
		#alpha_004.Value -> mix_004.Factor
		node_tree.links.new(alpha_004.outputs[0], mix_004.inputs[0])
		#group_input.Replace Color -> mix_004.B
		node_tree.links.new(group_input.outputs[17], mix_004.inputs[7])
		#color_key_004.Matte -> alpha_005.Value
		node_tree.links.new(color_key_004.outputs[1], alpha_005.inputs[1])
		#group_input.Image -> color_key_004.Image
		node_tree.links.new(group_input.outputs[0], color_key_004.inputs[0])
		#group_input.Key Color -> color_key_004.Key Color
		node_tree.links.new(group_input.outputs[21], color_key_004.inputs[1])
		#group_input.Hue -> color_key_004.Hue
		node_tree.links.new(group_input.outputs[23], color_key_004.inputs[2])
		#group_input.Saturation -> color_key_004.Saturation
		node_tree.links.new(group_input.outputs[24], color_key_004.inputs[3])
		#group_input.Value -> color_key_004.Value
		node_tree.links.new(group_input.outputs[25], color_key_004.inputs[4])
		#reroute.Output -> alpha_005.Value
		node_tree.links.new(reroute.outputs[0], alpha_005.inputs[0])
		#color_key_005.Matte -> alpha_006.Value
		node_tree.links.new(color_key_005.outputs[1], alpha_006.inputs[1])
		#group_input.Image -> color_key_005.Image
		node_tree.links.new(group_input.outputs[0], color_key_005.inputs[0])
		#group_input.Key Color -> color_key_005.Key Color
		node_tree.links.new(group_input.outputs[26], color_key_005.inputs[1])
		#group_input.Hue -> color_key_005.Hue
		node_tree.links.new(group_input.outputs[28], color_key_005.inputs[2])
		#group_input.Saturation -> color_key_005.Saturation
		node_tree.links.new(group_input.outputs[29], color_key_005.inputs[3])
		#group_input.Value -> color_key_005.Value
		node_tree.links.new(group_input.outputs[30], color_key_005.inputs[4])
		#reroute.Output -> alpha_006.Value
		node_tree.links.new(reroute.outputs[0], alpha_006.inputs[0])
		#color_key_006.Matte -> alpha_007.Value
		node_tree.links.new(color_key_006.outputs[1], alpha_007.inputs[1])
		#group_input.Image -> color_key_006.Image
		node_tree.links.new(group_input.outputs[0], color_key_006.inputs[0])
		#group_input.Key Color -> color_key_006.Key Color
		node_tree.links.new(group_input.outputs[31], color_key_006.inputs[1])
		#group_input.Hue -> color_key_006.Hue
		node_tree.links.new(group_input.outputs[33], color_key_006.inputs[2])
		#group_input.Saturation -> color_key_006.Saturation
		node_tree.links.new(group_input.outputs[34], color_key_006.inputs[3])
		#group_input.Value -> color_key_006.Value
		node_tree.links.new(group_input.outputs[35], color_key_006.inputs[4])
		#reroute.Output -> alpha_007.Value
		node_tree.links.new(reroute.outputs[0], alpha_007.inputs[0])
		#color_key_007.Matte -> alpha_008.Value
		node_tree.links.new(color_key_007.outputs[1], alpha_008.inputs[1])
		#group_input.Image -> color_key_007.Image
		node_tree.links.new(group_input.outputs[0], color_key_007.inputs[0])
		#group_input.Key Color -> color_key_007.Key Color
		node_tree.links.new(group_input.outputs[36], color_key_007.inputs[1])
		#group_input.Hue -> color_key_007.Hue
		node_tree.links.new(group_input.outputs[38], color_key_007.inputs[2])
		#group_input.Saturation -> color_key_007.Saturation
		node_tree.links.new(group_input.outputs[39], color_key_007.inputs[3])
		#group_input.Value -> color_key_007.Value
		node_tree.links.new(group_input.outputs[40], color_key_007.inputs[4])
		#mix_004.Result -> mix_005.A
		node_tree.links.new(mix_004.outputs[2], mix_005.inputs[6])
		#alpha_005.Value -> mix_005.Factor
		node_tree.links.new(alpha_005.outputs[0], mix_005.inputs[0])
		#group_input.Replace Color -> mix_005.B
		node_tree.links.new(group_input.outputs[22], mix_005.inputs[7])
		#mix_005.Result -> mix_006.A
		node_tree.links.new(mix_005.outputs[2], mix_006.inputs[6])
		#alpha_006.Value -> mix_006.Factor
		node_tree.links.new(alpha_006.outputs[0], mix_006.inputs[0])
		#group_input.Replace Color -> mix_006.B
		node_tree.links.new(group_input.outputs[27], mix_006.inputs[7])
		#mix_006.Result -> mix_007.A
		node_tree.links.new(mix_006.outputs[2], mix_007.inputs[6])
		#alpha_007.Value -> mix_007.Factor
		node_tree.links.new(alpha_007.outputs[0], mix_007.inputs[0])
		#group_input.Replace Color -> mix_007.B
		node_tree.links.new(group_input.outputs[32], mix_007.inputs[7])
		#mix_007.Result -> mix_008.A
		node_tree.links.new(mix_007.outputs[2], mix_008.inputs[6])
		#group_input.Replace Color -> mix_008.B
		node_tree.links.new(group_input.outputs[37], mix_008.inputs[7])
		#alpha_008.Value -> mix_008.Factor
		node_tree.links.new(alpha_008.outputs[0], mix_008.inputs[0])
		#reroute.Output -> alpha_008.Value
		node_tree.links.new(reroute.outputs[0], alpha_008.inputs[0])
		#math_004.Value -> math_005.Value
		node_tree.links.new(math_004.outputs[0], math_005.inputs[0])
		#alpha_005.Value -> math_005.Value
		node_tree.links.new(alpha_005.outputs[0], math_005.inputs[1])
		#math_005.Value -> math_006.Value
		node_tree.links.new(math_005.outputs[0], math_006.inputs[0])
		#alpha_006.Value -> math_006.Value
		node_tree.links.new(alpha_006.outputs[0], math_006.inputs[1])
		#math_006.Value -> math_007.Value
		node_tree.links.new(math_006.outputs[0], math_007.inputs[0])
		#alpha_007.Value -> math_007.Value
		node_tree.links.new(alpha_007.outputs[0], math_007.inputs[1])
		#math_007.Value -> math_008.Value
		node_tree.links.new(math_007.outputs[0], math_008.inputs[0])
		#alpha_008.Value -> math_008.Value
		node_tree.links.new(alpha_008.outputs[0], math_008.inputs[1])
		#separate_color.Alpha -> reroute.Input
		node_tree.links.new(separate_color.outputs[3], reroute.inputs[0])
		#group_input.Image -> separate_color.Image
		node_tree.links.new(group_input.outputs[0], separate_color.inputs[0])
		return node_tree
