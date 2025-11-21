import bpy
from ..defs import *
from .node_data import *

class Output_Props(bpy.types.PropertyGroup):
	def get_name(self):
		return self.get("name", "")

	def set_name(self, value):
		if value == '':
			value = self.type

		# Define props
		context = bpy.context
		props = context.scene.compositor_layer_props

		# Check existing layer
		existing_names = [item.name for item in props.output if item.name != self.sub_name]

		new_name = unique_name(value, existing_names)

		self["name"] = new_name

	def update_name(self, context):
		tree = get_scene_tree(context)
		node = tree.nodes.get(self.sub_name)
		if node:
			node.name = self.name
			self.sub_name = self.name

	def composite_item(self, context):
		list = []
		i = 0
		list.append(('Default', 'Default', '', 'BLANK1', i))

		for item in get_scene_compositor(context):
			i += 1
			list.append((item, item, '', "NODE_COMPOSITING", i))
		return list
	
	def update_composite(self, context):
		tree = get_scene_tree(context)
		node = tree.nodes.get(self.name)
		output_node = tree.nodes.get(self.composite)
		if output_node:
			output = get_outputs(output_node, None)
			tree.links.new(output, node.inputs[0])

	name : bpy.props.StringProperty(name='Output Name', update=update_name, get=get_name, set=set_name)
	sub_name : bpy.props.StringProperty()
	composite : bpy.props.EnumProperty(
						name='Composite',
						items = composite_item,
						update=update_composite,
						description = "Select Compositor"
								)
	type : bpy.props.StringProperty()
	icon : bpy.props.StringProperty()

class OUTPUT_UL_LIST(bpy.types.UIList):

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		if self.layout_type in {'DEFAULT'}:
			tree = get_scene_tree(context)
			node = tree.nodes[item.name]

			row = layout.row()
			row.label(text = "", icon = item.icon)
			row.prop(item, "name", text = "", emboss = False)
			from_node = None
			for link in tree.links:
				if link.to_node == node:
					from_node = link.from_node
					break

			if not from_node:
				row.label(text="No output", icon="CANCEL")
			else:
				if item.type == 'COMPOSITE':
					row.label(text=from_node.name, icon = "SCENE")
				elif item.type == 'OUTPUT_FILE':
					if bpy.app.version < (5, 0, 0):
						row.label(text=f"{len(node.file_slots)} Inputs", icon = "SCENE")
					else:
						row.label(text=f"{len(node.inputs)-1} Inputs", icon = "SCENE")

		return
	
class FILE_OUTPUT_UL_LIST(bpy.types.UIList):

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		if self.layout_type in {'DEFAULT'}:
			addon_prefs = get_addon_preference(context)
			tree = get_scene_tree(context)
			props = context.scene.compositor_layer_props
			output = props.output[props.output_index]
			output_node = tree.nodes[output.name]
			
			row = layout.row()
			if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
				row.prop(item, "name", text="", icon = socket_data[item.socket_type], emboss = False)
			else:
				row.prop(item, "path", text = "", emboss = False)

			from_node = None
			for link in tree.links:
				if link.to_socket == output_node.inputs[index]:
					from_node = link.from_node
					break

			if not from_node:
				row.label(text="No output", icon="CANCEL")
			else:
				parts = from_node.name.split('.')  # Split the name based on the period
				name = '.'.join(parts[:-1])  # Join the first two parts
				
				if from_node.name in get_scene_compositor(context):
					row.label(text=name, icon = "NODE_COMPOSITING")
				elif from_node.name.endswith(".Mix"):
					row.label(text='Compositor', icon = "NODE_COMPOSITING")
				else:
					row.label(text=name, icon = "NODE")

			if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
				link = row.operator("scene.comp_link_layer_file_output", text="", icon='NODETREE', emboss=False)
				link.name = output.name
				link.index = index
			else:
				link = row.operator("scene.comp_link_file_output", text="", icon='NODETREE', emboss=False)
				link.name = output.name
				link.index = index
		return
	
