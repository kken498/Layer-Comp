import bpy
import os
import shutil
from ..defs import *
from bpy_extras.io_utils import ImportHelper, ExportHelper

class New_OT_Preset(bpy.types.Operator):
	bl_idname = "scene.comp_new_preset"
	bl_label = "New Presets"
	bl_description = "New Presets"
	bl_options = {'REGISTER', 'UNDO'}

	name : bpy.props.StringProperty(options={'HIDDEN'})
	type : bpy.props.EnumProperty(
						default = "Effects",
						name = "Type",
						items = [('Effects', 'Effect', ''),
								('Compositors', 'Compositor', ''),
								],
						options={'HIDDEN'}
								)
	
	def invoke(self, context, event):
		self.name = "New Preset"
		return context.window_manager.invoke_props_dialog(self)
	
	def draw(self, context):
		layout = self.layout
		col = layout.column()
		if self.name in get_presets(self.type):
			sub = col.row()
			sub.alert = True
			sub.label(text = "Preset's name exists")
		elif self.name.startswith('.'):
			sub = col.row()
			sub.alert = True
			sub.label(text = "Name cannot start with '.' ")
		else:
			col.label(text = "Name")
		col.prop(self,"name", text = "")

	def execute(self, context):
		if self.name in get_presets(self.type):
			return context.window_manager.invoke_props_dialog(self)
		filepath = get_filepath(self.type)
		blendfile  = os.path.join(filepath, f"{self.name}.blend")
		data_blocks = set()
		bpy.data.libraries.write(blendfile, data_blocks, fake_user=True, compress=True)
		return {"FINISHED"}
	
class Remove_OT_Preset(bpy.types.Operator):
	bl_idname = "scene.comp_remove_preset"
	bl_label = "Remove Presets"
	bl_description = "Remove Presets"
	bl_options = {'REGISTER', 'UNDO'}

	name : bpy.props.StringProperty(options={'HIDDEN'})
	type : bpy.props.EnumProperty(
						default = "Effects",
						name = "Type",
						items = [('Effects', 'Effect', ''),
								('Compositors', 'Compositor', ''),
								],
						options={'HIDDEN'}
								)

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def draw(self, context):
		layout = self.layout
		layout.label(text=f"Comfirm remove preset - {self.name}")
		col = layout.column()
		col.alert = True
		col.label(text="Operation cannot be undone!")

	def execute(self, context):
		filepath = get_filepath(self.type)
		blendfile  = os.path.join(filepath, f"{self.name}.blend")
		os.remove(blendfile)
		return {"FINISHED"}

class Export_OT_Preset(bpy.types.Operator, ExportHelper):
	bl_idname = "scene.comp_export_preset"
	bl_label = "Export Presets"
	bl_description = "Export Presets"
	filename_ext = ".blend"

	name : bpy.props.StringProperty(options={'HIDDEN'})
	type : bpy.props.EnumProperty(
						default = "Effects",
						name = "Type",
						items = [('Effects', 'Effect', ''),
								('Compositors', 'Compositor', ''),
								],
						options={'HIDDEN'}
								)
	
	def execute(self, context):
		destination_file = self.filepath
		# Source and destination file paths
		filepath = get_filepath(self.type)
		source_file = os.path.join(filepath, f"{self.name}.blend")

		try:
			shutil.copy(source_file, destination_file)
			print(f"File copied successfully from '{source_file}' to '{destination_file}'")
		except IOError as e:
			print(f"Unable to copy file. {e}")

		return {"FINISHED"}

class Load_OT_Preset(bpy.types.Operator, ImportHelper):
	bl_idname = "scene.comp_load_preset"
	bl_label = "Load Presets"
	bl_description = "Load Presets"
	bl_options = {'REGISTER', 'UNDO'}
	
	filename_ext = '.blend'
	
	filter_glob: bpy.props.StringProperty(
		default='*.blend',
		options={'HIDDEN'}
	)
	directory: bpy.props.StringProperty(
			subtype='DIR_PATH',
	)
	
	files: bpy.props.CollectionProperty(
			type=bpy.types.OperatorFileListElement,
	)
	save_preset: bpy.props.BoolProperty(
		name="Save as presets",
		default=False
	)	
	type : bpy.props.EnumProperty(
						default = "Effects",
						name = "Type",
						items = [('Effects', 'Effect', ''),
								('Compositors', 'Compositor', ''),
								],
						options={'HIDDEN'}
								)

	def execute(self, context):
		directory = self.directory
		
		for file_elem in self.files:
			blend = os.path.join(directory, file_elem.name)
			presets = os.path.join(get_filepath(self.type), file_elem.name)
			shutil.copyfile(blend, presets)

		self.report({"INFO"}, "Loaded All Presets!")

		return {"FINISHED"}

