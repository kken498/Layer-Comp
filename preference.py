import bpy
from .defs import *
from .ui import *

class AddonPref_Properties:
	active_node_panel : bpy.props.BoolProperty(default = True, description = "Show active node panel in compositor area.")
	preset_panel : bpy.props.BoolProperty(default = True, description = "Show effect preset panel.")
	preset_type : bpy.props.EnumProperty(default = "Effects",
							items = [('Effects', 'Effects', ''),
									('Compositors', 'Compositors', ''),
									],
							description = "Presets Type"
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
	color_space : bpy.props.BoolProperty(default = True, description = "Show colorspace in Compositor")
	
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
	
	default_color_space : bpy.props.EnumProperty(
						name='Color Space',
						default='scene_linear',
						items=colorspace_items,
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
		box.scale_x = 0.4
	
		draw_options(self, box)

		box = row.box()
		colbox = box.column()
		
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
