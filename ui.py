import bpy
from .defs import *
from .unity import source, compositor, output, layer

class Compositor_Layer:
	def draw(self, context):
		layout = self.layout
		box = layout.box()
		self.draw_compositor(context, box)

	def draw_compositor(self, context, box):
		scene = context.scene
		rd = context.scene.render
		props = context.scene.compositor_layer_props
		addon_prefs = get_addon_preference(context)

		row = box.row()
		sub = row.row()
		sub.label(text = "Compositing", icon = "NODE_COMPOSITING")

		if bpy.app.version < (5, 0, 0):
			if scene.use_nodes == False:
				box.prop(scene, "use_nodes", text = "Compositor Use Nodes", icon = "NODETREE", toggle = True)
				return

		if hasattr(context.space_data, 'shading'):
			row = row.row()
			row.alignment = 'RIGHT'
			if context.space_data.shading.use_compositor == "DISABLED":
				row.label(text="Compositor is disabled", icon = "ERROR")
			elif context.space_data.shading.use_compositor == "CAMERA":
				row.label(text="(Only works in camera)")

			row.popover(panel="COMPOSITOR_PT_options", text="", icon='SETTINGS')

			row = box.row()
			row.use_property_split = True
			row.use_property_decorate = False
			row.prop(context.space_data.shading, "use_compositor", expand = True)
		else:
			sub.popover(panel="COMPOSITOR_PT_options", text="", icon='SETTINGS')

		col = box.column()
		col.use_property_split = True
		col.use_property_decorate = False
		row = col.row()
		row.prop(rd, "compositor_device", text="Device", expand=True)
		col.prop(rd, "compositor_precision", text="Precision")

		row = box.row()
		row.prop(props, "panel", expand=True)

		if props.panel == 'Source':
			source.draw_source(self, context, box)
		elif props.panel == 'Compositor':
			compositor.draw_compositor(self, context, box)
			if len(get_scene_compositor(context)) > 0:
				layer.draw_layer(self, context, box)
		elif props.panel == 'Output':
			output.draw_output(self, context, box)

		if context.area.ui_type == 'CompositorNodeTree':
			if addon_prefs.active_node_panel:
				node = context.active_node
				if node:
					header, panel = self.layout.panel(idname="Active Node", default_closed=True)
					header.label(text="Active Node", icon='NODE')
					header.operator("node.nw_reset_nodes", text="", icon='FILE_REFRESH', emboss = False)
					if panel:
						xbox = panel.box()
						col = xbox.column()
						col.use_property_split = True
						col.use_property_decorate = False
						sub = col.row()
						sub.enabled = False 
						sub.prop(node, "name", text = "Name")
						col.prop(node, "label", text = "Label")
						xbox.template_node_inputs(node)
		
		if addon_prefs.preset_panel:
			header, panel = self.layout.panel(idname="Presets", default_closed=True)
			header.label(text="Presets", icon='PRESET')

			if panel:
				xbox = panel.box()

				if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
					type = "Effects"
				else:
					row = xbox.row(align=True)
					row.prop(addon_prefs, 'preset_type', expand=True)
					row.menu("COMPOSITOR_MT_preset_specials", icon='DOWNARROW_HLT', text="")
					type = addon_prefs.preset_type
				
				col = xbox.column()
				row = col.row(align=True)
				row.operator("scene.comp_new_preset", text="Create New Preset", icon='ADD').type = type
				if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
					row.menu("COMPOSITOR_MT_preset_specials", icon='DOWNARROW_HLT', text="")
				if context.area.ui_type == 'CompositorNodeTree' and type == 'Effects':
					col.operator("scene.comp_save_preset", text='Save selected as preset', icon = "FILE_TICK").type = type
				if type == 'Compositors':
					col.operator("scene.comp_save_preset", text='Save current comp as preset', icon = "FILE_TICK").type = type

				presets = get_presets(type)
				if len(presets) > 0:
					col = xbox.column()
					for preset in presets:
						header, panel = col.panel(idname=f"{preset}.presets", default_closed=True)
						header.label(text=preset)
						remove = header.operator("scene.comp_remove_preset", text='', icon = "X", emboss=False)
						remove.type = type
						remove.name = preset
						if panel:
							items = get_presets_item(preset, type)
							panel_box = panel.box()
							if len(items) > 0:
								sub = panel_box.column()
								for item in items:
									if not item.startswith(".*"):
										row = sub.row()
										if type == "Compositors":
											add = row.operator("scene.comp_apply_preset_item", text='', icon = "ADD", emboss=False)
											add.preset = preset
											add.target = item
										row.label(text=item, icon = "SHADERFX" if type == 'Effects' else "NODE_COMPOSITING")
										remove = row.operator("scene.comp_remove_preset_item", text='', icon = "REMOVE", emboss=False)
										remove.preset = preset
										remove.target = item
										remove.type = type
							else:
								panel_box.label(text="Preset has item", icon = "FILEBROWSER")
				else:
					xbox.label(text="No Presets", icon = "FILEBROWSER")