class Save_OT_Preset(bpy.types.Operator):
	bl_idname = "scene.comp_save_preset"
	bl_label = "Save Presets"
	bl_description = "Save Presets"
	bl_options = {'REGISTER', 'UNDO'}

	unavailable_node = {}
	exist_node = []

	def preset_item(self, context):
		list = []
		presets = get_presets(self.type)
		for name in presets:
			list.append((name, name, ''))
		return list
	
	skip : bpy.props.BoolProperty(name='Skip', default = False)

	overwrite : bpy.props.BoolProperty(name='Overwrite', default = False)

	preset : bpy.props.EnumProperty(
					name='Preset', 
					description = "Preset that your effect save.",
					items = preset_item,)
	
	type : bpy.props.EnumProperty(
						default = "Effects",
						name = "Type",
						items = [('Effects', 'Effect', ''),
								('Compositors', 'Compositor', ''),
								],
						options={'HIDDEN'}
								)

	def invoke(self, context, event):
		self.unavailable_node = {}
		self.exist_node = []
		self.overwrite = False
		self.skip = False
		if len(get_presets(self.type)) == 0:
			bpy.ops.scene.comp_new_preset(name="New Preset", type=self.type)
			return self.execute(context)
		else:
			self.preset = get_presets(self.type)[0]
			return context.window_manager.invoke_props_dialog(self)
	
	def draw(self, context):
		layout = self.layout
		layout.use_property_split = True
		layout.use_property_decorate = False

		layout.prop(self, "preset")

		if self.exist_node or self.unavailable_node:
			layout.prop(self, "skip")
		if self.exist_node:
			layout.prop(self, "overwrite")

		if self.unavailable_node:
			layout.label(text="Detect unavailable node tree.")
			col = layout.column()
			for name in self.unavailable_node:
				sub = col.row(align=True)
				sub.label(text=name)
				colrow = sub.column()
				for text in self.unavailable_node[name]:
					colrow.label(text=text)
				col.separator()

		if self.exist_node:
			layout.label(text="Detect exist effect.")
			col = layout.column()
			for node in self.exist_node:
				col.label(text=node.node_tree.name)

	def execute(self, context):
		tree = get_scene_tree(context)
		self.available_node = []
		if self.type == "Effects":
			selected_node = [node for node in tree.nodes if node.select and node.type == "GROUP"]

			# Check is NodeTree available | NodeTree need image input socket and output sockets
			for node in selected_node:
				if node.inputs.get('Image') and node.outputs:
					self.available_node.append(node.node_tree)
					node.node_tree.use_fake_user = True
				else:
					unavailable = []
					if not node.inputs.get('Image'):
						unavailable.append("No image input socket")
					if not node.outputs:
						unavailable.append("No output sockets")
					
					self.unavailable_node[node.name] = unavailable

			# If any unavailable node then return dialog | you can skip by skip option from dialog
			if self.unavailable_node and not self.skip:
				return context.window_manager.invoke_props_dialog(self)
			
		elif self.type == "Compositors":
			self.available_node.append(bpy.data.node_groups[context.scene.compositing_node_group.name])

		# Get preset filepath
		filepath = get_filepath(self.type)
		blendfile = os.path.join(filepath, f"{self.preset}.blend")

		# Create a appended group list
		appended_group = []

		# Get every node group and check ig they exist
		with bpy.data.libraries.load(blendfile, link=False) as (data_from, data_to):
			for node in self.available_node:
				if node.name in data_from.node_groups:
					self.exist_node.append(node)

			for node_group in data_from.node_groups:
				if node_group not in bpy.data.node_groups:
					data_to.node_groups.append(node_group) # Don't append node_group that already in file
				appended_group.append(node_group) # Append node group to appended group list

		# If any exist node then return dialog | you can skip or overwrite
		if self.exist_node and not (self.skip or self.overwrite):
			return context.window_manager.invoke_props_dialog(self)
		
		# Appended group + Available_node
		if self.overwrite:
			data_blocks = {bpy.data.node_groups[group] for group in appended_group} | {node for node in self.available_node}
		else:
			data_blocks = {bpy.data.node_groups[group] for group in appended_group} | {node for node in self.available_node if node not in self.exist_node}

		bpy.data.libraries.write(blendfile, data_blocks, fake_user=True, compress=True)

		# Remove the node group that is appended
		for group in appended_group:
			if bpy.data.node_groups[group].use_fake_user == False and bpy.data.node_groups[group].users == 0:
				bpy.data.node_groups.remove(bpy.data.node_groups[group])

		self.report({"INFO"}, f"Save Preset!")

		return {"FINISHED"}

