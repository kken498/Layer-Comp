import bpy
from ..defs import *

class Matte_Props(bpy.types.PropertyGroup):
	def matte_item(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		list = []
		list.append(("None", "None", '', 'BLANK1', 0))
		i = 0
		for index, item in enumerate(compositor.layer):
			if self.index > index:
				if item.name != self.name and item.type != "Adjustment":
					list.append((item.name, item.name, '', item.label, i+1))
					i += 1
		return list
	
	def update_matte(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]

		mix_node = node_group.nodes.get(f'{self.name}.Mix')
		matte_mix_node = node_group.nodes.get(f'{self.matte}.Mix')

		if self.matte != 'None':
			node_group.links.new(matte_mix_node.outputs[1], mix_node.inputs['Matte'])
		else:
			for l in node_group.links:
				if l.to_socket == mix_node.inputs['Matte']:
					node_group.links.remove(l)
					break

		is_valid = True
		for l in node_group.links:
			if l.is_valid == False:
				is_valid = False
				break

		if is_valid == False:
			for l in node_group.links:
				if l.to_socket == mix_node.inputs['Matte']:
					node_group.links.remove(l)
					break

			self.matte = 'None'

		elif is_valid == True:	
			compositor = node_group.compositor_props

			if compositor.layer.get(self.matte):
				
				if compositor.layer[self.matte].is_matte == False:
					compositor.layer[self.matte].hide = True
			
			is_matte = []
			for layer in compositor.layer:
				if layer.matte != "None":
					is_matte.append(layer.matte)

			for layer in compositor.layer:
				if layer.name in is_matte:
					layer.is_matte = True
				else:
					layer.is_matte = False


	def update_matte_type(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		mix_node = node_group.nodes.get(f'{self.name}.Mix')
		if self.matte_type:
			mix_node.inputs[10].default_value = "Lightness"
		else:
			mix_node.inputs[10].default_value = "Alpha"

	def update_matte_invert(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		mix_node = node_group.nodes.get(f'{self.name}.Mix')
		mix_node.inputs[11].default_value = self.matte_invert

	matte : bpy.props.EnumProperty(
					name='Matte Layer', 
					description = "Select matte layer (inherit transparency from the track matte layer's alpha channel or luminance)",
					items = matte_item,
					update = update_matte
							)

	matte_type : bpy.props.BoolProperty(name='Matte Type',
									 description = "Click to switch Alpha/Luma Matte",
									 update = update_matte_type)
	
	matte_invert : bpy.props.BoolProperty(name='Invert Matte',
									   description = "Click to invert the matte",
									   update = update_matte_invert)
	
	is_matte : bpy.props.BoolProperty()