class Add_OT_Output(bpy.types.Operator):
	bl_idname = "scene.comp_add_output"
	bl_label = "Add Compositor Output"
	bl_description = "Add Compositor Output"
	bl_options = {'REGISTER', 'UNDO'}

	type : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props
		GroupOutput = tree.nodes.get("Group Output")

		# Set new output node location next to the last output node
		sub_node = None
		for output in reversed(props.output):
			node = tree.nodes.get(output.name)
			sub_node = node
			break

		comp_node = None
		if len(get_scene_compositor(context)) > 0:
			comp_node = tree.nodes.get(get_scene_compositor(context)[0])

		node = tree.nodes.new(self.type)
		node.name = output_node_data[self.type][0]

		if self.type == 'OUTPUT_FILE':
			bpy.ops.scene.comp_remove_file_output(name=node.name, index=0)

		if sub_node:
			node.location = (sub_node.location[0],sub_node.location[1]-350)
		elif GroupOutput:
			node.location = (GroupOutput.location[0],GroupOutput.location[1]-350)
		elif comp_node:
			node.location = (comp_node.location[0]+350,comp_node.location[1])

		# Set properties
		item = props.output.add()
		item.name = node.name
		item.sub_name = node.name
		item.type = node.type
		item.icon = output_node_data[self.type][1]

		props.output_index = len(props.output) - 1

		return {"FINISHED"}

class Reload_OT_Output(bpy.types.Operator):
	bl_idname = "scene.comp_reload_output"
	bl_label = "Reload Compositor Output"
	bl_description = "Reload Compositor Output"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		# Define props
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props
		index = props.output_index
		data = {}

		for item in props.output:
			data[item.name] = item.composite

		props.output.clear()

		for node in tree.nodes:
			if node.bl_idname not in output_node_data:
				continue

			item = props.output.add()
			item.name = node.name
			item.sub_name = node.name
			item.type = node.type
			item.icon = output_node_data[node.bl_idname][1]
			if data.get(node.name):
				item.composite = data[item.name]

		props.output_index = index

		return {"FINISHED"}

class Remove_OT_Output(bpy.types.Operator):
	bl_idname = "scene.comp_remove_output"
	bl_label = "Remove Compositor Output"
	bl_description = "Remove Compositor Output"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props

		item = props.output[self.index]

		group_node = tree.nodes.get(item.name)
		if group_node:
			tree.nodes.remove(group_node)

		props.output.remove(self.index)
		if props.output_index != 0 :
			props.output_index -= 1

		bpy.ops.scene.comp_reload_output()

		return {"FINISHED"}

class Add_OT_FileOutput(bpy.types.Operator):
	bl_idname = "scene.comp_add_file_output"
	bl_label = "Add Compositor File Output"
	bl_options = {'REGISTER', 'UNDO'}

	def compositor_item(self, context):
		list = []
		for i, item in enumerate(get_scene_compositor(context)):
			list.append((item, item, '', "NODE_COMPOSITING", i))
		return list

	name : bpy.props.StringProperty(options={'HIDDEN'})

	comp : bpy.props.EnumProperty(
							name='Compositor Layer Panel',
							items = compositor_item
							)

	def invoke(self, context, event):
		if len(get_scene_compositor(context)) > 0:
			return context.window_manager.invoke_props_dialog(self)
		else:
			return self.execute(context)

	def draw(self, context):
		tree = get_scene_tree(context)
		layout = self.layout
		layout.prop(self, "comp", text="")

	def execute(self, context):
		tree = get_scene_tree(context)
		links = tree.links
		output = tree.nodes.get(self.name)
		comp = tree.nodes.get(self.comp)

		if comp:
			output.file_slots.new(comp.name)
			slot =output.file_slots[output.active_input_index]
			links.new(comp.outputs[0], output.inputs[slot.path])
		else:
			output.file_slots.new('image')

		return {'FINISHED'}
	
class Remove_OT_FileOutput(bpy.types.Operator):
	bl_idname = "scene.comp_remove_file_output"
	bl_label = "Remove Compositor File Output"
	bl_options = {'REGISTER', 'UNDO'}

	name : bpy.props.StringProperty(options={'HIDDEN'})
	index  : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		tree = get_scene_tree(context)
		output = tree.nodes.get(self.name)

		output.file_slots.remove(output.inputs[self.index])

		if output.active_input_index > 0 and output.active_input_index == len(output.file_slots):
			output.active_input_index -= 1

		return {'FINISHED'}