class Remove_OT_Preset_Item(bpy.types.Operator):
	bl_idname = "scene.comp_remove_preset_item"
	bl_label = "Remove Presets"
	bl_description = "Remove Presets"
	bl_options = {'REGISTER', 'UNDO'}

	preset : bpy.props.StringProperty(options={'HIDDEN'})
	target : bpy.props.StringProperty(options={'HIDDEN'})
	type : bpy.props.EnumProperty(
						default = "Effects",
						name = "Type",
						items = [('Effects', 'Effect', ''),
								('Compositors', 'Compositor', ''),
								],
						options={'HIDDEN'}
								)

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def draw(self, context):
		layout = self.layout
		layout.label(text=f"Comfirm remove preset - {self.target}")
		col = layout.column()
		col.alert = True
		col.label(text="Operation cannot be undone!")

	def execute(self, context):

		target = self.target

		# Get preset filepath
		filepath = get_filepath(self.type)
		blendfile  = os.path.join(filepath, f"{self.preset}.blend")
		
		# Get current node group fake user and set all their use_fake_user to True
		not_fake_user_node_group = []
		for node_group in bpy.data.node_groups:
			if node_group.use_fake_user == False:
				not_fake_user_node_group.append(node_group)
				node_group.use_fake_user = True

		# Create a imported group list
		appended_group = []

		# Append all the preset effect node except the target
		with bpy.data.libraries.load(blendfile, link=False) as (data_from, data_to):
			for node_group in data_from.node_groups:
				if node_group not in bpy.data.node_groups and node_group != target:
					data_to.node_groups.append(node_group)
				if node_group != target:
					appended_group.append(node_group)

		# Overwrite the preset file (Overwrite is not include the target)
		data_blocks = {bpy.data.node_groups[group] for group in appended_group}
		bpy.data.libraries.write(blendfile, data_blocks, fake_user=True, compress=True)
		
		for group in appended_group:
			if bpy.data.node_groups[group].use_fake_user == False:
				bpy.data.node_groups.remove(bpy.data.node_groups[group])
			
		# Remove the node group that is imported (They are marked as not using fake user)
		for node_group in not_fake_user_node_group:
			node_group.use_fake_user = False

		self.report({"INFO"}, f"Remove {target} Preset!")

		return {"FINISHED"}

class Apply_OT_Preset_Item(bpy.types.Operator):
	bl_idname = "scene.comp_apply_preset_item"
	bl_label = "Apply Presets"
	bl_description = "Apply Presets"
	bl_options = {'REGISTER', 'UNDO'}

	preset : bpy.props.StringProperty(options={'HIDDEN'})
	target : bpy.props.StringProperty(options={'HIDDEN'})

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def draw(self, context):
		layout = self.layout
		layout.label(text="Comfirm apply compositor preset")

	def execute(self, context):
		props = context.scene.compositor_layer_props

		target = self.target

		# Get preset filepath
		filepath = get_filepath('Compositors')
		blendfile = os.path.join(filepath, f'{self.preset}.blend')

		if target not in bpy.data.node_groups:
			with bpy.data.libraries.load(blendfile) as (data_from, data_to):
				data_to.node_groups = [name for name in data_from.node_groups if name == name]

		node_group = bpy.data.node_groups[target]

		context.scene.compositing_node_group = node_group

		item = node_group.compositor_props
		item.sub_name = node_group.name
		item.name = node_group.name

		self.report({"INFO"}, f"Apply {target} Preset!")

		return {"FINISHED"}

class COMPOSITOR_MT_preset_specials(bpy.types.Menu):
	bl_label = "Preset Specials"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		addon_prefs = get_addon_preference(context)
		type = addon_prefs.preset_type
		
		layout = self.layout
		layout.operator("scene.comp_load_preset", text='Load Presets', icon = "IMPORT").type = type
		layout.menu("COMPOSITOR_MT_export_presets", text='Export Presets', icon = "EXPORT")

class COMPOSITOR_MT_export_presets(bpy.types.Menu):
	bl_label = "Export Preset"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		addon_prefs = get_addon_preference(context)
		type = addon_prefs.preset_type

		layout = self.layout
		presets = get_presets(type)
		if len(presets) > 0:
			for name in presets:
				export = layout.operator("scene.comp_export_preset", text=name)
				export.type = type
				export.name = name
		else:
			layout.label(text="No Preset")

classes = (
	New_OT_Preset,
	Remove_OT_Preset,
	Export_OT_Preset,
	Load_OT_Preset,
	Save_OT_Preset,
	Remove_OT_Preset_Item,
	Apply_OT_Preset_Item,
	COMPOSITOR_MT_preset_specials,
	COMPOSITOR_MT_export_presets,
		  )

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)