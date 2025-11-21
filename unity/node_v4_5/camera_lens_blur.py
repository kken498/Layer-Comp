import bpy
from ..node import *

class CompositorNodeCameraLensBlur(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodeCameraLensBlur'
	bl_label='Camera Lens Blur'
	bl_icon='VIEW_CAMERA'

	def init(self, context):
		self.getNodetree(context)
		self.inputs["Blur"].default_value = 1.0
		self.inputs["Bounding Box"].default_value = 1.0
		self.inputs["Side"].default_value = 5

	def draw_buttons(self, context, layout):
		return

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = "FILTER"

		GroupInput = node_tree.nodes.new('NodeGroupInput')
		GroupOutput = node_tree.nodes.new('NodeGroupOutput')
		BokehImage = node_tree.nodes.new('CompositorNodeBokehImage')
		BokehBlur = node_tree.nodes.new('CompositorNodeBokehBlur')

		result_socket = node_tree.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")

		image_socket = node_tree.interface.new_socket(name="Image", in_out="INPUT", socket_type="NodeSocketColor")
		image_socket.hide_value = True

		blur_socket = node_tree.interface.new_socket(name="Blur", in_out="INPUT", socket_type="NodeSocketFloat")
		blur_socket.default_value = 1.0
		blur_socket.min_value = 0.0
		blur_socket.max_value = 10.0

		box_socket = node_tree.interface.new_socket(name="Bounding Box", in_out="INPUT", socket_type="NodeSocketFloat")
		box_socket.default_value = 1.0
		box_socket.min_value = 0.0
		box_socket.max_value = 1.0

		box_socket = node_tree.interface.new_socket(name="Extend Bounds", in_out="INPUT", socket_type="NodeSocketBool")

		bokeh_panel = node_tree.interface.new_panel(name="Bokeh", description='', default_closed=False)

		flaps_socket = node_tree.interface.new_socket(name="Side", in_out="INPUT", socket_type="NodeSocketInt", description="The number of flaps in the bokeh")
		flaps_socket.default_value = 5
		flaps_socket.min_value = 3
		flaps_socket.max_value = 24

		node_tree.interface.move_to_parent(flaps_socket, bokeh_panel, 0)

		angle_socket = node_tree.interface.new_socket(name="Angle", in_out="INPUT", socket_type="NodeSocketFloat", description="The angle of the bokeh")
		angle_socket.subtype = 'ANGLE'

		node_tree.interface.move_to_parent(angle_socket, bokeh_panel, 1)

		roundness_socket = node_tree.interface.new_socket(name="Roundness", in_out="INPUT", socket_type="NodeSocketFloat", description="Specifies how round the bokeh is, maximum roundness produces a circular bokeh")
		roundness_socket.default_value = 0
		roundness_socket.min_value = 0
		roundness_socket.max_value = 1.0
		roundness_socket.subtype = 'FACTOR'

		node_tree.interface.move_to_parent(roundness_socket, bokeh_panel, 2)

		catadioptric_socket = node_tree.interface.new_socket(name="Catadioptric Size", in_out="INPUT", socket_type="NodeSocketFloat", description="Specifies the size of the catadioptric iris, zero means no iris")
		catadioptric_socket.default_value = 0
		catadioptric_socket.min_value = 0
		catadioptric_socket.max_value = 1.0
		catadioptric_socket.subtype = 'FACTOR'

		node_tree.interface.move_to_parent(catadioptric_socket, bokeh_panel, 3)

		color_shift_socket = node_tree.interface.new_socket(name="Color Shift", in_out="INPUT", socket_type="NodeSocketFloat", description="Specifies the amount of color shifting. 1 means maximum shifting towards blue while -1 means maximum shifting toward red")
		color_shift_socket.default_value = 0
		color_shift_socket.min_value = -1.0
		color_shift_socket.max_value = 1.0
		color_shift_socket.subtype = 'FACTOR'

		node_tree.interface.move_to_parent(color_shift_socket, bokeh_panel, 4)

		node_tree.links.new(GroupInput.outputs['Side'], BokehImage.inputs['Flaps'])
		node_tree.links.new(GroupInput.outputs['Angle'], BokehImage.inputs['Angle'])
		node_tree.links.new(GroupInput.outputs['Roundness'], BokehImage.inputs['Roundness'])
		node_tree.links.new(GroupInput.outputs['Catadioptric Size'], BokehImage.inputs['Catadioptric Size'])
		node_tree.links.new(GroupInput.outputs['Color Shift'], BokehImage.inputs['Color Shift'])

		node_tree.links.new(GroupInput.outputs['Image'], BokehBlur.inputs['Image'])
		node_tree.links.new(BokehImage.outputs['Image'], BokehBlur.inputs['Bokeh'])

		node_tree.links.new(GroupInput.outputs['Blur'], BokehBlur.inputs['Size'])
		node_tree.links.new(GroupInput.outputs['Bounding Box'], BokehBlur.inputs['Bounding box'])
		node_tree.links.new(GroupInput.outputs['Extend Bounds'], BokehBlur.inputs['Extend Bounds'])

		node_tree.links.new(BokehBlur.outputs['Image'], GroupOutput.inputs['Image'])

		return node_tree
