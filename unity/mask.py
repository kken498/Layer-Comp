import bpy
from ..defs import *

class Mask_Props(bpy.types.PropertyGroup):
	def get_name(self):
		return self.get("name", "")

	def set_name(self, value):
		if value == '':
			value = self.type

		# Define props
		context = bpy.context
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		# Check existing layer
		existing_names = [item.name for item in layer.mask if item.name != self.sub_name]

		new_name = unique_name(value, existing_names)

		self["name"] = new_name

	def update_name(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		mask_node = node_group.nodes.get(f'{layer.name}.Mask.{self.sub_name}')

		# Update Mask node name
		if mask_node:
			mask_node.name = f'{layer.name}.Mask.{self.name}'
			self.sub_name = self.name

	def update_hide(self, context):
		# Mute Mix node
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		node = node_group.nodes.get(f'{layer.name}.Mask.{self.name}')
		node.mute = self.hide

	name : bpy.props.StringProperty(name='Mask Name', update=update_name, get=get_name, set=set_name)
	sub_name : bpy.props.StringProperty()
	type : bpy.props.StringProperty()
	hide : bpy.props.BoolProperty(name='Hide Mask', update=update_hide)

class Add_OT_Mask(bpy.types.Operator):
	bl_idname = "scene.comp_add_mask"
	bl_label = "Add Compositor Layer Mask"
	bl_description = "Add Compositor Layer Mask"
	bl_options = {'REGISTER', 'UNDO'}

	mask_type : bpy.props.EnumProperty(default = "Ellipse",
							items = [('Box', 'Box', ''),
									('Ellipse', 'Ellipse', ''),
									],
									)

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self, width=300)

	def draw(self, context):
		layout = self.layout
		layout.label(text="Mask Type")
		layout.prop(self, "mask_type", expand = True)

	def execute(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		sub_mix_node = node_group.nodes.get(f'{layer.name}.Mix_Sub')
		math_node = node_group.nodes.get(f'{layer.name}.Mask_Mix')
		feather_node = node_group.nodes.get(f'{layer.name}.Mask_Feather')
		frame = node_group.nodes.get(f"{layer.name}.Frame")
		
		existing_names = [item.name for item in layer.mask]
		name = unique_name(self.mask_type, existing_names)

		if not math_node:
			if bpy.app.version >= (5, 0, 0):
				math_node = node_group.nodes.new('ShaderNodeMath')
			else:
				math_node = node_group.nodes.new('CompositorNodeMath')
			math_node.name = f'{layer.name}.Mask_Mix'
			math_node.operation = 'MULTIPLY'
			math_node.inputs[0].default_value = 1
			math_node.inputs[1].default_value = 1
			math_node.parent = frame
			math_node.location = (sub_mix_node.location[0]-150, sub_mix_node.location[1])
			if bpy.app.version >= (4, 5, 0):
				node_group.links.new(math_node.outputs[0], sub_mix_node.inputs[3])
			elif bpy.app.version < (4, 5, 0):
				node_group.links.new(math_node.outputs[0], sub_mix_node.inputs[2])

		if not feather_node:
			feather_node = node_group.nodes.new("CompositorNodeBlur")
			feather_node.name = f'{layer.name}.Mask_Feather'
			if bpy.app.version >= (5, 0, 0):
				feather_node.inputs[2].default_value = 'Fast Gaussian'
				feather_node.inputs[3].default_value = True

			else:
				feather_node.filter_type = 'FAST_GAUSS'
				if bpy.app.version >= (4, 5, 0):
					feather_node.inputs[2].default_value = True
				elif bpy.app.version < (4, 5, 0):
					feather_node.size_x = 500
					feather_node.size_y = 500
					feather_node.use_extended_bounds = True
					feather_node.inputs[1].default_value = 0
			feather_node.parent = frame
			feather_node.location = (math_node.location[0]-150, math_node.location[1]+150)
			node_group.links.new(feather_node.outputs[0], math_node.inputs[0])

		if self.mask_type == "Box":
			mask_node = node_group.nodes.new("CompositorNodeBoxMask")
		else:
			mask_node = node_group.nodes.new("CompositorNodeEllipseMask")

		mask_node.name = f'{layer.name}.Mask.{name}'
		mask_node.parent = frame

		if bpy.app.version >= (4, 5, 0):
			mask_node.inputs[3].default_value[0] = 1
			mask_node.inputs[3].default_value[1] = 0.55
		if bpy.app.version < (4, 5, 0):
			mask_node.mask_width = 1
			mask_node.mask_height = 0.55

		if len(layer.mask) > 0:
			sub_node = node_group.nodes.get(f'{layer.name}.Mask.{layer.mask[-1].name}')
			if sub_node:
				mask_node.location = sub_node.location.copy()
				node_group.links.new(mask_node.outputs[0], sub_node.inputs['Mask'])
				offset_node(node_group, mask_node, 'X', 150)
		else:
			mask_node.location = (feather_node.location[0]-150, feather_node.location[1]+150)
			node_group.links.new(mask_node.outputs[0], feather_node.inputs[0])

		item = layer.mask.add()
		item.name = name
		item.sub_name = name
		item.type = self.mask_type
		return {"FINISHED"}

class Remove_OT_Mask(bpy.types.Operator):
	bl_idname = "scene.comp_remove_mask"
	bl_label = "Remove Compositor Layer Mask"
	bl_description = "Remove Compositor Layer Mask"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		mask = layer.mask[self.index]

		# Define nodes
		mask_node = node_group.nodes.get(f'{layer.name}.Mask.{mask.name}')

		# Offset nodes
		offset_node(node_group, mask_node, 'X', -150)

		input_socket = None
		output_socket = None

		for link in node_group.links:
			if link.to_socket == mask_node.inputs[0]:
				input_socket = link.from_socket
				break
		for link in node_group.links:
			if link.from_socket == mask_node.outputs[0]:
				output_socket = link.to_socket
				break
		if input_socket and output_socket:
			node_group.links.new(input_socket, output_socket)

		# Remove nodes
		node_group.nodes.remove(mask_node)
		if len(layer.mask) == 1:
			node_group.nodes.remove(node_group.nodes.get(f'{layer.name}.Mask_Feather'))

		# Remove propterties
		layer.mask.remove(self.index)
	
		return {"FINISHED"}

class Clear_OT_Mask(bpy.types.Operator):
	bl_idname = "scene.comp_clear_mask"
	bl_label = "Clear Compositor Layer Mask"
	bl_description = "Clear Compositor Layer Mask"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		return len(layer.mask) > 0
	
	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		for i in range(len(layer.mask)):
			bpy.ops.scene.comp_remove_mask(index=0)

		return {"FINISHED"}

class Duplicate_OT_Mask(bpy.types.Operator):
	bl_idname = "scene.comp_duplicate_mask"
	bl_label = "Duplicate Compositor Layer Mask"
	bl_description = "Duplicate Compositor Layer Mask"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		mask = layer.mask[self.index]

		# Define nodes
		mask_node = node_group.nodes.get(f'{layer.name}.Mask.{mask.name}')

		bpy.ops.scene.comp_add_mask(mask_type=mask.type)
	
		new_mask = layer.mask[len(layer.mask)-1]
		new_mask_node = node_group.nodes.get(f'{layer.name}.Mask.{new_mask.name}')

		convert_node_data(mask_node, new_mask_node)

		return {"FINISHED"}

class Copy_OT_Mask(bpy.types.Operator):
	bl_idname = "scene.comp_copy_mask"
	bl_label = "Copy Compositor Layer Mask"
	bl_description = "Copy Compositor Layer Mask"
	bl_options = {'REGISTER', 'UNDO'}

	def compositor_item(self, context):
		addon_prefs = get_addon_preference(context)
		tree = get_scene_tree(context)
		list = []
		for i, name in enumerate(get_scene_compositor(context)):
			if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
				node_group = bpy.data.node_groups[name]
			else:
				node_group = tree.nodes[name].node_tree
			compositor = node_group.compositor_props
			if compositor.layer:
				list.append((name, name, ''))
		return list
	
	def layer_item(self, context):
		tree = get_scene_tree(context)
		addon_prefs = get_addon_preference(context)
		if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
			node_group = bpy.data.node_groups[self.compositor]
		else:
			node_group = tree.nodes[self.compositor].node_tree
		compositor = node_group.compositor_props
		list = []
		for i, item in enumerate(compositor.layer):
			if item.mask:
				list.append((str(i), item.name, '', item.icon, i))
		return list
	
	def mask_item(self, context):
		tree = get_scene_tree(context)
		addon_prefs = get_addon_preference(context)
		if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
			node_group = bpy.data.node_groups[self.compositor]
		else:
			node_group = tree.nodes[self.compositor].node_tree
		compositor = node_group.compositor_props
		layer = compositor.layer[int(self.layer)]
		list = []
		if self.layer:
			if bpy.app.version >= (4, 4, 0):
				list.append(('All', 'All', '', 'STRIP_COLOR_01', 0))
			else:
				list.append(('All', 'All', '', 'SEQUENCE_COLOR_01', 0))
			for i, item in enumerate(layer.mask):
				if item.type == "Box":
					icon="OBJECT_DATAMODE"
				elif item.type == "Ellipse":
					icon="CLIPUV_HLT"
				list.append((str(i+1), item.name, '', icon, i+1))
		return list
	
	compositor : bpy.props.EnumProperty(
						name = "Compositor",
						items = compositor_item,
								)
	
	layer : bpy.props.EnumProperty(
						name = "Layer",
						items = layer_item,
								)
	
	mask : bpy.props.EnumProperty(
						name = "Mask",
						items = mask_item,
								)

	@classmethod
	def poll(cls, context):
		addon_prefs = get_addon_preference(context)
		tree = get_scene_tree(context)
		for name in get_scene_compositor(context):
			if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
				node_group = bpy.data.node_groups[name]
			else:
				node_group = tree.nodes[name].node_tree
			comp = node_group.compositor_props
			for layer in comp.layer:
				if len(layer.mask) > 0:
					return True
		return False

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def execute(self, context):
		if not (self.layer and self.mask and self.compositor):
			self.report({"INFO"}, "No mask")
			return {"FINISHED"}
		
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props

		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		addon_prefs = get_addon_preference(context)

		if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
			copy_node_group = bpy.data.node_groups[self.compositor]
		else:
			copy_node_group = tree.nodes[self.compositor].node_tree

		copy_compositor = copy_node_group.compositor_props
		copy_layer = copy_compositor.layer[int(self.layer)]

		if self.mask != 'All':
			copy_mask = copy_layer.mask[int(self.mask)-1]
			copy_mask_node = copy_node_group.nodes.get(f'{copy_layer.name}.Mask.{copy_mask.name}')

			bpy.ops.scene.comp_add_mask(mask_type=copy_mask.type)

			mask = layer.mask[-1]
			node_group = bpy.data.node_groups[compositor.name]
			new_mask_node = node_group.nodes.get(f'{layer.name}.Mask.{mask.name}')

			convert_node_data(copy_mask_node, new_mask_node)

		else:

			for copy_mask in copy_layer.mask:

				bpy.ops.scene.comp_add_mask(mask_type=copy_mask.type)

				copy_node_group = bpy.data.node_groups[copy_compositor.name]
				copy_mask_node = copy_node_group.nodes.get(f'{copy_layer.name}.Mask.{copy_mask.name}')

				mask = layer.mask[-1]
				node_group = bpy.data.node_groups[compositor.name]
				new_mask_node = node_group.nodes.get(f'{layer.name}.Mask.{mask.name}')

				convert_node_data(copy_mask_node, new_mask_node)

		return {"FINISHED"}

class COMPOSITOR_MT_masks_specials(bpy.types.Menu):
	bl_label = "Masks Specials"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		layout.operator("scene.comp_add_mask", text="Add Mask", icon='ADD')
		layout.separator()
		layout.operator("scene.comp_copy_mask", text="Copy mask from layer", icon = 'PASTEDOWN', emboss = False)
		layout.separator()
		layout.operator("scene.comp_clear_mask", text="Clear Masks", icon='TRASH', emboss = False)

def draw_mask(self, context, box):
	props = context.scene.compositor_layer_props
	node_group = bpy.data.node_groups[props.compositor_panel]
	compositor = node_group.compositor_props
	layer = compositor.layer[compositor.layer_index]

	feather_node = node_group.nodes[f'{layer.name}.Mask_Feather']

	col = box.column()
	col.use_property_split = True
	col.use_property_decorate = False
	col.prop(feather_node, "filter_type", text="Feather")
	row = col.row(align=True)
	if bpy.app.version >= (5, 0, 0):
		row.prop(feather_node.inputs[1], 'default_value', text="Size", index=0)
		row.prop(feather_node.inputs[1], 'default_value', text="", index=1)
		col.prop(feather_node.inputs[2], 'default_value', text="Type")
		col.prop(feather_node.inputs[3], 'default_value', text="Extends Bounds")
	elif bpy.app.version >= (4, 5, 0) and bpy.app.version < (5, 0, 0):
		row.prop(feather_node.inputs[1], 'default_value', text="Size", index=0)
		row.prop(feather_node.inputs[1], 'default_value', text="", index=1)
		col.prop(feather_node.inputs[2], 'default_value', text="Extends Bounds")
	elif bpy.app.version < (4, 5, 0):
		col.prop(feather_node.inputs[1], 'default_value', text="Size")
		col.prop(feather_node, 'use_extended_bounds', text="Extends Bounds")

	for i, mask in enumerate(layer.mask):
		node = node_group.nodes[f'{layer.name}.Mask.{mask.name}']
		if mask.type == "Box":
			icon="OBJECT_DATAMODE"
		elif mask.type == "Ellipse":
			icon="CLIPUV_HLT"

		header, panel = box.panel(idname=f'{layer.name}.Mask.{mask.name}', default_closed=False)
		row = header.row()
		sub = row.row(align=True)
		sub.label(text="", icon = icon)
		sub.prop(mask, "hide", text = "", icon = "HIDE_ON" if mask.hide == True else "HIDE_OFF", invert_checkbox=True)
		sub.prop(mask, "name", text = "")
		if bpy.app.version >= (5, 0, 0):
			sub.prop(node.inputs[0], 'default_value', text="")
		else:
			sub.prop(node, "mask_type", text = "")
		rest = sub.operator("scene.comp_rest_node", text="", icon='FILE_REFRESH')
		rest.node_group = node_group.name
		rest.node = node.name
		sub.operator("scene.comp_duplicate_mask", text="", icon='DUPLICATE').index = i
		sub.operator("scene.comp_remove_mask", text="", icon='X').index = i

		if panel:
			panel.use_property_split = True
			panel.use_property_decorate = False
			panel_box = panel.box()
			col = panel_box.column()
			col.use_property_split = True
			col.use_property_decorate = False
			if bpy.app.version >= (5, 0, 0):
				col.prop(node.inputs[0], 'default_value', text="Mask Type")
				if not any(link.to_node == node for link in node_group.links):
					col.prop(node.inputs[1], 'default_value', text="Mask")
				row = col.row(align=True)
				row.prop(node.inputs[3], 'default_value', text="Position", index=0)
				row.prop(node.inputs[3], 'default_value', text="", index=1)
				row = col.row(align=True)
				row.prop(node.inputs[4], 'default_value', text="Scale", index=0)
				row.prop(node.inputs[4], 'default_value', text="", index=1)
				col.prop(node.inputs[5], 'default_value', text="Rotation")
				col.prop(node.inputs[2], 'default_value', text="Value")
			elif bpy.app.version < (5, 0, 0) and bpy.app.version >= (4, 5, 0):
				col.prop(node, "mask_type", text = "Mask Type")
				if not any(link.to_node == node for link in node_group.links):
					col.prop(node.inputs[0], 'default_value', text="Mask")
				row = col.row(align=True)
				row.prop(node.inputs[2], 'default_value', text="Position", index=0)
				row.prop(node.inputs[2], 'default_value', text="", index=1)
				row = col.row(align=True)
				row.prop(node.inputs[3], 'default_value', text="Scale", index=0)
				row.prop(node.inputs[3], 'default_value', text="", index=1)
				col.prop(node.inputs[4], 'default_value', text="Rotation")
				col.prop(node.inputs[1], 'default_value', text="Value")
			elif bpy.app.version < (4, 5, 0):
				col.prop(node, "mask_type", text = "Mask Type")
				if not any(link.to_node == node for link in node_group.links):
					col.prop(node.inputs[0], 'default_value', text="Mask")
				row = col.row(align=True)
				row.prop(node, 'x', text="Position")
				row.prop(node, 'y', text="Y")
				row = col.row(align=True)
				row.prop(node, 'mask_width', text="Scale", slider=True)
				row.prop(node, 'mask_height', text="Height", slider=True)
				col.prop(node, 'rotation', text="Rotation")
				col.prop(node.inputs[1], 'default_value', text="Value")
				

classes = (
	Mask_Props,
	Add_OT_Mask,
	Remove_OT_Mask,
	Clear_OT_Mask,
	Duplicate_OT_Mask,
	Copy_OT_Mask,
	COMPOSITOR_MT_masks_specials,
		  )
		  

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)