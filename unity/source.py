import bpy
from ..defs import *
from .node_data import *
from bpy_extras.io_utils import ImportHelper

class Source_Props(bpy.types.PropertyGroup):
	def get_name(self):
		return self.get("name", "")

	def set_name(self, value):
		if value == '':
			value = self.type

		# Define props
		context = bpy.context
		props = context.scene.compositor_layer_props

		# Check existing layer
		existing_names = [item.name for item in props.source if item.name != self.sub_name]

		new_name = unique_name(value, existing_names)

		self["name"] = new_name

	def update_name(self, context):
		addon_prefs = get_addon_preference(context)
		tree = get_scene_tree(context)

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
		
			if len(get_scene_compositor(context)) > 0:
				for name in get_scene_compositor(context):
					group_node = tree.nodes[name]
					for layer in group_node.node_tree.compositor_props.layer:
						if layer.source == self.sub_name:
							layer.source = self.name

					if group_node.inputs.get(self.sub_name):
						group_node.inputs[self.sub_name].name = self.name

					GroupInput = group_node.node_tree.nodes.get("Group Input")
					if GroupInput.outputs.get(self.sub_name):
						GroupInput.outputs[self.sub_name].name = self.name

		node = tree.nodes.get(self.sub_name)
		if node:
			node.name = self.name
			if node.type == 'GROUP':
				node.node_tree.compositor_props.name = self.name
				node.node_tree.name = self.name
			self.sub_name = self.name

	name : bpy.props.StringProperty(name='Source Name', update=update_name, get=get_name, set=set_name)
	sub_name : bpy.props.StringProperty()
	type : bpy.props.StringProperty()
	icon : bpy.props.StringProperty()
	
class SOURCE_UL_LIST(bpy.types.UIList):

	type : bpy.props.EnumProperty(default = "type",
							items = [('name', 'Name', ''),
									('type', 'Type', ''),
									],
							description = "Filter type."
									)
	
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

		if self.layout_type in {'DEFAULT'}:
			row = layout.row()
			row.label(text = "", icon = item.icon)
			row.prop(item, "name", text = "", emboss = False)

		return
	
	def filter_items(self, context, data, propname):
		items = getattr(data, propname)
		helper_funcs = bpy.types.UI_UL_list

		# Default return values.
		flt_flags = []
		flt_neworder = []

		# Reorder by name
		flt_neworder = helper_funcs.sort_items_by_name(
			items, self.type)
			
		return flt_flags, flt_neworder
	
	def draw_filter(self, context, layout):
		row = layout.row(align=True)
		row.prop(self, "type", text="")
		row.prop(self, "filter_name", text="")
		row.prop(self, "use_filter_invert", text="", icon = "ARROW_LEFTRIGHT")
		row.prop(self, "use_filter_sort_reverse", text="", icon = "SORT_DESC" if self.use_filter_sort_reverse else "SORT_ASC")

class Add_OT_Source(bpy.types.Operator):
	bl_idname = "scene.comp_add_source"
	bl_label = "Add Compositor Source"
	bl_description = "Add Compositor Source"
	bl_options = {'REGISTER', 'UNDO'}

	type : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props

		# Set new source node location next to the last source node
		sub_node = None
		for source in reversed(props.source):
			node = tree.nodes.get(source.name)
			if node.type == "GROUP" and node.node_tree.compositor_props.name:
				continue
			sub_node = node
			break

		node_data = source_node_data | texture_node_data

		node = tree.nodes.new(self.type)
		node.name = node_data[self.type][0]

		if sub_node:
			node.location = (sub_node.location[0],sub_node.location[1]-350)

		# Set properties
		item = props.source.add()
		item.name = node.name
		item.sub_name = node.name
		item.type = node_data[self.type][0]
		item.icon = node_data[self.type][1]

		props.source_index = len(props.source) - 1

		return {"FINISHED"}