class Link_OT_FileOutput(bpy.types.Operator):
	bl_idname = "scene.comp_link_file_output"
	bl_label = "Link Compositor File Output"
	bl_options = {'REGISTER', 'UNDO'}

	def compositor_item(self, context):
		list = []
		for i, item in enumerate(get_scene_compositor(context)):
			list.append((item, item, '', "NODE_COMPOSITING", i))
		return list
	
	index : bpy.props.IntProperty(options={'HIDDEN'})

	name : bpy.props.StringProperty(options={'HIDDEN'})

	comp : bpy.props.EnumProperty(
							name='Compositor Layer Panel',
							items = compositor_item
							)

	def invoke(self, context, event):
		if len(get_scene_compositor(context)) > 0:
			return context.window_manager.invoke_props_dialog(self)
		else:
			return self.execute(context)

	def draw(self, context):
		tree = get_scene_tree(context)
		layout = self.layout
		layout.prop(self, "comp", text="")

	def execute(self, context):
		tree = get_scene_tree(context)
		links = tree.links
		output = tree.nodes.get(self.name)
		comp = tree.nodes.get(self.comp)

		if comp:
			links.new(comp.outputs[0], output.inputs[self.index])

		return {'FINISHED'}

class Link_Layer_OT_FileOutput(bpy.types.Operator):
	bl_idname = "scene.comp_link_layer_file_output"
	bl_label = "Link Compositor File Output"
	bl_options = {'REGISTER', 'UNDO'}

	def link_item(self, context):
		tree = get_scene_tree(context)
		addon_prefs = get_addon_preference(context)
		props = context.scene.compositor_layer_props

		if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
			node_group = bpy.data.node_groups[props.compositor_panel]
		else:
			node_group = tree.nodes[props.compositor_panel].node_tree

		compositor = node_group.compositor_props
		list = []
		list.append((' ', 'Compositor', '', 'NODE_COMPOSITING', 0))
		for i, item in enumerate(compositor.layer):
			list.append((item.name, item.name, '', item.icon, i+1))
		return list
	
	index : bpy.props.IntProperty(options={'HIDDEN'})

	name : bpy.props.StringProperty(options={'HIDDEN'})

	link : bpy.props.EnumProperty(
							name='Link',
							items = link_item
							)

	def invoke(self, context, event):
		if len(get_scene_compositor(context)) > 0:
			return context.window_manager.invoke_props_dialog(self)
		else:
			return self.execute(context)

	def draw(self, context):
		layout = self.layout
		layout.prop(self, "link", text="")

	def execute(self, context):
		tree = get_scene_tree(context)
		links = tree.links
		output = tree.nodes.get(self.name)
		if self.link != ' ':
			if tree.nodes.get(f"{self.link}.Set_Matte"):
				link = tree.nodes.get(f"{self.link}.Set_Matte")
			else:
				link = tree.nodes.get(f"{self.link}.Transform")

			links.new(link.outputs[0], output.inputs[self.index])
		else:
			addon_prefs = get_addon_preference(context)
			props = context.scene.compositor_layer_props
			if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
				node_group = bpy.data.node_groups[props.compositor_panel]
			else:
				node_group = tree.nodes[props.compositor_panel].node_tree

			compositor = node_group.compositor_props.layer[-1].name

			link = tree.nodes.get(f"{compositor}.Mix")
			
			links.new(link.outputs['Result'], output.inputs[self.index])

		return {'FINISHED'}

class Add_Slot_OT_FileOutput(bpy.types.Operator):
	bl_idname = "scene.comp_add_slot_file_output"
	bl_label = "Add Slot Compositor File Output"
	bl_options = {'REGISTER', 'UNDO'}

	def link_item(self, context):
		tree = get_scene_tree(context)
		addon_prefs = get_addon_preference(context)
		props = context.scene.compositor_layer_props

		if bpy.app.version >= (5, 0, 0) and addon_prefs.compositor_type == '5.0':
			node_group = bpy.data.node_groups[props.compositor_panel]
		else:
			node_group = tree.nodes[props.compositor_panel].node_tree

		compositor = node_group.compositor_props
		list = []
		list.append((' ', 'Compositor', '', 'NODE_COMPOSITING', 0))
		for i, item in enumerate(compositor.layer):
			list.append((item.name, item.name, '', item.icon, i+1))
		return list

	name : bpy.props.StringProperty(options={'HIDDEN'})

	link : bpy.props.EnumProperty(
							name='Link',
							items = link_item
							)

	def invoke(self, context, event):
		return context.window_manager.invoke_props_dialog(self)

	def execute(self, context):
		tree = get_scene_tree(context)
		node = tree.nodes.get(self.name)
		if self.link == ' ':
			name = "Compositor"
		else:
			name = self.link
		node.file_output_items.new('RGBA', name)
		bpy.ops.scene.comp_link_layer_file_output(name=self.name, link=self.link, index=-2)
		return {'FINISHED'}

