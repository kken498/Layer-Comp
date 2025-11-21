import bpy
from ..defs import *
from .layer import Layer_Props

class Compositor_Props(bpy.types.PropertyGroup):
	def get_name(self):
		return self.get("name", "")

	def set_name(self, value):
		if value == '':
			value = 'Compositor'

		# Check existing layer
		existing_names = [node_group.name for node_group in bpy.data.node_groups if node_group.name != self.sub_name]

		new_name = unique_name(value, existing_names)

		self["name"] = new_name

	def update_name(self, context):
		props = context.scene.compositor_layer_props
		addon_prefs = get_addon_preference(context)

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			tree = get_scene_tree(context)
			group_node = tree.nodes.get(self.sub_name)
			node_group = bpy.data.node_groups.get(self.sub_name)
			if group_node and node_group:
				group_node.name = self.name
				node_group.name = self.name
		else:
			context.scene.compositing_node_group.name = self.name

		props.compositor_panel = self.name

		self.sub_name = self.name

	name : bpy.props.StringProperty(name = "Compositor Name",update=update_name, get=get_name, set=set_name)
	sub_name : bpy.props.StringProperty()

	search : bpy.props.StringProperty(name = "Compositor Search")

	layer : bpy.props.CollectionProperty(name = "Layer", type=Layer_Props)
	layer_index: bpy.props.IntProperty(name = "Layer")
	
class New_OT_Compositor(bpy.types.Operator):
	bl_idname = "scene.comp_new_compositor"
	bl_label = "New Compositor"
	bl_description = "New Compositor"
	bl_options = {'REGISTER', 'UNDO'}

	add_layer : bpy.props.BoolProperty(options={'HIDDEN'}, default=False)
	from_source : bpy.props.BoolProperty(options={'HIDDEN'}, default=False)

	def invoke(self, context, event):
		addon_prefs = get_addon_preference(context)
		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			if self.from_source:
				self.add_layer = False
			else:
				if addon_prefs.new_compositor_option == 'First' and len(get_scene_compositor(context)) == 0:
					self.add_layer = True
				elif addon_prefs.new_compositor_option == 'Any':
					self.add_layer = True

		return self.execute(context)

	def execute(self, context):
		# Define props
		addon_prefs = get_addon_preference(context)
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props
		
		existing_names = [node_group.name for node_group in bpy.data.node_groups]

		name = unique_name("Compositor", existing_names)

		# Create node group
		node_group = bpy.data.node_groups.new(type='CompositorNodeTree', name=name)
		node_group.use_fake_user = True

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			group_node = tree.nodes.new("CompositorNodeGroup")
			group_node.node_tree = node_group
			group_node.name = node_group.name
			group_node.location = (-100,0)

		else:
			context.scene.compositing_node_group = node_group
			tree = get_scene_tree(context)

		item = node_group.compositor_props
		item.sub_name = node_group.name
		item.name = node_group.name

		links = tree.links

		GroupInput = node_group.nodes.new("NodeGroupInput")
		GroupInput.location[0] = -900
		GroupOutput = node_group.nodes.new("NodeGroupOutput")
		GroupOutput.location[0] = 900

		input_socket = node_group.interface.new_socket(name='Empty', in_out='INPUT', socket_type='NodeSocketColor')
		input_socket.default_value = (0, 0, 0, 1)

		output_socket = node_group.interface.new_socket(name='Result', in_out='OUTPUT', socket_type='NodeSocketColor')
		output_socket.hide_value = True

		node_group.links.new(GroupInput.outputs[0], GroupOutput.inputs[0])

		render_node = tree.nodes.get("Render Layers")
		viewer_node = tree.nodes.get("Viewer")

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			if len(get_scene_compositor(context)) > 1:
				sub_node = tree.nodes.get(get_scene_compositor(context)[-2])
				if sub_node:
					group_node.location = (sub_node.location[0],sub_node.location[1]-350)

			if not viewer_node:
				viewer_node = tree.nodes.new("CompositorNodeViewer")
				viewer_node.location = (group_node.location[0] + 200, group_node.location[0] - 50)

			links.new(group_node.outputs[0], viewer_node.inputs[0])
			group_node.inputs[0].default_value = (0,0,0,1)

		props.compositor_panel = node_group.name

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			if render_node and self.add_layer:
				bpy.ops.scene.comp_add_layer(name="Render Layers", icon="RENDER_RESULT", type="Source")
		else:
			bpy.ops.scene.comp_add_layer(name="Render Layers", icon="RENDER_RESULT", type="CompositorNodeRLayers")
				
		if len(get_scene_compositor(context)) == 1:
			bpy.ops.scene.comp_reload_output()
			if props.output:
				props.output[0].composite = node_group.name

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			bpy.ops.scene.comp_reload_source()
		
		self.from_source = False
		self.add_layer = False

		return {"FINISHED"}