class Reload_OT_Source(bpy.types.Operator):
	bl_idname = "scene.comp_reload_source"
	bl_label = "Reload Compositor Source"
	bl_description = "Reload Compositor Source"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		return get_scene_tree(context)

	def execute(self, context):
		# Define props
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props
		index = props.source_index
		props.source.clear()

		for node in tree.nodes:
			if node.bl_idname not in source_node_data or not node.outputs:
				continue
			
			if node.type == 'GROUP' and node.node_tree.name.startswith('.*'):
				continue

			item = props.source.add()
			item.name = node.name
			item.sub_name = node.name

			if node.type == 'GROUP':

				if node.node_tree.compositor_props.name:
					item.type = 'Compositor'
					item.icon = source_node_data[node.bl_idname][1]
				else:
					item.type = 'Group'
					item.icon = 'NODETREE'
			else:
				item.type = source_node_data[node.bl_idname][0]
				item.icon = source_node_data[node.bl_idname][1]

		props.source_index = index

		return {"FINISHED"}

class Remove_OT_Source(bpy.types.Operator):
	bl_idname = "scene.comp_remove_source"
	bl_label = "Remove Compositor Source"
	bl_description = "Remove Compositor Source"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props

		item = props.source[self.index]
		if item.name in get_scene_compositor(context):
			props.compositor_panel = item.name
			bpy.ops.scene.comp_remove_compositor()
		else:
			group_node = tree.nodes.get(item.name)
			if group_node:
				tree.nodes.remove(group_node)

		props.source.remove(self.index)

		bpy.ops.scene.comp_reload_source()

		return {"FINISHED"}

class Edit_OT_Source(bpy.types.Operator):
	bl_idname = "scene.comp_edit_source"
	bl_label = "Edit Compositor Source"
	bl_description = "Edit Compositor Source"
	bl_options = {'REGISTER', 'UNDO'}

	name : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		for name in get_scene_compositor(context):
			if name == self.name:
				props.panel = 'Compositor'
				props.compositor_panel = name
				break

		return {"FINISHED"}

class Load_OT_Source_Media(bpy.types.Operator, ImportHelper):
	bl_idname = "scene.comp_load_source_media"
	bl_label = "Load Media"
	bl_description = "Load Media"
	bl_options = {'REGISTER', 'UNDO'}
	
	filename_ext = '.bmp, .tiff, .png, .jpg, .jpeg, .webm, .gif, .mp4, .avi'  # List of acceptable image file extensions
	
	filter_glob: bpy.props.StringProperty(
		default='*.bmp;*.tiff;*.png;*.jpg;*.jpeg;*.webm;*.gif;*.mp4;*.avi',  # Update the default filter to include multiple image types
		options={'HIDDEN'}
	)

	directory: bpy.props.StringProperty(
			subtype='DIR_PATH',
	)
	
	files: bpy.props.CollectionProperty(
			type=bpy.types.OperatorFileListElement,
	)

	def execute(self, context):
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props

		directory = self.directory
		
		for file_elem in self.files:
			file_path = os.path.join(directory, file_elem.name)

			file_extension = os.path.splitext(file_path)[1]

			if file_extension in {'.mp4'}:
				if bpy.data.movieclips.get(file_elem.name):
					movieclips =  bpy.data.movieclips[file_elem.name]
				else:
					movieclips = bpy.data.movieclips.load(file_path)

				bpy.ops.scene.comp_add_source(type = 'CompositorNodeMovieClip')

				movieclips.use_fake_user = True

				node = tree.nodes.get(props.source[-1].name)
				node.clip = movieclips

				props.source[-1].name = movieclips.name

			else:
				if bpy.data.images.get(file_elem.name):
					image =  bpy.data.images[file_elem.name]
				else:
					image = bpy.data.images.load(file_path)

				bpy.ops.scene.comp_add_source(type = 'CompositorNodeImage')

				image.use_fake_user = True

				node = tree.nodes.get(props.source[-1].name)
				node.image = image

				props.source[-1].name = image.name

		return {'FINISHED'}

class New_Comp_OT_Source(bpy.types.Operator):
	bl_idname = "scene.comp_new_comp_from_source"
	bl_label = "New Compositor From Source"
	bl_description = "New compositor from source"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		props = context.scene.compositor_layer_props
		item = props.source[self.index]
		
		bpy.ops.scene.comp_new_compositor(from_source=True)

		bpy.ops.scene.comp_add_layer(name = item.name, icon = item.icon, type = "Source")

		return {"FINISHED"}