class Remove_Slot_OT_FileOutput(bpy.types.Operator):
	bl_idname = "scene.comp_remove_slot_file_output"
	bl_label = "Remove Slot Compositor File Output"
	bl_options = {'REGISTER', 'UNDO'}

	name : bpy.props.StringProperty(options={'HIDDEN'})
	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		tree = get_scene_tree(context)
		node = tree.nodes.get(self.name)
		item = node.file_output_items[self.index]
		node.file_output_items.remove(item)
		return {'FINISHED'}

class COMPOSITOR_MT_add_output(bpy.types.Menu):
	bl_label = "Output"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout

		for data in output_node_data:
			layout.operator("scene.comp_add_output", text=output_node_data[data][0], icon=output_node_data[data][1]).type = data

def draw_format(layout, props):
	layout.use_property_split = True
	layout.use_property_decorate = False
	if bpy.app.version >= (4, 4, 0):
		layout.prop(props, "save_as_render")
	col = layout.column()
	col.prop(props.format, "file_format")
	col.row().prop(props.format, "color_mode", text="Color", expand = True)
	col.row().prop(props.format, "color_depth", expand = True)
	col.prop(props.format, "compression")
	layout.row().prop(props.format, "color_management", expand = True)
	col = layout.column()
	col.active = props.format.color_management == 'OVERRIDE'
	col.prop(props.format.display_settings, "display_device")
	col.prop(props.format.view_settings, "view_transform")
	col.prop(props.format.view_settings, "look")
	col.prop(props.format.view_settings, "exposure")
	col.prop(props.format.view_settings, "gamma")
	col.prop(props.format.view_settings, "use_curve_mapping")
	if props.format.view_settings.use_curve_mapping:
		col.template_curve_mapping(props.format.view_settings, "curve_mapping", type='COLOR', levels=True)
	col.prop(props.format.view_settings, "use_white_balance")
	if props.format.view_settings.use_white_balance:
		col.prop(props.format.view_settings, "white_balance_temperature")
		col.prop(props.format.view_settings, "white_balance_tint")

