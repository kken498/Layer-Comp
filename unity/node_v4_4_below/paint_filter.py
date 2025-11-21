import bpy
from ..node import *

class CompositorNodePaintFilter(bpy.types.CompositorNodeCustomGroup, Node):
	bl_name='CompositorNodePaintFilter'
	bl_label='Paint Filter'
	bl_icon='BRUSHES_ALL'

	def init(self, context):
		self.getNodetree(context)
		self.inputs[1].default_value = 6
		self.inputs[2].default_value = 1
		self.inputs[3].default_value = 1
		self.inputs[4].default_value = 1
		self.inputs[5].default_value = 6
		self.inputs[6].default_value = 0.2
		self.inputs[7].default_value = 0.1
		self.inputs[8].default_value = 1
		self.inputs[9].default_value = 1
		self.inputs[10].default_value = (1.0, 1.0, 1.0, 1.0)
		self.inputs[11].default_value = 0.5

	def getNodetree(self, context):
		#create the private node_group... just for illustration purposes!
		ntname = '.*' + self.bl_name + '_nodetree' #blender hides Nodegroups with name '.*'
		node_tree = self.node_tree = bpy.data.node_groups.new(ntname, 'CompositorNodeTree')
		node_tree.color_tag = 'FILTER'
		node_tree.description = ""

		#node_tree interface
		#Socket Image
		image_socket = node_tree.interface.new_socket(name = "Image", in_out='OUTPUT', socket_type = 'NodeSocketColor')
		image_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket.attribute_domain = 'POINT'
		image_socket.hide_value = True

		#Socket Image
		image_socket_1 = node_tree.interface.new_socket(name = "Image", in_out='INPUT', socket_type = 'NodeSocketColor')
		image_socket_1.default_value = (1.0, 1.0, 1.0, 1.0)
		image_socket_1.attribute_domain = 'POINT'
		image_socket_1.hide_value = True

		#Socket Size
		size_socket = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
		size_socket.default_value = 8.0
		size_socket.min_value = 0.0
		size_socket.max_value = 3.4028234663852886e+38
		size_socket.subtype = 'NONE'
		size_socket.attribute_domain = 'POINT'

		#Socket Base Sharpen
		base_sharpen_socket = node_tree.interface.new_socket(name = "Base Sharpen", in_out='INPUT', socket_type = 'NodeSocketFloat')
		base_sharpen_socket.default_value = 0.3499999940395355
		base_sharpen_socket.min_value = 0.0
		base_sharpen_socket.max_value = 2.0
		base_sharpen_socket.subtype = 'FACTOR'
		base_sharpen_socket.attribute_domain = 'POINT'

		#Socket Sharpen
		sharpen_socket = node_tree.interface.new_socket(name = "Sharpen", in_out='INPUT', socket_type = 'NodeSocketFloat')
		sharpen_socket.default_value = 2.0
		sharpen_socket.min_value = 0.0
		sharpen_socket.max_value = 2.0
		sharpen_socket.subtype = 'FACTOR'
		sharpen_socket.attribute_domain = 'POINT'

		#Socket Mix Kuwahara
		mix_kuwahara_socket = node_tree.interface.new_socket(name = "Mix Kuwahara", in_out='INPUT', socket_type = 'NodeSocketFloat')
		mix_kuwahara_socket.default_value = 1.0
		mix_kuwahara_socket.min_value = 0.0
		mix_kuwahara_socket.max_value = 1.0
		mix_kuwahara_socket.subtype = 'FACTOR'
		mix_kuwahara_socket.attribute_domain = 'POINT'

		#Socket Size
		size_socket_1 = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
		size_socket_1.default_value = 12.0
		size_socket_1.min_value = 0.0
		size_socket_1.max_value = 3.4028234663852886e+38
		size_socket_1.subtype = 'NONE'
		size_socket_1.attribute_domain = 'POINT'

		#Panel Bloom
		bloom_panel = node_tree.interface.new_panel("Bloom")
		#Socket Threshold
		threshold_socket = node_tree.interface.new_socket(name = "Threshold", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bloom_panel)
		threshold_socket.default_value = 0.20000000298023224
		threshold_socket.min_value = 0.0
		threshold_socket.max_value = 3.4028234663852886e+38
		threshold_socket.subtype = 'NONE'
		threshold_socket.attribute_domain = 'POINT'

		#Socket Smoothness
		smoothness_socket = node_tree.interface.new_socket(name = "Smoothness", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bloom_panel)
		smoothness_socket.default_value = 0.10000000149011612
		smoothness_socket.min_value = 0.0
		smoothness_socket.max_value = 1.0
		smoothness_socket.subtype = 'FACTOR'
		smoothness_socket.attribute_domain = 'POINT'

		#Socket Strength
		strength_socket = node_tree.interface.new_socket(name = "Strength", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bloom_panel)
		strength_socket.default_value = 1.0
		strength_socket.min_value = 0.0
		strength_socket.max_value = 1.0
		strength_socket.subtype = 'FACTOR'
		strength_socket.attribute_domain = 'POINT'

		#Socket Saturation
		saturation_socket = node_tree.interface.new_socket(name = "Saturation", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bloom_panel)
		saturation_socket.default_value = 1.0
		saturation_socket.min_value = 0.0
		saturation_socket.max_value = 1.0
		saturation_socket.subtype = 'FACTOR'
		saturation_socket.attribute_domain = 'POINT'

		#Socket Tint
		tint_socket = node_tree.interface.new_socket(name = "Tint", in_out='INPUT', socket_type = 'NodeSocketColor', parent = bloom_panel)
		tint_socket.default_value = (1.0, 1.0, 1.0, 1.0)
		tint_socket.attribute_domain = 'POINT'

		#Socket Size
		size_socket_2 = node_tree.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketFloat', parent = bloom_panel)
		size_socket_2.default_value = 0.5
		size_socket_2.min_value = 0.0
		size_socket_2.max_value = 1.0
		size_socket_2.subtype = 'FACTOR'
		size_socket_2.attribute_domain = 'POINT'



		#initialize node_tree nodes
		#node Group Output
		group_output = node_tree.nodes.new("NodeGroupOutput")
		group_output.name = "Group Output"
		group_output.is_active_output = True

		#node Group Input
		group_input = node_tree.nodes.new("NodeGroupInput")
		group_input.name = "Group Input"

		#node Filter
		filter = node_tree.nodes.new("CompositorNodeFilter")
		filter.name = "Filter"
		filter.filter_type = 'SHARPEN_DIAMOND'

		#node Mix
		mix = node_tree.nodes.new("CompositorNodeMixRGB")
		mix.name = "Mix"
		mix.blend_type = 'MIX'
		mix.use_alpha = False
		mix.use_clamp = False
		#Fac
		mix.inputs[0].default_value = 1.0

		#node Glare 
		glare_ = node_tree.nodes.new("CompositorNodeGlare")
		glare_.name = "Glare "
		glare_.glare_type = 'BLOOM'
		glare_.quality = 'MEDIUM'
		#Maximum Highlights
		glare_.inputs[3].default_value = 0.0

		#node Kuwahara
		kuwahara = node_tree.nodes.new("CompositorNodeKuwahara")
		kuwahara.name = "Kuwahara"
		kuwahara.eccentricity = 2.0
		kuwahara.sharpness = 1.0
		kuwahara.uniformity = 5
		kuwahara.use_high_precision = False
		kuwahara.variation = 'ANISOTROPIC'

		#node Filter.001
		filter_001 = node_tree.nodes.new("CompositorNodeFilter")
		filter_001.name = "Filter.001"
		filter_001.filter_type = 'SHARPEN_DIAMOND'

		#node Mix.001
		mix_001 = node_tree.nodes.new("CompositorNodeMixRGB")
		mix_001.name = "Mix.001"
		mix_001.blend_type = 'MIX'
		mix_001.use_alpha = False
		mix_001.use_clamp = False

		#node Kuwahara.001
		kuwahara_001 = node_tree.nodes.new("CompositorNodeKuwahara")
		kuwahara_001.name = "Kuwahara.001"
		kuwahara_001.eccentricity = 1.0
		kuwahara_001.sharpness = 1.0
		kuwahara_001.uniformity = 5
		kuwahara_001.use_high_precision = False
		kuwahara_001.variation = 'ANISOTROPIC'

		#Set locations
		group_output.location = (703.8403930664062, 0.0)
		group_input.location = (-713.8404541015625, 0.0)
		filter.location = (-513.8404541015625, 95.6823501586914)
		mix.location = (-176.56655883789062, 132.47967529296875)
		glare_.location = (-332.58953857421875, -61.28557586669922)
		kuwahara.location = (38.3214111328125, 91.04048156738281)
		filter_001.location = (274.08184814453125, 73.52950286865234)
		mix_001.location = (513.8404541015625, 44.45295333862305)
		kuwahara_001.location = (43.31060791015625, -132.47967529296875)

		#Set dimensions
		group_output.width, group_output.height = 140.0, 100.0
		group_input.width, group_input.height = 140.0, 100.0
		filter.width, filter.height = 140.0, 100.0
		mix.width, mix.height = 140.0, 100.0
		glare_.width, glare_.height = 140.0, 100.0
		kuwahara.width, kuwahara.height = 140.0, 100.0
		filter_001.width, filter_001.height = 140.0, 100.0
		mix_001.width, mix_001.height = 140.0, 100.0
		kuwahara_001.width, kuwahara_001.height = 140.0, 100.0

		#initialize node_tree links
		#filter.Image -> kuwahara_001.Image
		node_tree.links.new(filter.outputs[0], kuwahara_001.inputs[0])
		#mix.Image -> kuwahara.Image
		node_tree.links.new(mix.outputs[0], kuwahara.inputs[0])
		#kuwahara_001.Image -> mix_001.Image
		node_tree.links.new(kuwahara_001.outputs[0], mix_001.inputs[2])
		#glare_.Image -> mix.Image
		node_tree.links.new(glare_.outputs[0], mix.inputs[2])
		#filter.Image -> mix.Image
		node_tree.links.new(filter.outputs[0], mix.inputs[1])
		#filter_001.Image -> mix_001.Image
		node_tree.links.new(filter_001.outputs[0], mix_001.inputs[1])
		#kuwahara.Image -> filter_001.Image
		node_tree.links.new(kuwahara.outputs[0], filter_001.inputs[1])
		#group_input.Image -> filter.Image
		node_tree.links.new(group_input.outputs[0], filter.inputs[1])
		#mix_001.Image -> group_output.Image
		node_tree.links.new(mix_001.outputs[0], group_output.inputs[0])
		#group_input.Size -> kuwahara.Size
		node_tree.links.new(group_input.outputs[1], kuwahara.inputs[1])
		#group_input.Base Sharpen -> filter.Fac
		node_tree.links.new(group_input.outputs[2], filter.inputs[0])
		#group_input.Sharpen -> filter_001.Fac
		node_tree.links.new(group_input.outputs[3], filter_001.inputs[0])
		#group_input.Size -> kuwahara_001.Size
		node_tree.links.new(group_input.outputs[5], kuwahara_001.inputs[1])
		#group_input.Mix Kuwahara -> mix_001.Fac
		node_tree.links.new(group_input.outputs[4], mix_001.inputs[0])
		#filter.Image -> glare_.Image
		node_tree.links.new(filter.outputs[0], glare_.inputs[0])
		#group_input.Threshold -> glare_.Threshold
		node_tree.links.new(group_input.outputs[6], glare_.inputs[1])
		#group_input.Smoothness -> glare_.Smoothness
		node_tree.links.new(group_input.outputs[7], glare_.inputs[2])
		#group_input.Strength -> glare_.Strength
		node_tree.links.new(group_input.outputs[8], glare_.inputs[4])
		#group_input.Saturation -> glare_.Saturation
		node_tree.links.new(group_input.outputs[9], glare_.inputs[5])
		#group_input.Tint -> glare_.Tint
		node_tree.links.new(group_input.outputs[10], glare_.inputs[6])
		#group_input.Size -> glare_.Size
		node_tree.links.new(group_input.outputs[11], glare_.inputs[7])
		return node_tree