class NODE_PT_Compositor_Layer(bpy.types.Panel, Compositor_Layer):
	bl_space_type = 'NODE_EDITOR'
	bl_region_type = 'UI'
	bl_idname = "NODE_PT_Compositor_Layer"
	bl_label = "Layer Comp"
	bl_category = "Layer Comp"

	@classmethod
	def poll(cls, context):
		if bpy.app.version >= (5, 0, 0) and context.space_data.node_tree_sub_type != 'SCENE':
			return False
		return context.area.ui_type == 'CompositorNodeTree'

class VIEW_PT_Compositor_Layer(bpy.types.Panel, Compositor_Layer):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = "Layer Comp"
	bl_idname = "VIEW_PT_Compositor_Layer"
	bl_category = "Layer Comp"

	@classmethod
	def poll(cls, context):
		addon_prefs = get_addon_preference(context)
		return addon_prefs.view3d

class COMPOSITOR_PT_options(bpy.types.Panel):
	bl_space_type = 'NODE_EDITOR'
	bl_region_type = 'HEADER'
	bl_label = "Options"
	bl_ui_units_x = 14

	def draw(self, context):
		addon_prefs = get_addon_preference(context)

		layout = self.layout
		layout.label(text="User Interface")
		layout.use_property_split = True
		layout.use_property_decorate = False
		if bpy.app.version >= (5, 0, 0):
			layout.row().prop(addon_prefs, "compositor_type", text="Compositor", expand = True)
			
		col = layout.column(heading="Panel", align=True)
		col.prop(addon_prefs, "view3d", text="3D Viewport Panel")
		col.prop(addon_prefs, "active_node_panel", text="Active Node")
		col.prop(addon_prefs, "preset_panel", text="Presets Panel")
		col = layout.column(heading = "Compositor")
		col.prop(addon_prefs, "search", text="Search Box")
		row = col.row()
		row.prop(addon_prefs, "layer_name", text="Layer Name", expand=True)

		row = col.row(heading="Layer Display", align=True)
		row.prop(addon_prefs, "label", text="Label", toggle = True)
		row.prop(addon_prefs, "fx_toggle", text="FX", toggle = True)
		row.prop(addon_prefs, "blend_mode", text="Blend", toggle = True)
		row.prop(addon_prefs, "mix", text="Mix", toggle = True)
		col = layout.column(heading="Properties", align=True)
		row = col.row()
		row.prop(addon_prefs, "panel_type", text="Panel Type", expand=True)
		layout.label(text="Operator")
		col = layout.column(heading="", align=True)
		colrow = col.row()
		colrow.active = addon_prefs.compositor_type != '5.0'
		colrow.prop(addon_prefs, "new_compositor_option", text="New Compositor", expand = True)
		col = layout.column(heading="", align=True)
		col.row().prop(addon_prefs, "duplicate_layer_option", text="Duplicate Layer", expand = True)
		col.row().prop(addon_prefs, "duplicate_effect_option", text="Effect", expand = True)

classes = (
	NODE_PT_Compositor_Layer,
	VIEW_PT_Compositor_Layer,
	COMPOSITOR_PT_options
		  )

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)