def draw_output(self, context, box):
	addon_prefs = get_addon_preference(context)
	tree = get_scene_tree(context)
	props = context.scene.compositor_layer_props

	if bpy.app.version < (5, 0, 0):
		box.operator("wm.call_menu", text="Add Output", icon='ADD').name = "COMPOSITOR_MT_add_output"
	else:
		box.operator("scene.comp_add_output", text="Add Output", icon='ADD').type = 'CompositorNodeOutputFile'
		
	box.template_list("OUTPUT_UL_LIST", "", props, "output", props, "output_index")
	if len(props.output) > 0:
		item = props.output[props.output_index]
		node = tree.nodes[item.name]

		row = box.row(align=True)
		row.label(text="", icon = item.icon)
		row.prop(item, 'name', text="")
		row.operator("scene.comp_remove_output", text="", icon='X').index = props.output_index

		if item.type == 'COMPOSITE':
			from_node = None
			for link in tree.links:
				if link.to_node == node:
					from_node = link.from_node
					break
			box.prop(item, 'composite', text="")
			if from_node:
				if from_node.name != item.composite or item.composite == "Default":
					box.label(text=from_node.name, icon="NODE")
				if item.composite != "Default" and from_node.name != item.composite:
					box.label(text="Composite is not connecting compositor", icon="ERROR")
			else:
				box.label(text="Composite is not connected", icon="CANCEL")

		elif item.type == 'OUTPUT_FILE':
			if bpy.app.version < (5, 0, 0):
				col = box.column()
				col.label(text = "Base Path")
				col.prop(node, "base_path", text="")

				draw_format(box, node)

				box.operator("scene.comp_add_file_output", text="Add Input", icon='ADD').name = node.name
				sub = box.row()
				sub.template_list("FILE_OUTPUT_UL_LIST", "", node, "file_slots", node, "active_input_index")

				if len(node.file_slots) > 0:

					slot = node.file_slots[node.active_input_index]
					col = box.column()
					col.label(text="File Subpath")
					sub = col.row(align=True)
					sub.prop(slot, 'path', text="")
					remove = sub.operator("scene.comp_remove_file_output", text="", icon='X')
					remove.name = node.name
					remove.index = node.active_input_index

					col = box.column()
					col.use_property_split = False
					col.prop(slot, "use_node_format")
					if bpy.app.version < (4, 4, 0):
						col.prop(slot, "save_as_render")
					if not slot.use_node_format:
						draw_format(box, slot)
			else:
				col = box.column()
				col.prop(node, "directory", text="")
				col.prop(node, "file_name", text="")
				box.row().prop(node.format, "media_type", expand = True)
				box.separator()
				box.use_property_split = True
				box.use_property_decorate = False
				if node.format.media_type == "IMAGE":
					col = box.column()
					if bpy.app.version >= (4, 4, 0):
						box.prop(node, "save_as_render")
					col = box.column()
					col.prop(node.format, "file_format")
					col.row().prop(node.format, "color_mode", text="Color", expand = True)
					col.row().prop(node.format, "color_depth", expand = True)
					col.prop(node.format, "compression")
					if node.save_as_render:
						box.row().prop(node.format, "color_management", expand = True)
						col = box.column()
						col.active = node.format.color_management == 'OVERRIDE'
						col.prop(node.format.display_settings, "display_device")
						col.prop(node.format.view_settings, "view_transform")
						col.prop(node.format.view_settings, "look")
						col.prop(node.format.view_settings, "exposure")
						col.prop(node.format.view_settings, "gamma")
						col.prop(node.format.view_settings, "use_curve_mapping")
						if node.format.view_settings.use_curve_mapping:
							col.template_curve_mapping(node.format.view_settings, "curve_mapping", type='COLOR', levels=True)
						col.prop(node.format.view_settings, "use_white_balance")
						if node.format.view_settings.use_white_balance:
							col.prop(node.format.view_settings, "white_balance_temperature")
							col.prop(node.format.view_settings, "white_balance_tint")

				elif node.format.media_type == 'MULTI_LAYER_IMAGE':
					col = box.column()
					col.use_property_split = True
					col.use_property_decorate = False
					col.prop(node, "save_as_render")
					col.row().prop(node.format, "color_depth", expand = True)
					col.prop(node.format, "exr_codec")
					col.prop(node.format, "use_exr_interleave")
					col.row().prop(node.format, "color_management", text="Color Space", expand = True)
					if node.format.color_management == 'OVERRIDE':
						col.prop(node.format.linear_colorspace_settings, "name", text="Color Space")

				if addon_prefs.compositor_type == '5.0':
					sub = box.row()
					sub.template_list("FILE_OUTPUT_UL_LIST", "", node, "file_output_items", node, "active_item_index")

					colsub = sub.column(align=True)

					xcolsub = colsub.split(align=True)
					xcolsub.enabled = bool(len(get_scene_compositor(context)))
					add = xcolsub.operator("scene.comp_add_slot_file_output", text="", icon='ADD')
					add.name = node.name

					xcolsub = colsub.split(align=True)
					xcolsub.enabled = bool(len(node.file_output_items) > 0)
					
					x = xcolsub.operator("scene.comp_remove_slot_file_output", text="", icon='X')
					x.name = node.name
					x.index = node.active_item_index
					if len(node.file_output_items) > 0:
						slot = node.file_output_items[node.active_item_index]
						col = box.column()
						col.prop(slot, "socket_type")
						if slot.socket_type == "VECTOR":
							col.prop(slot, "vector_socket_dimensions")

						if node.format.media_type == "IMAGE":
							col.prop(slot, "override_node_format")
							if slot.override_node_format:
								draw_format(box, slot)
					

classes = (
	Output_Props,
	OUTPUT_UL_LIST,
	FILE_OUTPUT_UL_LIST,
	Add_OT_Output,
	Reload_OT_Output,
	Remove_OT_Output,
	Add_OT_FileOutput,
	Remove_OT_FileOutput,
	Link_OT_FileOutput,
	Link_Layer_OT_FileOutput,
	Add_Slot_OT_FileOutput,
	Remove_Slot_OT_FileOutput,
	COMPOSITOR_MT_add_output,
		  )

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)