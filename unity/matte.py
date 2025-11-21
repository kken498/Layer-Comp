import bpy
from .node import *

class Matte_Props(bpy.types.PropertyGroup):
	def matte_item(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		compositor = node_group.compositor_props
		list = []
		list.append(("None", "None", '', 'BLANK1', 0))
		i = 0
		for item in compositor.layer:
			if item.name != self.name and item.type != "Adjustment":
				list.append((item.name, item.name, '', item.label, i+1))
				i += 1
		return list
	
	def update_matte(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]

		sub_mix_node = node_group.nodes.get(f'{self.name}.Mix_Sub')
		math_node = node_group.nodes.get(f'{self.name}.Mask_Mix')
		matte_node = node_group.nodes.get(f'{self.name}.Matte')
		invert_node = node_group.nodes.get(f'{self.name}.Matte_Invert')

		frame = node_group.nodes.get(f"{self.name}.Frame")
		matte_frame = node_group.nodes.get(f"{self.matte}.Frame")

		matte_sub_mix_node = node_group.nodes.get(f'{self.matte}.Mix_Sub')
		set_matte_node = node_group.nodes.get(f'{self.matte}.Set_Matte')

		if self.matte != 'None':
			matte_math_node = node_group.nodes.get(f'{self.matte}.Mask_Mix')
			mix_node = node_group.nodes.get(f'{self.matte}.Mix')
			transform_node = node_group.nodes.get(f'{self.matte}.Transform')
			if not math_node:
				if bpy.app.version >= (5, 0, 0):
					math_node = node_group.nodes.new('ShaderNodeMath')
				else:
					math_node = node_group.nodes.new('CompositorNodeMath')
				math_node.name = f'{self.name}.Mask_Mix'
				math_node.operation = 'MULTIPLY'
				math_node.inputs[0].default_value = 1
				math_node.inputs[1].default_value = 1
				math_node.parent = frame
				math_node.location = (sub_mix_node.location[0]-150, sub_mix_node.location[1])
				if bpy.app.version >= (4, 5, 0):
					node_group.links.new(math_node.outputs[0], sub_mix_node.inputs[3])
				elif bpy.app.version < (4, 5, 0):
					node_group.links.new(math_node.outputs[0], sub_mix_node.inputs[2])
			if not invert_node:
				invert_node = node_group.nodes.new('CompositorNodeInvert')
				invert_node.name = f'{self.name}.Matte_Invert'
				invert_node.parent = frame
				invert_node.location = (math_node.location[0]-150, math_node.location[1]-100)
				node_group.links.new(invert_node.outputs[0], math_node.inputs[1])
			if not matte_node:
				matte_node = node_group.nodes.new('CompositorNodeSeparateColor')
				matte_node.name = f'{self.name}.Matte'
				matte_node.mode = 'HSL'
				matte_node.parent = frame
				matte_node.location = (invert_node.location[0]-150, invert_node.location[1])
			if not set_matte_node:
				set_matte_node = node_group.nodes.new('CompositorNodeSetAlpha')
				set_matte_node.name = f'{self.matte}.Set_Matte'
				set_matte_node.parent = matte_frame
				set_matte_node.location = (mix_node.location[0], mix_node.location[1]-150)
				node_group.links.new(get_mix_node_outputs(matte_sub_mix_node), set_matte_node.inputs[1])
				node_group.links.new(transform_node.outputs[0], set_matte_node.inputs[0])

			if not matte_math_node:
				if bpy.app.version >= (5, 0, 0):
					matte_math_node = node_group.nodes.new('ShaderNodeMath')
				else:
					matte_math_node = node_group.nodes.new('CompositorNodeMath')
				matte_math_node.name = f'{self.matte}.Mask_Mix'
				matte_math_node.operation = 'MULTIPLY'
				matte_math_node.inputs[0].default_value = 1
				matte_math_node.inputs[1].default_value = 1
				matte_math_node.parent = matte_frame
				matte_math_node.location = (matte_sub_mix_node.location[0]-150, matte_sub_mix_node.location[1])
				if bpy.app.version >= (4, 5, 0):
					node_group.links.new(matte_math_node.outputs[0], matte_sub_mix_node.inputs[3])
				elif bpy.app.version < (4, 5, 0):
					node_group.links.new(matte_math_node.outputs[0], matte_sub_mix_node.inputs[2])

			if self.matte_type:
				node_group.links.new(matte_node.outputs['Blue'], invert_node.inputs['Color'])
			else:
				node_group.links.new(matte_node.outputs['Alpha'], invert_node.inputs['Color'])
			get_invert_node_inputs(invert_node, 'Color', self.matte_invert)
			inputs = matte_node.inputs[0]
			node_group.links.new(set_matte_node.outputs[0], inputs)

		else:
			if matte_node:
				node_group.nodes.remove(matte_node)
			if invert_node:
				node_group.nodes.remove(invert_node)
		
		is_valid = True
		for l in node_group.links:
			if l.is_valid == False:
				is_valid = False
				break

		if is_valid == False:
			for l in node_group.links:
				if l.from_socket == set_matte_node.outputs[0] and l.to_socket == inputs:
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
		matte_node = node_group.nodes.get(f'{self.name}.Matte')
		invert_node = node_group.nodes.get(f'{self.name}.Matte_Invert')
		if matte_node and invert_node:
			if self.matte_type:
				node_group.links.new(matte_node.outputs['Blue'], invert_node.inputs['Color'])
			else:
				node_group.links.new(matte_node.outputs['Alpha'], invert_node.inputs['Color'])

	def update_matte_invert(self, context):
		props = context.scene.compositor_layer_props
		node_group = bpy.data.node_groups[props.compositor_panel]
		invert_node = node_group.nodes.get(f'{self.name}.Matte_Invert')
		if invert_node:
			get_invert_node_inputs(invert_node, 'Color', self.matte_invert)
	
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