class Add_Comp_OT_Source(bpy.types.Operator):
	bl_idname = "scene.comp_add_comp_from_source"
	bl_label = "Add Compositor From Source"
	bl_description = "Add compositor from source"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def compositor_item(self, context):
		tree = get_scene_tree(context)
		list = []
		for i, name in enumerate(get_scene_compositor(context)):
			node_group = tree.nodes[name].node_tree
			compositor = node_group.compositor_props
			if compositor.layer:
				list.append((name, name, ''))
		return list
	
	compositor : bpy.props.EnumProperty(
						name = "Compositor",
						items = compositor_item,
								)

	def invoke(self, context, event):
		wm = context.window_manager
		if len(get_scene_compositor(context)) > 0:
			return wm.invoke_props_dialog(self)
		else:
			return self.execute(context)

	def execute(self, context):
		props = context.scene.compositor_layer_props
		item = props.source[self.index]

		if self.compositor:
			props.compositor_panel = self.compositor

			bpy.ops.scene.comp_add_layer(name = item.name, icon = item.icon, type = "Source")

		else:
		
			bpy.ops.scene.comp_new_compositor(from_source=True)

			bpy.ops.scene.comp_add_layer(name = item.name, icon = item.icon, type = "Source")

		return {"FINISHED"}

class COMPOSITOR_MT_add_source(bpy.types.Menu):
	bl_label = "Source"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout

		group = source_node_data['CompositorNodeGroup']
		layout.operator("scene.comp_new_compositor", text=group[0], icon=group[1])
		layout.separator()
		
		for item in source_node_data:
			if item != 'GROUP':
				layout.operator("scene.comp_add_source", text=source_node_data[item][0], icon = source_node_data[item][1]).type = item

		layout.separator()
		if bpy.app.version >= (4, 5, 0):
			layout.menu("COMPOSITOR_MT_add_texture_source", icon = "TEXTURE")
		elif bpy.app.version < (4, 5, 0):
			texture = source_node_data['CompositorNodeTexture']
			layout.operator("scene.comp_add_source", text=texture[0], icon = "TEXTURE").type = 'CompositorNodeTexture'

class COMPOSITOR_MT_add_texture_source(bpy.types.Menu):
	bl_label = "Texture"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		for item in texture_node_data:
			if bpy.app.version >= (5, 0, 0) and item == 'CompositorNodeTexture':
				continue
			layout.operator("scene.comp_add_source", text=texture_node_data[item][0]).type = item

def draw_source(self, context, box):
	tree = get_scene_tree(context)
	props = context.scene.compositor_layer_props
	
	row = box.row(align=True)
	row.operator("wm.call_menu", text="Add Source", icon='ADD').name = "COMPOSITOR_MT_add_source"
	row.operator("scene.comp_load_source_media", text='Load Media', icon = 'FILEBROWSER')
	box.template_list("SOURCE_UL_LIST", "", props, "source", props, "source_index")

	if len(props.source) > 0 and props.source_index < len(props.source):
		item = props.source[props.source_index]
		node = tree.nodes[item.name]
		row = box.row(align=True)
		row.label(text="", icon = item.icon)
		row.prop(item, 'name', text="")
		row.operator("scene.comp_add_comp_from_source", text="", icon='ADD').index = props.source_index
		row.operator("scene.comp_new_comp_from_source", text="", icon='NODE_COMPOSITING').index = props.source_index
		if item.type == 'GROUP':
			row.operator("scene.comp_remove_compositor", text="", icon='X').name = item.name
		else:
			row.operator("scene.comp_remove_source", text="", icon='X').index = props.source_index
		xbox = box.box()
		xbox.label(text="Properties", icon = "PROPERTIES")
		if item.type == 'COMPOSITOR':
			xbox.operator("scene.comp_edit_source", text="Edit Compositor", icon='NODE_COMPOSITING').name = item.name
		else:
			xbox.template_node_inputs(node)

classes = (
	Source_Props,
	SOURCE_UL_LIST,
	Add_OT_Source,
	Reload_OT_Source,
	Remove_OT_Source,
	Edit_OT_Source,
	Load_OT_Source_Media,
	New_Comp_OT_Source,
	Add_Comp_OT_Source,
	COMPOSITOR_MT_add_source,
	COMPOSITOR_MT_add_texture_source,
		  )

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)