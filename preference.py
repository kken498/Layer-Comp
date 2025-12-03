import bpy
from .defs import *

class AddonPref_Properties:
	active_node_panel : bpy.props.BoolProperty(default = True, description = "Show active node panel in compositor area.")
	preset_panel : bpy.props.BoolProperty(default = True, description = "Show effect preset panel.")
	preset_type : bpy.props.EnumProperty(default = "Effects",
							items = [('Effects', 'Effects', ''),
									('Compositors', 'Compositors', ''),
									],
							description = "Presets Type"
									)
	
	compositor_type : bpy.props.EnumProperty(default = "5.0",
							items = [('Legacy', 'Legacy', ''),
									('5.0', '5.0', ''),
									],
							description = "Compositor system type, Legacy which is using node group as a compositor. 5.0 will combine compositor node group assets. (Both cannot be used in the same project)"
									)

	layer_name : bpy.props.EnumProperty(default = "Layer",
							items = [('Layer', 'Layer', ''),
									('Source', 'Source', ''),
									],
							description = "Layer name display type."
									)
	panel_type : bpy.props.EnumProperty(default = "Expand",
							items = [('List', 'List', ''),
									('Expand', 'Expand', ''),
									],
							description = "Properties panel type."
									)
	view3d : bpy.props.BoolProperty(default = True, description = "Show Panel in 3D Viewport")

	search : bpy.props.BoolProperty(default = True, description = "Search Layer in Compositor")
	
	label : bpy.props.BoolProperty(default = True, description = "Show label icon in layer.")
	fx_toggle : bpy.props.BoolProperty(default = True, description = "Show FX toggle in layer.")
	blend_mode : bpy.props.BoolProperty(default = True, description = "Show blend mode in layer.")
	mix : bpy.props.BoolProperty(default = True, description = "Show mix in layer.")

	new_compositor_option : bpy.props.EnumProperty(default = "First",
							items = [('Never', 'Never', ''),
									('First', 'First', ''),
									('Any', 'Any', ''),
									],
							description = "New compositor will add reder layer."
									)
	
	duplicate_layer_option : bpy.props.EnumProperty(default = "Next",
							items = [('Next', 'Next', ''),
									('Top', 'Top', ''),
									],
							description = "Duplicated item position."
									)
	duplicate_effect_option : bpy.props.EnumProperty(default = "Next",
							items = [('Next', 'Next', ''),
									('Top', 'Top', ''),
									],
							description = "Duplicated item position."
									)

class AddonPreferences(bpy.types.AddonPreferences, AddonPref_Properties):
	bl_idname = __package__

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		self.draw_preferences(context, col)

	def draw_preferences(self, context, col):
		row = col.row()

		box = row.box()
		box.use_property_split = True
		box.use_property_decorate = False
		box.scale_x= 0.4
		if bpy.app.version >= (5, 0, 0):
			box.row().prop(self, "compositor_type", text="Compositor", expand = True)
		
		box.label(text="UI Settings")
		col = box.column(heading="Panel", align=True)
		col.prop(self, "view3d", text="3D Viewport Panel")
		col.prop(self, "active_node_panel", text="Active Node")
		col.prop(self, "preset_panel", text="Presets Panel")
		col = box.column(heading = "Compositor")
		col.prop(self, "search", text="Search Box")
		sub = col.row()
		sub.prop(self, "layer_name", text="Layer Name", expand=True)

		sub = col.row(heading="Layer Display", align=True)
		sub.prop(self, "label", text="Label", toggle = True)
		sub.prop(self, "fx_toggle", text="FX", toggle = True)
		sub.prop(self, "blend_mode", text="Blend", toggle = True)
		sub.prop(self, "mix", text="Mix", toggle = True)
		col = box.column(heading="Properties", align=True)
		sub = col.row()
		sub.prop(self, "panel_type", text="Panel Type", expand=True)
		box.label(text="Operator")
		col = box.column(heading="", align=True)
		colrow = col.row()
		colrow.active = self.compositor_type != '5.0'
		colrow.prop(self, "new_compositor_option", text="New Compositor", expand = True)
		col = box.column(heading="", align=True)
		col.row().prop(self, "duplicate_layer_option", text="Duplicate Layer", expand = True)
		col.row().prop(self, "duplicate_effect_option", text="Effect", expand = True)

		box = row.box()
		colbox = box.column()
		
		if bpy.app.version < (5, 0, 0) or self.compositor_type == 'Legacy':
			type = "Effects"
		else:
			row = colbox.row(align=True)
			row.prop(self, 'preset_type', expand=True)
			row.menu("COMPOSITOR_MT_preset_specials", icon='DOWNARROW_HLT', text="")
			type = self.preset_type
		
		presets = get_presets(type)
		if len(presets) > 0:
			col = colbox.column()
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
			colbox.label(text="No Presets", icon = "FILEBROWSER")

classes = (
	AddonPreferences,
)

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