class Duplicate_OT_Compositor(bpy.types.Operator):
	bl_idname = "scene.comp_duplicate_compositor"
	bl_label = "Duplicate Compositor"
	bl_description = "Duplicate Compositor"
	bl_options = {'REGISTER', 'UNDO'}

	name : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		addon_prefs = get_addon_preference(context)
		tree = get_scene_tree(context)
		props = context.scene.compositor_layer_props

		links = tree.links
		name = self.name

		# Create node group
		node_group = bpy.data.node_groups[name].copy()
		node_group.compositor_props.sub_name = node_group.name

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			group_node = tree.nodes.new("CompositorNodeGroup")
			group_node.node_tree = node_group
			group_node.location = (-100,0)
			group_node.name = node_group.name

		node_group.compositor_props.name = node_group.name
		
		viewer_node = tree.nodes.get("Viewer")

		input_node = None

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			if len(get_scene_compositor(context)) > 1:
				sub_node = tree.nodes.get(get_scene_compositor(context)[-2])
				if sub_node:
					group_node.location = (sub_node.location[0],sub_node.location[1]-350)
					
			if not viewer_node:
				viewer_node = tree.nodes.new("CompositorNodeViewer")
				viewer_node.location = (group_node.location[0] + 200, group_node.location[0] - 50)

			if input_node:
				links.new(input_node.outputs[0], group_node.inputs[0])
			else:
				links.new(group_node.outputs[0], viewer_node.inputs[0])

			for link in links:
				if link.to_node == tree.nodes[name]:
					links.new(link.from_socket, group_node.inputs[link.to_socket.name])

		props.compositor_panel = node_group.name

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			bpy.ops.scene.comp_reload_source()

		return {"FINISHED"}

class Remove_OT_Compositor(bpy.types.Operator):
	bl_idname = "scene.comp_remove_compositor"
	bl_label = "Remove Compositor"
	bl_description = "Remove Compositor"
	bl_options = {'REGISTER', 'UNDO'}

	name : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		addon_prefs = get_addon_preference(context)
		tree = get_scene_tree(context)
		links = tree.links

		props = context.scene.compositor_layer_props
		
		if self.name:
			name = self.name
		else:
			name = props.compositor_panel

		group_node = tree.nodes.get(name)
		node_group = bpy.data.node_groups.get(name)

		render_node = tree.nodes.get("Render Layers")
		viewer_node = tree.nodes.get("Viewer")

		if len(get_scene_compositor(context)) > 1:
			if name == get_scene_compositor(context)[-1]:
				props.compositor_panel = get_scene_compositor(context)[-2]

		else:
			for link in links:
				if link.to_node == group_node:
					if viewer_node:
						links.new(link.from_node.outputs[0], viewer_node.inputs[0])

		if group_node:
			tree.nodes.remove(group_node)
		if node_group:
			bpy.data.node_groups.remove(node_group)

		if bpy.app.version < (5, 0, 0) or addon_prefs.compositor_type == 'Legacy':
			bpy.ops.scene.comp_reload_source()
		else:
			if props.compositor_panel != "":
				context.scene.compositing_node_group = bpy.data.node_groups[props.compositor_panel]

		return {"FINISHED"}

def draw_compositor(self, context, box):
	props = context.scene.compositor_layer_props

	if bpy.app.version >= (4, 5, 0):
		if len(get_scene_compositor(context)) > 1:
			row = box.row()
			if len(get_scene_compositor(context)) > (context.region.width/75):
				row.prop(props, 'compositor_panel', text="")
			else:
				row.prop(props, 'compositor_panel', expand = True)

	elif bpy.app.version < (4, 5, 0):
		if len(get_scene_compositor(context)) > 1:
			box.prop(props, 'compositor_panel', text="")

	if len(get_scene_compositor(context)) == 0:
		box.operator("scene.comp_new_compositor", text="New Compositor", icon='ADD')
	else:
		node_group = bpy.data.node_groups[props.compositor_panel]
		item = node_group.compositor_props
		row = box.row(align=True)
		row.label(text="", icon = "NODE_COMPOSITING")
		row.prop(item, 'name', text="")
		row.operator("scene.comp_new_compositor", text="", icon='ADD')
		row.operator("scene.comp_duplicate_compositor", text="", icon='DUPLICATE').name = props.compositor_panel
		row.operator("scene.comp_remove_compositor", text="", icon='X')

classes = (
	Compositor_Props,
	New_OT_Compositor,
	Remove_OT_Compositor,
	Duplicate_OT_Compositor,
		  )

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.NodeTree.compositor_props = bpy.props.PointerProperty(type = Compositor_Props)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	del bpy.types.NodeTree.compositor_props
	