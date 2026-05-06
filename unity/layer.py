import bpy
import re
from ..defs import *
from .effect import *
from .matte import *
from .mask import *
from .node_data import *
from bpy_extras.io_utils import ImportHelper

class Layer_Props(Matte_Props, bpy.types.PropertyGroup):
	def get_name(self):
		return self.get("name", "")

	def set_name(self, value):
		if value == '':
			value = self.source

		# Define props
		context = bpy.context
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props

		# Check existing layer
		existing_names = [item.name for item in compositor.layer if item.name != self.sub_name]

		new_name = unique_name(value, existing_names)

		self["name"] = new_name

	def update_name(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]

		for node in node_group.nodes:
			if node.parent == node_group.nodes.get(f"{self.sub_name}.Frame"):
				if node.name.startswith(f"{self.sub_name}.") and not re.match(rf"{self.sub_name}.\d+", node.name) or node.name == self.sub_name:
					node.name = node.name.replace(self.sub_name, self.name)

		if node_group.nodes.get(f"{self.sub_name}.Frame"):
			frame = node_group.nodes.get(f"{self.sub_name}.Frame")
			frame.name = frame.name.replace(self.sub_name, self.name)
			frame.label = self.name

		self.sub_name = self.name

	def update_hide(self, context):
		# Mute Mix node
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		mix_node = node_group.nodes.get(f"{self.name}.Mix")
		if bpy.app.version >= (5, 0, 0):
			if any(layer.solo for layer in compositor.layer):
				if self.solo:
					mix_node.inputs["Mute"].default_value = self.hide
				else:
					return
			else:
				mix_node.inputs["Mute"].default_value = self.hide

		elif bpy.app.version < (5, 0, 0):
			if any(layer.solo for layer in compositor.layer):
				if self.solo:
					mix_node.mute = self.hide
				else:
					return
			else:
				mix_node.mute = self.hide

	def update_fx(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]

		for effect in self.effect:
			effect_node = node_group.nodes.get(f'{self.name}.Effect.{effect.name}')
			if effect.hide == False and self.fx == True:
				effect_node.mute = False
			else:
				effect_node.mute = True

	def layer_channel(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		node = node_group.nodes.get(layer.name)

		list = []
		i = 0
		for item in node.outputs:
			if item.enabled:
				if bpy.app.version >= (4, 5, 0):
					list.append((item.name, item.name, '', socket_data[item.type], i))
				elif bpy.app.version < (4, 5, 0):
					list.append((item.name, item.name, ''))
				i += 1
		return list
	
	def update_layer_channel(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		node = node_group.nodes.get(layer.name)

		for link in node_group.links:
			if link.from_node == node:
				output_socket = link.to_socket
				break

		node_group.links.new(node.outputs[self.channel], output_socket)

	def update_layer_solo(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		if bpy.app.version >= (5, 0, 0):
			if any(layer.solo for layer in compositor.layer):
				for layer in compositor.layer:
					mix_node = node_group.nodes.get(f"{layer.name}.Mix")
					mix_node.inputs["Mute"].default_value = not layer.solo
			else:
				for layer in compositor.layer:
					mix_node = node_group.nodes.get(f"{layer.name}.Mix")
					mix_node.inputs["Mute"].default_value = layer.hide

		elif bpy.app.version < (5, 0, 0):
			if any(layer.solo for layer in compositor.layer):
				for layer in compositor.layer:
					mix_node = node_group.nodes.get(f"{layer.name}.Mix")
					mix_node.mute = not layer.solo
			else:
				for layer in compositor.layer:
					mix_node = node_group.nodes.get(f"{layer.name}.Mix")
					mix_node.mute = layer.hide

	def label_item(self, context):
		list = []
		if self.type != "Adjustment":
			list.append((self.icon, '', '', self.icon, 0))
		for i in range(9):
			if self.type != "Adjustment":
				index = i+1
			else:
				index = i
			icon = f'STRIP_COLOR_0{i+1}'
			list.append((icon, '', '', icon, index))
		for i, item in enumerate(socket_data):
			list.append((socket_data[item], '', '', socket_data[item], i+10))

		return list
	
	def update_colorspace(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		
		color_in_node = node_group.nodes.get(f"{layer.name}.color_in")
		color_out_node = node_group.nodes.get(f"{layer.name}.color_out")

		if color_in_node:
			color_in_node.to_color_space = self.colorspace
		if color_out_node:
			color_out_node.from_color_space = self.colorspace

	def update_in_colorspace(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		
		color_in_node = node_group.nodes.get(f"{layer.name}.color_in")

		if color_in_node:
			color_in_node.from_color_space = self.in_colorspace

	def update_out_colorspace(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]
		
		color_out_node = node_group.nodes.get(f"{layer.name}.color_out")

		if color_out_node:
			color_out_node.to_color_space = self.out_colorspace

	name : bpy.props.StringProperty(name='Layer Name', update=update_name, get=get_name, set=set_name)
	sub_name : bpy.props.StringProperty()
	icon : bpy.props.StringProperty()
	source : bpy.props.StringProperty(name='Source Name', )
	socket : bpy.props.StringProperty()
	type : bpy.props.StringProperty()

	effect : bpy.props.CollectionProperty(type=Effect_Props)
	effect_index: bpy.props.IntProperty(name = "Effect")

	mask : bpy.props.CollectionProperty(type=Mask_Props)
	mask_index: bpy.props.IntProperty(name = "Mask")

	fx : bpy.props.BoolProperty(name='Toggle Layer Effect',  default=True, update=update_fx)
	channel : bpy.props.EnumProperty(
							items = layer_channel,
							update = update_layer_channel
									)
	
	colorspace : bpy.props.EnumProperty(
							name='Color Space',
							default='scene_linear',
							items=colorspace_items,
							update = update_colorspace,
									)
	
	in_colorspace : bpy.props.EnumProperty(
							name='In Color Space',
							default='scene_linear',
							items=colorspace_items,
							update = update_in_colorspace,
									)
	
	out_colorspace : bpy.props.EnumProperty(
							name='Out Color Space',
							default='scene_linear',
							items=colorspace_items,
							update = update_out_colorspace,
									)

	label : bpy.props.EnumProperty(
					name='Layer Label', 
					items = label_item,
							)

	solo : bpy.props.BoolProperty(name='Solo Layer', update = update_layer_solo)
	hide : bpy.props.BoolProperty(name='Hide Layer', update = update_hide)

	drag : bpy.props.BoolProperty()
	index : bpy.props.IntProperty()

class LAYER_UL_LIST(bpy.types.UIList):

	def update_layer_name(self, context):
		addon_prefs = get_addon_preference(context)
		if addon_prefs.layer_name == 'Layer':
			addon_prefs.layer_name = 'Source'
		elif addon_prefs.layer_name == 'Source':
			addon_prefs.layer_name = 'Layer'

	layer_name: bpy.props.BoolProperty(
		name="Layer Name",
		default=False,
		update=update_layer_name
	)

	def draw_filter(self, context, layout):
		addon_prefs = get_addon_preference(context)
		row = layout.row(align=True)
		row.prop(self, "layer_name", toggle = True, text=addon_prefs.layer_name, invert_checkbox = not self.layer_name)
		row.prop(addon_prefs, "label", text="Label", toggle = True)
		row.prop(addon_prefs, "fx_toggle", text="FX", toggle = True)
		row.prop(addon_prefs, "blend_mode", text="Blend", toggle = True)
		row.prop(addon_prefs, "mix", text="Mix", toggle = True)

	def draw_item(self, context, layout, data, item, propname, icon, active_data, active_propname, index):

		if self.layout_type in {'DEFAULT'}:
			props = context.scene.compositor_layer_props
			node_group = bpy.data.node_groups[props.compositor_panel]
			compositor = node_group.compositor_props
			addon_prefs = get_addon_preference(context)

			mix_node = node_group.nodes.get(f"{item.name}.Mix")

			row = layout.row(align=True)
			row.prop(item, "hide", text = "", icon = "HIDE_ON" if item.hide == True else "HIDE_OFF", emboss = False)
			if item.hide:
				row.label(text = '', icon = 'BLANK1')
			else:
				row.prop(item, "solo", text = "", icon = "LAYER_ACTIVE" if item.solo == True else "LAYER_USED", emboss = False)

			hide = False
			if any(layer.solo for layer in compositor.layer):
				if item.solo:
					hide = not item.hide
				else:
					hide = False
			else:
				hide = not item.hide

			xrow = row.row(align=True)
			xrow.active = hide

			sub = xrow.row(align=True)
			subrow = sub.row()
			subrow.prop(item, "label", text = "", emboss = False)

			if addon_prefs.layer_name == "Layer":
				subrow.prop(item, "name", text = "", emboss = False)
			elif addon_prefs.layer_name == "Source":
				subrow.label(text = f'{str(len(compositor.layer) - item.index)}   {item.source}')

			sub = xrow.row(align=True)
			if addon_prefs.label:
				if item.matte != "None":
					sub.label(text = "", icon = "IMAGE_ZDEPTH")
				elif item.is_matte:
					sub.label(text = "", icon = "MOD_MASK")
				else:
					sub.label(text = "", icon = "BLANK1")
			
			if addon_prefs.fx_toggle:
				if item.effect:
					sub.prop(item, "fx", text = "", icon = "SHADERFX")
				else:
					sub.label(text = "", icon = "BLANK1")

			sub = xrow.row(align=True)
			if addon_prefs.blend_mode:
				sub.prop(mix_node.inputs[0], 'default_value', text="")
			if addon_prefs.mix:
				sub.prop(mix_node.inputs[1], 'default_value', text="Opacity")

			row.operator("scene.comp_drag_layer", text="", icon='LAYER_ACTIVE' if item.drag else 'COLLAPSEMENU', emboss = False).index = item.index

		return
	
	def filter_items(self, context, data, propname):
		"""Filter and sort items in the list"""

		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props

		filtered = []
		ordered = []

		items = getattr(data, propname)
		helper_funcs = bpy.types.UI_UL_list

		if compositor.search:
			filtered = helper_funcs.filter_items_by_name(compositor.search, self.bitflag_filter_item, items, "name",
															reverse=self.use_filter_sort_reverse)
			
		no_match = all(elem == 0 for elem in filtered)

		if no_match:
			filtered = []

		ordered = list(reversed(range(len(items))))

		return filtered, ordered

class Add_OT_Layer(bpy.types.Operator):
	bl_idname = "scene.comp_add_layer"
	bl_label = "Add Compositor Layer"
	bl_description = "Add Compositor Layer"
	bl_options = {'REGISTER', 'UNDO'}
	
	name : bpy.props.StringProperty(options={'HIDDEN'})
	icon : bpy.props.StringProperty(options={'HIDDEN'})
	socket : bpy.props.StringProperty(options={'HIDDEN'})
	type : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		addon_prefs = get_addon_preference(context)
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props

		# Check existing nodes
		existing_names = [item.name for item in compositor.layer]
		if self.socket:
			source_name = unique_name(f'{self.name}({self.socket})', existing_names)
		else:
			source_name = unique_name(self.name, existing_names)

		# Define nodes
		node_group = bpy.data.node_groups[compositor.name]
		
		# Define node group nodes
		GroupInput = node_group.nodes.get("Group Input")
		GroupOutput = node_group.nodes.get("Group Output")
		
		# Create Frame
		frame = node_group.nodes.new("NodeFrame")
		frame.name = f"{source_name}.Frame"
		frame.label = source_name

		mix_node = append_node('Presets', ".*Mix Layer", 'v5_0', node_group.nodes)
		mix_node.name = f"{source_name}.Mix"
		mix_node.parent = frame

		# Create color space conversion nodes
		color_in_node = node_group.nodes.new("CompositorNodeConvertColorSpace")
		color_in_node.name = f"{source_name}.color_in"
		color_in_node.parent = frame
		color_in_node.location = (mix_node.location[0] - 500, mix_node.location[1] - 150)

		color_out_node = node_group.nodes.new("CompositorNodeConvertColorSpace")
		color_out_node.name = f"{source_name}.color_out"
		color_out_node.parent = frame
		color_out_node.location = (mix_node.location[0] - 200, mix_node.location[1] - 150)

		# Connect color_out to mix
		node_group.links.new(color_out_node.outputs[0], mix_node.inputs[3])

		# Initially connect color_in to color_out
		node_group.links.new(color_in_node.outputs[0], color_out_node.inputs[0])

		if self.type == "Adjustment":
			if len(compositor.layer) == 0:
				GroupInput = node_group.nodes.new("NodeGroupInput")
				GroupInput.name = f"{source_name}.GroupInput"
				GroupInput.parent = frame

				# Connect GroupInput to color_in
				node_group.links.new(color_in_node.inputs[0], GroupInput.outputs[0])
			else:
				last_layer = compositor.layer[-1]
				last_mix = node_group.nodes.get(f"{last_layer.name}.Mix")
				node_group.links.new(color_in_node.inputs[0], last_mix.outputs[0])
			
			input_node = None

		elif self.type == "Compositor":
			input_node = node_group.nodes.new("CompositorNodeGroup")
			input_node.node_tree = bpy.data.node_groups[self.name]
			input_node.name = source_name
			input_node.parent = frame
			
			# Connect to color_in
			output = get_outputs(input_node, None)
			node_group.links.new(color_in_node.inputs[0], output)

		else:
			input_node = node_group.nodes.new(self.type)
			input_node.name = source_name
			input_node.parent = frame
			
			# Connect to color_in
			output = get_outputs(input_node, None)
			node_group.links.new(color_in_node.inputs[0], output)

		# Set alpha to mix node 1 if the layer is single layer
		if len(compositor.layer) == 0:
			node_group.links.new(mix_node.inputs[2], GroupInput.outputs[0])
		else:
			# Connect mix node from last layer 
			last_layer = compositor.layer[len(compositor.layer)-1]
			last_mix_node = node_group.nodes.get(f"{last_layer.name}.Mix")

			node_group.links.new(mix_node.inputs[2], last_mix_node.outputs[0])

		if input_node:
			input_node.location = (color_in_node.location[0] - 250, color_in_node.location[1] - 100)
			GroupInput.location = (input_node.location[0], input_node.location[1] + 250)
		else:
			GroupInput.location = (color_in_node.location[0] - 500, color_in_node.location[1] + 250)

		node_group.links.new(GroupOutput.inputs[0], mix_node.outputs[0])

		# Create or update viewer node
		viewer_node = node_group.nodes.get("Viewer")
		if not viewer_node:
			viewer_node = node_group.nodes.new("CompositorNodeViewer")
			viewer_node.name = "Viewer"
		
		# Connect viewer to current mix node output
		for link in node_group.links:
			if link.from_socket.node == viewer_node:
				node_group.links.remove(link)
				break
		node_group.links.new(mix_node.outputs[0], viewer_node.inputs[0])

		# Add layer properties
		item = compositor.layer.add()
		item.name = source_name
		item.sub_name = source_name
		item.icon = self.icon
		item.source = self.name
		item.socket = self.socket
		item.type = self.type
		item.index = len(compositor.layer) - 1
		item.colorspace = addon_prefs.default_color_space

		self.socket = ""

		compositor.layer_index = len(compositor.layer) - 1

		bpy.ops.scene.comp_align_node_tree(name=node_group.name)

		return {"FINISHED"}

class Add_OT_Layer_Media(bpy.types.Operator, ImportHelper):
	bl_idname = "scene.comp_add_layer_media"
	bl_label = "Add Media"
	bl_description = "Add Media"
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
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]

		directory = self.directory
		
		for file_elem in self.files:
			file_path = os.path.join(directory, file_elem.name)

			file_extension = os.path.splitext(file_path)[1]

			if file_extension in {'.mp4'}:
				if bpy.data.movieclips.get(file_elem.name):
					movieclips =  bpy.data.movieclips[file_elem.name]
				else:
					movieclips = bpy.data.movieclips.load(file_path)

				bpy.ops.scene.comp_add_layer(name=movieclips.name, icon="MOVIECLIP", type="CompositorNodeMovieClip")

				movieclips.use_fake_user = True

				node = node_group.nodes.get(movieclips.name)
				node.clip = movieclips

			else:
				if bpy.data.images.get(file_elem.name):
					image =  bpy.data.images[file_elem.name]
				else:
					image = bpy.data.images.load(file_path)

				bpy.ops.scene.comp_add_layer(name=image.name, icon="OUTLINER_OB_IMAGE", type="CompositorNodeImage")

				image.use_fake_user = True

				node = node_group.nodes.get(image.name)
				node.image = image

		return {'FINISHED'}

class Remove_OT_Layer(bpy.types.Operator):
	bl_idname = "scene.comp_remove_layer"
	bl_label = "Remove Compositor Layer"
	bl_description = "Remove Compositor Layer Socket"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[self.index]

		layer_matte = {}

		for l in compositor.layer:
			layer_matte[l.name] = l.matte
	
		# Define nodes
		if node_group.nodes.get(f"{layer.name}.GroupInput"):
			GroupInput = node_group.nodes.get(f"{layer.name}.GroupInput")
		else:
			GroupInput = node_group.nodes.get("Group Input")
			
		mix_node = node_group.nodes.get(f"{layer.name}.Mix")

		# Connect last layer to the next layer
		last_layer = compositor.layer[compositor.layer_index-1]
		last_mix_node = node_group.nodes.get(f"{last_layer.name}.Mix")

		for link in node_group.links:
			if link.from_node == mix_node:
				next_input = link.to_socket
				if compositor.layer_index > 0:
					node_group.links.new(next_input, get_mix_node_outputs(last_mix_node))
				else:
					node_group.links.new(next_input, node_group.nodes.get("Group Input").outputs[0])

		# Remove layer and change index
		for i, l in enumerate(compositor.layer):
			if i > self.index:
				l.index -= 1

		# Remove node
		for node in node_group.nodes:
			if node.parent == node_group.nodes.get(f"{layer.name}.Frame"):
				if node.name.startswith(f"{layer.name}.") and not re.match(rf"{layer.name}.\d+", node.name) or node.name == layer.name:
					node_group.nodes.remove(node)

		if node_group.nodes.get(f"{layer.name}.Frame"):
			node_group.nodes.remove(node_group.nodes.get(f"{layer.name}.Frame"))

		layer.effect.clear()

		for l in compositor.layer:
			if layer_matte[l.name] != layer.name:
				l.matte = layer_matte[l.name]

		compositor.layer.remove(self.index)
		if compositor.layer_index > 0:
			compositor.layer_index -= 1

		if len(compositor.layer) == 0:
			GroupInput = node_group.nodes.get("Group Input")
			GroupOutput = node_group.nodes.get("Group Output")
			node_group.links.new(GroupInput.outputs[0], GroupOutput.inputs[0])
		else:
			# Update viewer to show new top layer
			viewer_node = node_group.nodes.get("Viewer")
			if viewer_node:
				for link in node_group.links:
					if link.from_socket.node == viewer_node:
						node_group.links.remove(link)
						break
				new_top_layer = compositor.layer[-1]
				new_top_mix = node_group.nodes.get(f"{new_top_layer.name}.Mix")
				if new_top_mix:
					node_group.links.new(new_top_mix.outputs[0], viewer_node.inputs[0])

		bpy.ops.scene.comp_align_node_tree(name=node_group.name)

		return {"FINISHED"}

class Clear_OT_Layer(bpy.types.Operator):
	bl_idname = "scene.comp_clear_layer"
	bl_label = "Clear Compositor Layer"
	bl_description = "Clear Compositor Layer"
	bl_options = {'REGISTER', 'UNDO'}

	@classmethod
	def poll(cls, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		return len(compositor.layer) > 0
	
	def execute(self, context):
		# Define props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		for i in range(len(compositor.layer)):
			bpy.ops.scene.comp_remove_layer(index=0)

		return {"FINISHED"}

class Duplicate_OT_Layer(bpy.types.Operator):
	bl_idname = "scene.comp_duplicate_layer"
	bl_label = "Duplicate Compositor Layer"
	bl_description = "Duplicate Compositor Layer"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		addon_prefs = get_addon_preference(context)
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[compositor.layer_index]

		layer_matte_set = {}

		for l in compositor.layer:
			layer_matte_set[l.name] = l.matte

		layer_matte = (layer.matte, layer.matte_type, layer.matte_invert)

		bpy.ops.scene.comp_add_layer(name=layer.source, icon=layer.icon, socket=layer.socket ,type=layer.type)

		new_layer = compositor.layer[len(compositor.layer)-1]

		new_layer.colorspace = layer.colorspace
		new_layer.in_colorspace = layer.in_colorspace
		new_layer.out_colorspace = layer.out_colorspace

		if layer_matte[0] != "None":
			new_layer.matte = layer_matte[0]
			new_layer.matte_type = layer_matte[1]
			new_layer.matte_invert  = layer_matte[2]

		mix_node = node_group.nodes.get(f"{layer.name}.Mix")
		new_mix_node = node_group.nodes.get(f"{new_layer.name}.Mix")

		color_in_node = node_group.nodes.get(f"{layer.name}.color_in")
		new_color_in_node = node_group.nodes.get(f"{new_layer.name}.color_in")

		color_out_node = node_group.nodes.get(f"{layer.name}.color_out")
		new_color_out_node = node_group.nodes.get(f"{new_layer.name}.color_out")

		source_node = node_group.nodes.get(layer.name)
		new_source_node = node_group.nodes.get(new_layer.name)

		convert_node_data(mix_node, new_mix_node)
		convert_node_data(color_in_node, new_color_in_node)
		convert_node_data(color_out_node, new_color_out_node)
		if source_node and new_source_node:
			convert_node_data(source_node, new_source_node)

		if addon_prefs.duplicate_layer_option == "Next":
			for i in range(len(compositor.layer) - 1, -1, -1):
				if i > self.index + 1:
					bpy.ops.scene.comp_move_layer(index=i, direction='DOWN')

		if layer.effect:
			bpy.ops.scene.comp_copy_effect(compositor=compositor.name, layer=str(layer.index), effect="All")

		if layer.mask:
			bpy.ops.scene.comp_copy_mask(compositor=compositor.name, layer=str(layer.index), mask="All")

		feather_node = node_group.nodes.get(f'{layer.name}.Mask_Feather')
		new_feather_node = node_group.nodes.get(f'{new_layer.name}.Mask_Feather')

		if feather_node and new_feather_node:
			convert_node_data(feather_node, new_feather_node)

		for l in compositor.layer:
			if l.name in layer_matte_set:
				l.matte = layer_matte_set[l.name]

		bpy.ops.scene.comp_align_node_tree(name=node_group.name)

		return {"FINISHED"}

class Copy_OT_Layer(bpy.types.Operator):
	bl_idname = "scene.comp_copy_layer"
	bl_label = "Copy Compositor Layer"
	bl_description = "Copy Compositor Layer"
	bl_options = {'REGISTER', 'UNDO'}

	def compositor_item(self, context):
		list = []
		for i, name in enumerate(get_scene_compositor(context)):
			node_group = bpy.data.node_groups[name]
			compositor = node_group.compositor_props
			if compositor.layer:
				list.append((name, name, ''))
		return list
	
	def layer_item(self, context):
		node_group = bpy.data.node_groups[self.compositor]
		compositor = node_group.compositor_props
		list = []
		list.append(('All', 'All', '', 'STRIP_COLOR_01', 0))
		for i, item in enumerate(compositor.layer):
			list.append((str(i), item.name, '', item.label, i+1))
		return list
	
	compositor : bpy.props.EnumProperty(
						name = "Compositor",
						items = compositor_item,
								)
	
	layer : bpy.props.EnumProperty(
						name = "Layer",
						items = layer_item,
								)

	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_props_dialog(self)

	def execute(self, context):
		if not (self.compositor and self.layer):
			self.report({"INFO"}, "No layer item")
			return {"FINISHED"}

		props = context.scene.compositor_layer_props

		copy_node_group = bpy.data.node_groups[self.compositor]

		copy_compositor = copy_node_group.compositor_props
		
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props

		if self.layer != 'All':
			copy_layer = copy_compositor.layer[int(self.layer)]

			copy_layer_matte = (copy_layer.matte, copy_layer.matte_type, copy_layer.matte_invert)

			bpy.ops.scene.comp_add_layer(name=copy_layer.source, icon=copy_layer.icon, socket=copy_layer.socket ,type=copy_layer.type)

			new_layer = compositor.layer[len(compositor.layer)-1]

			new_layer.name = copy_layer.name

			new_layer.colorspace = copy_layer.colorspace
			new_layer.in_colorspace = copy_layer.in_colorspace
			new_layer.out_colorspace = copy_layer.out_colorspace

			if copy_layer_matte[0] != "None":
				if any(copy_layer_matte[0] == layer.name for layer in compositor.layer):
					new_layer.matte = copy_layer_matte[0]
					new_layer.matte_type = copy_layer_matte[1]
					new_layer.matte_invert  = copy_layer_matte[2]

			mix_node = copy_node_group.nodes.get(f"{copy_layer.name}.Mix")
			new_mix_node = node_group.nodes.get(f"{new_layer.name}.Mix")

			color_in_node = copy_node_group.nodes.get(f"{copy_layer.name}.color_in")
			new_color_in_node = node_group.nodes.get(f"{new_layer.name}.color_in")

			color_out_node = copy_node_group.nodes.get(f"{copy_layer.name}.color_out")
			new_color_out_node = node_group.nodes.get(f"{new_layer.name}.color_out")

			source_node = copy_node_group.nodes.get(copy_layer.name)
			new_source_node = node_group.nodes.get(new_layer.name)

			convert_node_data(mix_node, new_mix_node)
			convert_node_data(color_in_node, new_color_in_node)
			convert_node_data(color_out_node, new_color_out_node)
			if source_node and new_source_node:
				convert_node_data(source_node, new_source_node)

			if copy_layer.effect:
				bpy.ops.scene.comp_copy_effect(compositor=copy_compositor.name, layer=str(copy_layer.index), effect="All")

			if copy_layer.mask:
				bpy.ops.scene.comp_copy_mask(compositor=copy_compositor.name, layer=str(copy_layer.index), mask="All")

			feather_node = copy_node_group.nodes.get(f'{copy_layer.name}.Mask_Feather')
			new_feather_node = node_group.nodes.get(f'{new_layer.name}.Mask_Feather')

			if feather_node and new_feather_node:
				convert_node_data(feather_node, new_feather_node)

		else:
			for copy_layer in copy_compositor.layer:

				bpy.ops.scene.comp_add_layer(name=copy_layer.source, icon=copy_layer.icon, socket=copy_layer.socket ,type=copy_layer.type)

				new_layer = compositor.layer[len(compositor.layer)-1]

				new_layer.name = copy_layer.name

				new_layer.colorspace = copy_layer.colorspace
				new_layer.in_colorspace = copy_layer.in_colorspace
				new_layer.out_colorspace = copy_layer.out_colorspace

				mix_node = copy_node_group.nodes.get(f"{copy_layer.name}.Mix")
				new_mix_node = node_group.nodes.get(f"{new_layer.name}.Mix")

				source_node = copy_node_group.nodes.get(copy_layer.name)
				new_source_node = node_group.nodes.get(new_layer.name)

				convert_node_data(mix_node, new_mix_node)
				if source_node and new_source_node:
					convert_node_data(source_node, new_source_node)

				if copy_layer.effect:
					bpy.ops.scene.comp_copy_effect(compositor=copy_compositor.name, layer=str(copy_layer.index), effect="All")

				if copy_layer.mask:
					bpy.ops.scene.comp_copy_mask(compositor=copy_compositor.name, layer=str(copy_layer.index), mask="All")

				feather_node = copy_node_group.nodes.get(f'{copy_layer.name}.Mask_Feather')
				new_feather_node = node_group.nodes.get(f'{new_layer.name}.Mask_Feather')

				if feather_node and new_feather_node:
					convert_node_data(feather_node, new_feather_node)

			for copy_layer in copy_compositor.layer:
				
				copy_layer_matte = (copy_layer.matte, copy_layer.matte_type, copy_layer.matte_invert)

				new_layer = compositor.layer[copy_layer.name]

				if copy_layer_matte[0] != "None":
					if any(copy_layer_matte[0] == layer.name for layer in compositor.layer):
						new_layer.matte = copy_layer_matte[0]
						new_layer.matte_type = copy_layer_matte[1]
						new_layer.matte_invert  = copy_layer_matte[2]

		return {"FINISHED"}

class Move_OT_Layer(bpy.types.Operator):
	bl_idname = "scene.comp_move_layer"
	bl_label = "Move Compositor Layer"
	bl_options = {'REGISTER', 'UNDO'}

	index : bpy.props.IntProperty(options={'HIDDEN'})
	direction : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		tree = get_scene_tree(context)
		props = tree.compositor_props
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[self.index]

		GroupInput = node_group.nodes.get("Group Input")

		if self.direction == 'UP' and self.index < len(compositor.layer) - 1:
			next_layer = compositor.layer[self.index+1]
			mix_node = node_group.nodes[f"{layer.name}.Mix"]
			next_mix_node = node_group.nodes[f"{next_layer.name}.Mix"]
			last_mix_node = None
			if self.index > 0:
				last_layer = compositor.layer[self.index-1]
				last_mix_node = node_group.nodes.get(f"{last_layer.name}.Mix")

			input_socket = []
			input_socket2 = []
			input_socket3 = []
			output_socket = []

			for link in node_group.links:
				if link.from_socket == get_mix_node_outputs(next_mix_node):
					input_socket.append(link.to_socket)

				if link.from_socket == get_mix_node_outputs(mix_node):
					input_socket2.append(link.to_socket)

				if link.to_socket == get_mix_node_inputs(mix_node, 1):
					if "GroupInput" not in link.from_node.name:
						output_socket.append(link.from_socket)

				if last_mix_node:
					if link.from_socket == get_mix_node_outputs(last_mix_node):
						input_socket3.append(link.to_socket)

			for input in input_socket:
				node_group.links.new(get_mix_node_outputs(mix_node), input)

			if input_socket3:
				for input in input_socket3:
					node_group.links.new(get_mix_node_outputs(next_mix_node), input)

			if output_socket:
				for output in output_socket:
					node_group.links.new(output, get_mix_node_inputs(next_mix_node, 1))
					for input in input_socket2:
						node_group.links.new(output, input)
			else:
				for link in node_group.links:
					if link.to_socket in input_socket2:
						node_group.links.remove(link)
					elif link.from_node == mix_node and link.to_node == next_mix_node:
						node_group.links.remove(link)

				node_group.links.new(get_mix_node_inputs(next_mix_node, 1), GroupInput.outputs[0])
				for input in input_socket2:
					node_group.links.new(input, GroupInput.outputs[0])

			if layer.type == "Adjustment":
				color_in_node = node_group.nodes.get(f"{layer.name}.color_in")
				if color_in_node:
					input = get_inputs(color_in_node)
				elif layer.effect:
					input = get_inputs(node_group.nodes[f'{layer.name}.Effect.{layer.effect[0].name}'])
				else:
					input = node_group.nodes[f"{layer.name}.Mix"].inputs[3]

				node_group.links.new(get_mix_node_outputs(next_mix_node), input)

			node_group.links.new(get_mix_node_outputs(next_mix_node), get_mix_node_inputs(mix_node, 1))

			next_layer.index -= 1
			layer.index += 1

			compositor.layer.move(self.index, self.index + 1)
			compositor.layer_index = self.index + 1

		elif self.direction == 'DOWN' and self.index > 0:
			last_layer = compositor.layer[self.index-1]

			mix_node = node_group.nodes[f"{layer.name}.Mix"]
			last_mix_node = node_group.nodes[f"{last_layer.name}.Mix"]

			last2_mix_node = None
			if self.index > 1:
				last2_layer = compositor.layer[self.index-2]
				last2_mix_node = node_group.nodes[f"{last2_layer.name}.Mix"]

			input_socket = []
			input_socket2 = []
			input_socket3 = []
			output_socket = []

			for link in node_group.links:
				if link.from_socket == get_mix_node_outputs(mix_node):
					input_socket.append(link.to_socket)

				if link.from_socket == get_mix_node_outputs(last_mix_node):
					input_socket2.append(link.to_socket)

				if link.to_socket == get_mix_node_inputs(last_mix_node, 1):
					if "GroupInput" not in link.from_node.name:
						output_socket.append(link.from_socket)

				if last2_mix_node:
					if link.from_socket == get_mix_node_outputs(last2_mix_node):
						input_socket3.append(link.to_socket)

			for input in input_socket:
				node_group.links.new(get_mix_node_outputs(last_mix_node), input)

			if input_socket3:
				for input in input_socket3:
					node_group.links.new(get_mix_node_outputs(mix_node), input)

			if output_socket:
				for output in output_socket:
					node_group.links.new(output, get_mix_node_inputs(mix_node, 1))
					for input in input_socket2:
						node_group.links.new(output, input)
			else:
				for link in node_group.links:
					if link.to_socket in input_socket2:
						node_group.links.remove(link)
					elif link.from_node == last_mix_node and link.to_node == mix_node:
						node_group.links.remove(link)
						
				node_group.links.new(get_mix_node_inputs(mix_node, 1), GroupInput.outputs[0])
				for input in input_socket2:
					node_group.links.new(input, GroupInput.outputs[0])

			if last_layer.type == "Adjustment":
				color_in_node = node_group.nodes.get(f"{last_layer.name}.color_in")
				if color_in_node:
					input = get_inputs(color_in_node)
				elif last_layer.effect:
					input = get_inputs(node_group.nodes[f'{last_layer.name}.Effect.{last_layer.effect[0].name}'])
				else:
					if bpy.app.version >= (5, 0, 0):
						input = node_group.nodes[f"{layer.name}.Mix"].inputs[3]
					else:
						input = node_group.nodes[f"{layer.name}.Transform"].inputs[0]

				node_group.links.new(get_mix_node_outputs(mix_node), input)

			node_group.links.new(get_mix_node_outputs(mix_node), get_mix_node_inputs(last_mix_node, 1))

			last_layer.index += 1
			layer.index -= 1

			compositor.layer.move(self.index, self.index - 1)
			compositor.layer_index = self.index - 1

		bpy.ops.scene.comp_align_node_tree(name=node_group.name)
		
		# Update viewer to always show top layer
		viewer_node = node_group.nodes.get("Viewer")
		if viewer_node and len(compositor.layer) > 0:
			for link in node_group.links:
				if link.from_socket.node == viewer_node:
					node_group.links.remove(link)
					break
			top_layer = compositor.layer[-1]
			top_mix = node_group.nodes.get(f"{top_layer.name}.Mix")
			if top_mix:
				node_group.links.new(top_mix.outputs[0], viewer_node.inputs[0])
		
		return {"FINISHED"}

class Drag_OT_Layer(bpy.types.Operator):
	bl_idname = "scene.comp_drag_layer"
	bl_label = "Drag Compositor Layer"
	bl_description = "Drag Compositor Layer Socket"
	bl_options = {'REGISTER', 'UNDO'}

	index: bpy.props.IntProperty(options={'HIDDEN'})
	step_counter: int = 0

	layer_matte = {}

	mouse_region_x = None
	mouse_region_y = None

	def modal(self, context, event):
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[self.index]

		if event.type == 'MOUSEMOVE':
			# Increment the step counter
			self.step_counter += 1

			# Check if the step counter reaches the specified interval
			if self.step_counter >= 10:
				if event.mouse_region_y < self.mouse_region_y:
					if self.index > 0:
						bpy.ops.scene.comp_move_layer(index=self.index, direction='DOWN')
						self.index -= 1
				elif event.mouse_region_y > self.mouse_region_y:
					if self.index < len(compositor.layer) - 1:
						bpy.ops.scene.comp_move_layer(index=self.index, direction='UP')
						self.index += 1

				context.area.tag_redraw()
				self.mouse_region_y = event.mouse_region_y

				# Reset the step counter after triggering the operator
				self.step_counter = 0

		if event.type in ('LEFTMOUSE', 'RIGHTMOUSE'):
			layer.drag = False
			for l in compositor.layer:
				l.matte = self.layer_matte[l.name]

			return {'FINISHED'}
		
		return {'RUNNING_MODAL'}
		
	def invoke(self, context, event):
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		layer = compositor.layer[self.index]
		layer.drag = True
		self.mouse_region_x = event.mouse_region_x
		self.mouse_region_y = event.mouse_region_y

		self.layer_matte = {}

		for l in compositor.layer:
			self.layer_matte[l.name] = l.matte

		context.window_manager.modal_handler_add(self)
		return {'RUNNING_MODAL'}

class Edit_OT_Comp_Layer(bpy.types.Operator):
	bl_idname = "scene.comp_edit_comp_layer"
	bl_label = "Edit Compositor Layer"
	bl_description = "Edit Compositor Layer"
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

class COMPOSITOR_MT_add_layer(bpy.types.Menu):
	bl_label = "Layer"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		if layout.operator_context == 'EXEC_REGION_WIN':
			layout.operator_context = 'INVOKE_REGION_WIN'
			layout.operator("WM_OT_search_single_menu", text="Search...",
							icon='VIEWZOOM').menu_idname = "COMPOSITOR_MT_add_layer"
			layout.separator()

		layout.operator_context = 'EXEC_REGION_WIN'
		layout.menu("COMPOSITOR_MT_add_comp_layer", icon = "NODE_COMPOSITING")
		layout.separator()
		add = layout.operator("scene.comp_add_layer", text="Adjustment Layer", icon='STRIP_COLOR_01')
		add.name = "Adjustment Layer"
		add.type = "Adjustment"
		add.icon = 'STRIP_COLOR_01'
		layout.separator()
		for item in layer_node_data:
			if item in layer_node_data_5_2 and bpy.app.version < (5, 2, 0):
				continue
			add = layout.operator("scene.comp_add_layer", text=layer_node_data[item][0], icon=layer_node_data[item][1])
			add.name = layer_node_data[item][0]
			add.type = item
			add.icon = layer_node_data[item][1]

		layout.separator()
		layout.menu("COMPOSITOR_MT_add_texture_layer", icon = "TEXTURE")

class COMPOSITOR_MT_add_comp_layer(bpy.types.Menu):
	bl_label = "Compositor"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		for item in bpy.data.node_groups:
			if item.compositor_props.name != '' and item.name != context.scene.compositing_node_group.name:
				add = layout.operator("scene.comp_add_layer", text=item.name, icon="NODE_COMPOSITING")
				add.name = item.name
				add.type = "Compositor"
				add.icon = "NODE_COMPOSITING"

class COMPOSITOR_MT_add_texture_layer(bpy.types.Menu):
	bl_label = "Texture"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		for item in texture_node_data:
			if item == 'CompositorNodeTexture':
				continue
			add = layout.operator("scene.comp_add_layer", text=texture_node_data[item][0])
			add.name = texture_node_data[item][0]
			add.type = item
			add.icon = texture_node_data[item][1]

class COMPOSITOR_MT_layers_specials(bpy.types.Menu):
	bl_label = "Layer Specials"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		props = context.scene.compositor_layer_props

		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props

		layout = self.layout
		layout.label(text=f"Compositor Version: {compositor.version}", icon = "NODE_COMPOSITING")
		layout.separator()
		layout.operator("wm.call_menu", text="Add Layer", icon='ADD').name = "COMPOSITOR_MT_add_layer"
		if len(compositor.layer) > 0:
			layout.operator("wm.call_menu", text="Add Effect", icon='SHADERFX').name = "COMPOSITOR_MT_add_effects"
			layout.operator("scene.comp_add_mask", text="Add Mask", icon='MOD_MASK')
		layout.separator()
		layout.operator("scene.comp_copy_layer", text="Copy layer from compositor", icon = 'PASTEDOWN', emboss = False)
		layout.separator()
		layout.operator("scene.comp_clear_layer", text="Clear Layer", icon='TRASH', emboss = False)

class COMPOSITOR_PT_Layer_ColorSpace(bpy.types.Panel):
	bl_space_type = 'NODE_EDITOR'
	bl_region_type = 'HEADER'
	bl_label = "In/Out ColorSpace"
	bl_ui_units_x = 14

	def draw(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		item = compositor.layer[compositor.layer_index]

		layout = self.layout
		layout.label(text="In/Out ColorSpace")
		layout.prop(item, "in_colorspace", text="Input")
		layout.prop(item, "out_colorspace", text="Output")

def draw_layer(self, context, box):
	addon_prefs = get_addon_preference(context)

	tree = get_scene_tree(context)
	props = context.scene.compositor_layer_props

	node_group = bpy.data.node_groups[props.compositor_panel]
	compositor = node_group.compositor_props
	
	row = box.row(align=True)
	row.operator("scene.comp_add_layer_media", text="", icon="FILEBROWSER")
	row.operator("wm.call_menu", text="Add Layer", icon='ADD').name = "COMPOSITOR_MT_add_layer"
	if len(compositor.layer) > 0:
		row.operator("wm.call_menu", text="Effects", icon='SHADERFX').name = "COMPOSITOR_MT_add_effects"
	row.menu("COMPOSITOR_MT_layers_specials", icon='DOWNARROW_HLT', text="")
	col = box.column()
	if addon_prefs.search:
		sub = col.row(align=True)
		sub.prop(compositor, "search", text="", icon = "VIEWZOOM")

	filtered = None
	if compositor.search:
		filtered = list(filter(lambda x: any(y in x for y in [compositor.search.lower()]), [layer.name.lower() for layer in compositor.layer]))

	if filtered:
		row = box.row()
		row.active = False
		row.label(text=f'{len(filtered)} result(s) for "{compositor.search}"', icon='VIEWZOOM')
		sub = row.column()
		sub.alignment = 'RIGHT'
		sub.label(text=f'{len(compositor.layer) - len(filtered)} remaining')

	box.template_list("LAYER_UL_LIST", "", compositor, "layer", compositor, "layer_index")
	if len(compositor.layer) > 0:
		item = compositor.layer[compositor.layer_index]
		
		row = box.row(align=True)
		row.label(text="", icon = item.icon)
		row.prop(item, 'name', text="")
		sub = row.row(align=True)
		sub.operator("scene.comp_duplicate_layer", text="", icon='DUPLICATE').index = compositor.layer_index
		row.operator("scene.comp_remove_layer", text="", icon='X').index = compositor.layer_index
		xbox = box.box()
		xrow = xbox.row()
		xrow.label(text = "Properties", icon = "PROPERTIES")
		if item.type == "Compositor" and bpy.data.node_groups.get(item.source):
			xrow.operator("scene.comp_edit_comp_layer", text="Edit Compositor", icon='NODE_COMPOSITING').name = item.source

		mix_node = node_group.nodes.get(f"{item.name}.Mix")

		if addon_prefs.panel_type == "Expand":
			row = xbox.row()
			row.prop(props, 'properties_panel', expand=True)

			if addon_prefs.color_space and props.properties_panel != "Mask":
				row = xbox.row(align=True)
				row.label(text="In/Out ColorSpace", icon="FCURVE")
				row.prop(item, "colorspace", text="")
				row.popover(panel="COMPOSITOR_PT_Layer_ColorSpace", icon='DOWNARROW_HLT', text="")

			if props.properties_panel == "Transfrom":
				xbox.label(text = "Transform", icon = "ORIENTATION_LOCAL")
				col = xbox.column()
				col.use_property_split = True
				col.use_property_decorate = False

				col.prop(mix_node.inputs[0], 'default_value', text="Blend")
				col.prop(mix_node.inputs[1], 'default_value', text="Opacity")
				col.separator()
				row = col.row(align=True)
				row.prop(mix_node.inputs[5], 'default_value', text="Position", index=0)
				row.prop(mix_node.inputs[5], 'default_value', text="", index=1)
				row = col.row(align=True)
				row.prop(mix_node.inputs[7], 'default_value', text="Scale", index=0)
				row.prop(mix_node.inputs[7], 'default_value', text="", index=1)
				col.prop(mix_node.inputs[6], 'default_value', text="Rotation")

				if item.type not in ["Adjustment"]:
					node = node_group.nodes.get(item.name)
					xbox.label(text = "Layer Settings", icon = "CURRENT_FILE")	
					col = xbox.column()
					col.use_property_split = True
					col.use_property_decorate = False
					col.template_node_inputs(node)
					if len(node.outputs) > 1:
						col.separator()
						col.prop(item, "channel", text="Channel")

			elif props.properties_panel == "Effect":
				row = xbox.row(align=True)
				row.label(text = "Effects", icon = "SHADERFX")
				sub = row.row(align=True)
				sub.alignment = 'RIGHT'
				if item.effect:
					sub.prop(item, "fx", text = "", icon = "SHADERFX")
				sub.menu("COMPOSITOR_MT_effects_specials", icon='DOWNARROW_HLT', text="")
				panel_box = xbox.box()
				panel_box.active = item.fx
				if item.effect:
					draw_effect(self, context, panel_box)
				else:
					panel_box.operator("wm.call_menu", text="Add Effects", icon='SHADERFX').name = "COMPOSITOR_MT_add_effects"

			elif props.properties_panel == "Mask":
				row = xbox.row(align=True)
				row.label(text = "Masks", icon = "MOD_MASK")
				sub = row.row(align=True)
				sub.alignment = 'RIGHT'
				sub.prop(item, 'matte', text = "Matte")
				sub.prop(item, 'matte_type',text = "", icon = "FILE_IMAGE" if item.matte_type else "IMAGE_ALPHA", invert_checkbox = item.matte_type)
				sub.prop(item, 'matte_invert',text = "", icon = "MOD_MASK" if item.matte_invert else "SHADING_BBOX", invert_checkbox = item.matte_invert)
				sub.menu("COMPOSITOR_MT_masks_specials", icon='DOWNARROW_HLT', text="")
				panel_box = xbox.box()
				panel_box.operator("scene.comp_add_mask", text="Add Mask", icon='ADD')
				if item.mask:
					draw_mask(self, context, panel_box)

		elif addon_prefs.panel_type == "List":
			col = xbox.column()
			col.use_property_split = True
			col.use_property_decorate = False

			col.prop(mix_node.inputs[0], 'default_value', text="Blend")
			col.prop(mix_node.inputs[1], 'default_value', text="Opacity")

			header, panel = xbox.panel(idname="Transform", default_closed=False)
			header.label(text = "Transform", icon = "ORIENTATION_LOCAL")
			if panel:
				panel_box = panel.box()
				col = panel_box.column()
				col.use_property_split = True
				col.use_property_decorate = False
				row = col.row(align=True)
				row.prop(mix_node.inputs[5], 'default_value', text="Position", index=0)
				row.prop(mix_node.inputs[5], 'default_value', text="", index=1)
				row = col.row(align=True)
				row.prop(mix_node.inputs[7], 'default_value', text="Scale", index=0)
				row.prop(mix_node.inputs[7], 'default_value', text="", index=1)
				col.prop(mix_node.inputs[6], 'default_value', text="Rotation")

			if item.type not in ["Adjustment"]:
				node = node_group.nodes.get(item.name)
				header, panel = xbox.panel(idname=item.name, default_closed=False)
				header.label(text = "Layer Settings", icon = "CURRENT_FILE")
				if panel:	
					panel.use_property_split = True
					panel.use_property_decorate = False
					panel_box = panel.box()
					panel_box.template_node_inputs(node)
					if len(node.outputs) > 1:
						panel_box.prop(item, "channel", text="Channel")

			if addon_prefs.color_space:
				header, panel = xbox.panel(idname="In/Out ColorSpace", default_closed=True)
				header.label(text="In/Out ColorSpace", icon="FCURVE")
				row = header.row(align=True)
				row.alignment = 'RIGHT'
				row.prop(item, "colorspace", text="")
				if panel:
					panel_box = panel.box()
					col = panel_box.column()
					col.use_property_split = True
					col.use_property_decorate = False
					col.prop(item, "in_colorspace", text="Input")
					col.prop(item, "out_colorspace", text="Output")

			header, panel = xbox.panel(idname="Effects", default_closed=False)
			header.label(text = "Effects", icon = "SHADERFX")
			row = header.row(align=True)
			row.alignment = 'RIGHT'
			if item.effect:
				row.prop(item, "fx", text = "", icon = "SHADERFX")
			row.menu("COMPOSITOR_MT_effects_specials", icon='DOWNARROW_HLT', text="")
			if panel:
				panel_box = panel.box()
				panel_box.active = item.fx
				if item.effect:
					draw_effect(self, context, panel_box)
				else:
					panel_box.operator("wm.call_menu", text="Add Effects", icon='SHADERFX').name = "COMPOSITOR_MT_add_effects"

			header, panel = xbox.panel(idname="Masks", default_closed=True)
			header.label(text = "Masks", icon = "MOD_MASK")
			row = header.row(align=True)
			row.alignment = 'RIGHT'
			row.prop(item, 'matte', text = "Matte")
			row.prop(item, 'matte_type',text = "", icon = "FILE_IMAGE" if item.matte_type else "IMAGE_ALPHA", invert_checkbox = item.matte_type)
			row.prop(item, 'matte_invert',text = "", icon = "MOD_MASK" if item.matte_invert else "SHADING_BBOX", invert_checkbox = item.matte_invert)
			row.menu("COMPOSITOR_MT_masks_specials", icon='DOWNARROW_HLT', text="")
			if panel:
				panel_box = panel.box()
				panel_box.operator("scene.comp_add_mask", text="Add Mask", icon='ADD')
				if item.mask:
					draw_mask(self, context, panel_box)

classes = (
	Layer_Props,
	LAYER_UL_LIST,
	Add_OT_Layer,
	Add_OT_Layer_Media,
	Remove_OT_Layer,
	Clear_OT_Layer,
	Duplicate_OT_Layer,
	Copy_OT_Layer,
	Move_OT_Layer,
	Drag_OT_Layer,
	Edit_OT_Comp_Layer,
	COMPOSITOR_MT_add_layer,
	COMPOSITOR_MT_add_comp_layer,
	COMPOSITOR_MT_add_texture_layer,
	COMPOSITOR_MT_layers_specials,
	COMPOSITOR_PT_Layer_ColorSpace,
		  )

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)
