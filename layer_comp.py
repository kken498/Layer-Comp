import bpy
from .defs import *
from .unity.output import Output_Props
from itertools import chain
from bpy.app.translations import (
    pgettext_rpt as rpt_,
)

class Compositing_Layer_Props(bpy.types.PropertyGroup):
	def update_panel(self, context):
		if self.panel == 'Compositor':
			bpy.ops.scene.comp_reload_source()
		elif self.panel == 'Output':
			bpy.ops.scene.comp_reload_output()
		
	def compositor_item(self, context):
		list = []
		for i, item in enumerate(get_scene_compositor(context)):
			list.append((item, item, '', "NODE_COMPOSITING", i))
		return list
	
	def update_compositor_panel(self, context):
		context.scene.compositing_node_group = bpy.data.node_groups.get(self.compositor_panel)

	def panel_item(self, context):
		items = []
		items.append(('Compositor', 'Compositor', ''))
		items.append(('Output', 'Output', ''))
		return items

	panel : bpy.props.EnumProperty(
							name='Compositor Layer Panel', 
							items = panel_item,
							update=update_panel
									)
	properties_panel : bpy.props.EnumProperty(default = "Transfrom",
							items = [('Transfrom', 'Transfroms', ''),
									('Effect', 'Effect Controls', ''),
									('Mask', 'Masks', ''),
									],
							description = "Properties Panel"
									)

	compositor_panel : bpy.props.EnumProperty(
						name='Compositor Panel',
						description = "Compositor Panel",
						items = compositor_item,
						update=update_compositor_panel
								)

	output : bpy.props.CollectionProperty(type=Output_Props)
	output_index: bpy.props.IntProperty(name = "Output")

class Align_OT_Node_Tree(bpy.types.Operator):
	bl_idname = "scene.comp_align_node_tree"
	bl_label = "Align Node Tree"
	bl_description = "Align Node Tree"
	bl_options = {'REGISTER', 'UNDO'}

	name : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		# Define props
		node_group = bpy.data.node_groups[self.name]
		compositor = node_group.compositor_props
		GroupInput = node_group.nodes.get("Group Input")
		GroupOutput = node_group.nodes.get("Group Output")
		viewer_node = node_group.nodes.get("Viewer")

		frame = None

		for i, layer in enumerate(compositor.layer):
			frame = node_group.nodes.get(f"{layer.name}.Frame")
			if frame:
				if i > 0:
					last_frame = node_group.nodes.get(f"{compositor.layer[i-1].name}.Frame")
					if last_frame:
						frame.location = (last_frame.location[0] + last_frame.width + 200, last_frame.location[1])
				else:
					frame.location = (GroupInput.location[0] + GroupInput.width + 200, GroupInput.location[1])

		if frame:
			GroupOutput.location = (frame.location[0] + frame.width + 200, frame.location[1])
			viewer_node.location = (GroupOutput.location[0], GroupOutput.location[1] + 250)
			for node in node_group.nodes:
				if node.type == "OUTPUT_FILE":
					node.location = (GroupOutput.location[0], node.location[1])

		return {"FINISHED"}

class Rest_OT_Node(bpy.types.Operator):
	bl_idname = "scene.comp_rest_node"
	bl_label = "Rest Node"
	bl_description = "Rest Node"
	bl_options = {'REGISTER', 'UNDO'}

	node_group : bpy.props.StringProperty(options={'HIDDEN'})
	node : bpy.props.StringProperty(options={'HIDDEN'})

	def execute(self, context):
		node_group = bpy.data.node_groups[self.node_group]
		node_active = node_group.nodes.get(self.node)

		node_selected = [node_active]
		node_ignore = ["FRAME", "REROUTE", "SIMULATION_INPUT", "SIMULATION_OUTPUT"]

		active_node_name = node_active.name if node_active.select else None
		valid_nodes = [n for n in node_selected if n.type not in node_ignore]

		# Create output lists
		selected_node_names = [n.name for n in node_selected]
		success_names = []

		# Reset all valid children in a frame
		node_active_is_frame = False
		if len(node_selected) == 1 and node_active.type == "FRAME":
			node_tree = node_active.id_data
			children = [n for n in node_tree.nodes if n.parent == node_active]
			if children:
				valid_nodes = [n for n in children if n.type not in node_ignore]
				selected_node_names = [n.name for n in children if n.type not in node_ignore]
				node_active_is_frame = True

		# Check if valid nodes in selection
		if not (len(valid_nodes) > 0):
			# Check for frames only
			frames_selected = [n for n in node_selected if n.type == "FRAME"]
			if (len(frames_selected) > 1 and len(frames_selected) == len(node_selected)):
				self.report({'ERROR'}, "Please select only 1 frame to reset")
			else:
				self.report({'ERROR'}, "No valid node(s) in selection")
			return {'CANCELLED'}

		# Report nodes that are not valid
		if len(valid_nodes) != len(node_selected) and node_active_is_frame is False:
			valid_node_names = [n.name for n in valid_nodes]
			not_valid_names = list(set(selected_node_names) - set(valid_node_names))
			self.report({'INFO'}, rpt_("Ignored {}").format(", ".join(not_valid_names)))

		# Deselect all nodes
		for i in node_selected:
			i.select = False

		# Run through all valid nodes
		for node in valid_nodes:

			parent = node.parent if node.parent else None
			node_loc = [node.location.x, node.location.y]
			node_mute = node.mute

			node_tree = node.id_data
			props_to_copy = 'bl_idname name location height width'.split(' ')

			reconnections = []
			mappings = chain.from_iterable([node.inputs, node.outputs])
			for i in (i for i in mappings if i.is_linked):
				for L in i.links:
					reconnections.append([L.from_node.name, L.from_socket.name, L.to_node.name, L.to_socket.name])

			props = {j: getattr(node, j) for j in props_to_copy}

			new_node = node_tree.nodes.new(props['bl_idname'])
			props_to_copy.pop(0)

			for prop in props_to_copy:
				setattr(new_node, prop, props[prop])

			if node.type == "GROUP":
				new_node.node_tree = node.node_tree

			nodes = node_tree.nodes
			nodes.remove(node)
			new_node.name = props['name']

			if parent:
				new_node.parent = parent
				new_node.location = node_loc

			new_node.mute = node_mute

			for link in reconnections:
				node_group.links.new(node_group.nodes[link[0]].outputs[link[1]], node_group.nodes[link[2]].inputs[link[3]])

			new_node.select = False
			success_names.append(new_node.name)

		# Reselect all nodes
		if selected_node_names and node_active_is_frame is False:
			for i in selected_node_names:
				node_tree.nodes[i].select = True

		if active_node_name is not None:
			node_tree.nodes[active_node_name].select = True
			node_tree.nodes.active = node_tree.nodes[active_node_name]

		message = rpt_("Successfully reset {}").format(", ".join(success_names))
		self.report({'INFO'}, message)
		return {'FINISHED'}

classes = (
	Compositing_Layer_Props,
	Align_OT_Node_Tree,
	Rest_OT_Node,
		  )

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.Scene.compositor_layer_props = bpy.props.PointerProperty(type = Compositing_Layer_Props)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	del bpy.types.Scene.compositor_layer_props
