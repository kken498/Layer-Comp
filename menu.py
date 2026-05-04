import bpy
from .defs import *
from .unity.node_data import *

class CompositorAddMenu:

	@classmethod
	def operator_add_effect(cls, layout, name):
		if name in effect_node_data:
			data = effect_node_data[name]
			layout.operator(
				"scene.comp_add_effect",
				text=data[0],
				text_ctxt=data[0],
				icon=data[1],
			).type = name

		elif name in feature_node_data:
			data = feature_node_data[name]
			add = layout.operator("scene.comp_append_effect",text=data[0], text_ctxt=data[0], icon=data[1])
			add.name = data[0]
			add.type = "v5_0"
			add.file = 'Presets'
			add.icon = data[1]

	@classmethod
	def operator_add_node(cls, layout, name):
		data = feature_node_data[name]
		add = layout.operator("scene.append_presets_node",text=data[0], text_ctxt=data[0], icon=data[1])
		add.name = data[0]
		add.type = "v5_0"
		add.file = 'Presets'

	@classmethod
	def operator_append_essentials_effect(cls, layout, name):
		add = layout.operator("scene.comp_append_essentials_effect",text=name)
		add.name = name
		add.type = name		

class COMPOSITOR_MT_add_effects(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Effect"
	bl_options = {'SEARCH_ON_KEY_PRESS'}


	def draw(self, context):
		layout = self.layout
		if layout.operator_context == 'EXEC_REGION_WIN':
			layout.operator_context = 'INVOKE_REGION_WIN'
			layout.operator("WM_OT_search_single_menu", text="Search...",
							icon='VIEWZOOM').menu_idname = "COMPOSITOR_MT_add_effects"
			layout.separator()

		layout.operator_context = 'EXEC_REGION_WIN'
		layout.menu("COMPOSITOR_MT_add_effects_adjustment")
		layout.menu("COMPOSITOR_MT_add_effects_filter")
		layout.menu("COMPOSITOR_MT_add_effects_blur")
		layout.menu("COMPOSITOR_MT_add_effects_keying")
		layout.menu("COMPOSITOR_MT_add_effects_transform")
		layout.separator()
		layout.label(text="Feature", icon="SHADERFX")
		layout.menu("COMPOSITOR_MT_add_effects_features_color")
		layout.menu("COMPOSITOR_MT_add_effects_features_camera")
		layout.menu("COMPOSITOR_MT_add_effects_features_looks")
		layout.menu("COMPOSITOR_MT_add_effects_features_3d")
		layout.menu("COMPOSITOR_MT_add_effects_features_other")
		layout.separator()
		layout.menu("COMPOSITOR_MT_add_effects_presets", icon="PRESET")
		#layout.menu("COMPOSITOR_MT_add_effects_asset_browser", icon="ASSET_MANAGER")

class COMPOSITOR_MT_add_effects_adjustment(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Adjustment"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, "CompositorNodeBrightContrast")
		self.operator_add_effect(layout, "ShaderNodeValToRGB")
		self.operator_add_effect(layout, "CompositorNodeColorBalance")
		self.operator_add_effect(layout, "CompositorNodeColorCorrection")
		self.operator_add_effect(layout, "CompositorNodeExposure")
		self.operator_add_effect(layout, "ShaderNodeGamma")
		self.operator_add_effect(layout, "CompositorNodeHueCorrect")
		self.operator_add_effect(layout, "CompositorNodeHueSat")
		self.operator_add_effect(layout, "CompositorNodeCurveRGB")
		self.operator_add_effect(layout, "CompositorNodeTonemap")
		self.operator_add_effect(layout, "CompositorNodeInvert")
		self.operator_add_effect(layout, "CompositorNodeRGBToBW")
		self.operator_add_effect(layout, "CompositorNodeConvertColorSpace")
		self.operator_add_effect(layout, "CompositorNodeConvertToDisplay")
		self.operator_add_effect(layout, "CompositorNodeZcombine")
		self.operator_add_effect(layout, "CompositorNodeSeparateColor")

		layout.separator()
		self.operator_add_effect(layout, "CompositorNodeAlphaOver")
		self.operator_add_effect(layout, "CompositorNodeSetAlpha")
		self.operator_add_effect(layout, "CompositorNodePremulKey")
		
class COMPOSITOR_MT_add_effects_filter(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Filter"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout

		self.operator_add_effect(layout, "CompositorNodeAntiAliasing")
		self.operator_add_effect(layout, "CompositorNodeConvolve")
		self.operator_add_effect(layout, "CompositorNodeDespeckle")
		self.operator_add_effect(layout, "CompositorNodeInpaint")
		self.operator_add_effect(layout, "CompositorNodeFilter")
		self.operator_add_effect(layout, "CompositorNodeGlare")
		self.operator_add_effect(layout, "CompositorNodeKuwahara")
		self.operator_add_effect(layout, "CompositorNodePixelate")
		self.operator_add_effect(layout, "CompositorNodePosterize")
		self.operator_add_effect(layout, "CompositorNodeLensdist")

class COMPOSITOR_MT_add_effects_blur(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Blur"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, "CompositorNodeBlur")
		self.operator_add_effect(layout, "CompositorNodeBokehBlur")
		self.operator_add_effect(layout, "CompositorNodeBilateralblur")
		self.operator_add_effect(layout, "CompositorNodeDefocus")
		self.operator_add_effect(layout, "CompositorNodeDBlur")

class COMPOSITOR_MT_add_effects_keying(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Keying"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, "CompositorNodeCryptomatte")
		layout.separator()
		self.operator_add_effect(layout, "CompositorNodeChannelMatte")
		self.operator_add_effect(layout, "CompositorNodeChromaMatte")
		self.operator_add_effect(layout, "CompositorNodeColorMatte")
		self.operator_add_effect(layout, "CompositorNodeColorSpill")
		self.operator_add_effect(layout, "CompositorNodeDistanceMatte")
		self.operator_add_effect(layout, "CompositorNodeKeying")
		self.operator_add_effect(layout, "CompositorNodeLumaMatte")

class COMPOSITOR_MT_add_effects_transform(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Transform"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, "CompositorNodeTransform")
		self.operator_add_effect(layout, "CompositorNodeTranslate")
		self.operator_add_effect(layout, "CompositorNodeRotate")
		self.operator_add_effect(layout, "CompositorNodeScale")
		layout.separator()
		self.operator_add_effect(layout, "CompositorNodeCornerPin")
		self.operator_add_effect(layout, "CompositorNodeCrop")
		self.operator_add_effect(layout, "CompositorNodeDisplace")
		self.operator_add_effect(layout, "CompositorNodeFlip")

class COMPOSITOR_MT_add_effects_features(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Features"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		version = bpy.app.version
		layout = self.layout
		layout.menu("COMPOSITOR_MT_add_effects_features_color")
		layout.menu("COMPOSITOR_MT_add_effects_features_looks")
		layout.menu("COMPOSITOR_MT_add_effects_features_3d")
		layout.menu("COMPOSITOR_MT_add_effects_features_other")

class COMPOSITOR_MT_add_effects_features_color(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Color"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, "CompositorNodeFill")
		self.operator_add_effect(layout, "CompositorNodeSpotFill")
		self.operator_add_effect(layout, "CompositorNodeColorSelection")
		self.operator_add_effect(layout, "CompositorNodeColorReplace")
		self.operator_add_effect(layout, "CompositorNodeColorInnerShadow")
		self.operator_add_effect(layout, "CompositorNodeColorInnerShadowSingle")
		self.operator_add_effect(layout, "CompositorNodeColorRimLight")
		self.operator_add_effect(layout, "CompositorNodeDropShadow")
		self.operator_add_effect(layout, "CompositorNodeInnerShadow")
		self.operator_add_effect(layout, "CompositorNodeOuterGlow")
		self.operator_add_effect(layout, "CompositorNodeBoundaryLine")
		self.operator_add_effect(layout, "CompositorNodeUnmult")
		self.operator_add_effect(layout, "CompositorNodeSeparateRGBA")

class COMPOSITOR_MT_add_effects_features_camera(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Camera"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, "CompositorNodeAutoExposure")
		self.operator_add_effect(layout, "CompositorNodeSpotExposure")
		self.operator_add_effect(layout, "CompositorNodeCameraLensBlur")
		self.operator_add_effect(layout, "CompositorNodeLensDirt")
		self.operator_add_effect(layout, "CompositorNodeSwingTilt")
		self.operator_add_effect(layout, "CompositorNodeShutterStreak")
		self.operator_add_effect(layout, "CompositorNodeChromaticAberration")
		self.operator_add_effect(layout, "CompositorNodeVignette")
		self.operator_add_effect(layout, "CompositorNodeEdgeSoftness")
		self.operator_add_effect(layout, "CompositorNodeRadialBlur")
		self.operator_add_effect(layout, "CompositorNodeRenoiser")

class COMPOSITOR_MT_add_effects_features_looks(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Looks"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		version = bpy.app.version
		layout = self.layout
		self.operator_add_effect(layout, "CompositorNodeHalation")
		self.operator_add_effect(layout, "CompositorNodePaintFilter")
		self.operator_add_effect(layout, "CompositorNodeBlurRGB")
		self.operator_add_effect(layout, "CompositorNodeTwitch")

class COMPOSITOR_MT_add_effects_features_3d(CompositorAddMenu, bpy.types.Menu):
	bl_label = "3D"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, "CompositorNodeRelight")
		self.operator_add_effect(layout, "CompositorNodeRimLight")
		self.operator_add_effect(layout, "CompositorNodeSceneRimLight")

class COMPOSITOR_MT_add_effects_features_other(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Other"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_effect(layout, "CompositorNodeWiggleTransfrom")
		self.operator_add_effect(layout, "CompositorNodeTile")

class COMPOSITOR_MT_add_effects_presets(bpy.types.Menu):
	bl_label = "Presets"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		presets = get_presets('Effects')
		layout = self.layout
		if len(presets) > 0:
			for preset in presets:
				add = layout.operator("scene.comp_append_effect_preset",text=preset)
				add.preset = preset
				add.type = "COMP"
		else:
			layout.label(text="No Preset")

class COMPOSITOR_MT_add_nodes_features(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Feature"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		version = bpy.app.version
		layout = self.layout
		layout.menu("COMPOSITOR_MT_add_nodes_features_color")
		layout.menu("COMPOSITOR_MT_add_nodes_features_camera")
		layout.menu("COMPOSITOR_MT_add_nodes_features_looks")
		layout.menu("COMPOSITOR_MT_add_nodes_features_3d")
		layout.menu("COMPOSITOR_MT_add_nodes_features_other")

class COMPOSITOR_MT_add_nodes_features_color(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Color"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_node(layout, "CompositorNodeFill")
		self.operator_add_node(layout, "CompositorNodeSpotFill")
		self.operator_add_node(layout, "CompositorNodeColorSelection")
		self.operator_add_node(layout, "CompositorNodeColorReplace")
		self.operator_add_node(layout, "CompositorNodeColorInnerShadow")
		self.operator_add_node(layout, "CompositorNodeColorInnerShadowSingle")
		self.operator_add_node(layout, "CompositorNodeColorRimLight")
		self.operator_add_node(layout, "CompositorNodeDropShadow")
		self.operator_add_node(layout, "CompositorNodeInnerShadow")
		self.operator_add_node(layout, "CompositorNodeOuterGlow")
		self.operator_add_node(layout, "CompositorNodeBoundaryLine")
		self.operator_add_node(layout, "CompositorNodeUnmult")
		self.operator_add_node(layout, "CompositorNodeSeparateRGBA")

class COMPOSITOR_MT_add_nodes_features_camera(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Camera"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_node(layout, "CompositorNodeAutoExposure")
		self.operator_add_node(layout, "CompositorNodeSpotExposure")
		self.operator_add_node(layout, "CompositorNodeCameraLensBlur")
		self.operator_add_node(layout, "CompositorNodeLensDirt")
		self.operator_add_node(layout, "CompositorNodeSwingTilt")
		self.operator_add_node(layout, "CompositorNodeShutterStreak")
		self.operator_add_node(layout, "CompositorNodeChromaticAberration")
		self.operator_add_node(layout, "CompositorNodeVignette")
		self.operator_add_node(layout, "CompositorNodeEdgeSoftness")
		self.operator_add_node(layout, "CompositorNodeRadialBlur")
		self.operator_add_node(layout, "CompositorNodeRenoiser")

class COMPOSITOR_MT_add_nodes_features_looks(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Looks"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		version = bpy.app.version
		layout = self.layout
		self.operator_add_node(layout, "CompositorNodeHalation")
		self.operator_add_node(layout, "CompositorNodePaintFilter")
		self.operator_add_node(layout, "CompositorNodeBlurRGB")
		self.operator_add_node(layout, "CompositorNodeTwitch")

class COMPOSITOR_MT_add_nodes_features_3d(CompositorAddMenu, bpy.types.Menu):
	bl_label = "3D"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_node(layout, "CompositorNodeRelight")
		self.operator_add_node(layout, "CompositorNodeRimLight")
		self.operator_add_node(layout, "CompositorNodeSceneRimLight")

class COMPOSITOR_MT_add_nodes_features_other(CompositorAddMenu, bpy.types.Menu):
	bl_label = "Other"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		self.operator_add_node(layout, "CompositorNodeWiggleTransfrom")
		self.operator_add_node(layout, "CompositorNodeTile")

class COMPOSITOR_MT_add_nodes_presets(bpy.types.Menu):
	bl_label = "Presets"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		presets = get_presets('Effects')
		layout = self.layout
		if len(presets) > 0:
			for preset in presets:
				add = layout.operator("scene.comp_append_effect_preset",text=preset)
				add.preset = preset
				add.type = ""
		else:
			layout.label(text="No Preset")

class COMPOSITOR_MT_add_effects_asset_browser(bpy.types.Menu):
	bl_label = "Asset Browser"
	bl_options = {'SEARCH_ON_KEY_PRESS'}
	menu_path = "Root"

	def draw(self, context):
		layout = self.layout

class COMPOSITOR_MT_effects_specials(bpy.types.Menu):
	bl_label = "Effect Specials"
	bl_options = {'SEARCH_ON_KEY_PRESS'}

	def draw(self, context):
		layout = self.layout
		layout.operator("wm.call_menu", text="Add Effect", icon='ADD').name = "COMPOSITOR_MT_add_effects"
		layout.separator()
		layout.operator("scene.comp_copy_effect", text="Copy effect from layer", icon = 'PASTEDOWN', emboss = False)
		layout.separator()
		layout.operator("scene.comp_clear_effect", text="Clear Effects", icon='TRASH', emboss = False)

def feature_node_menu(self, context):
	if context.space_data.tree_type == "CompositorNodeTree":
		self.layout.separator()
		
		self.layout.menu('COMPOSITOR_MT_add_nodes_features', icon = 'SHADERFX')
		self.layout.menu("COMPOSITOR_MT_add_nodes_presets", icon="PRESET")

classes = (
	COMPOSITOR_MT_add_effects,
	COMPOSITOR_MT_add_effects_adjustment,
	COMPOSITOR_MT_add_effects_filter,
	COMPOSITOR_MT_add_effects_blur,
	COMPOSITOR_MT_add_effects_keying,
	COMPOSITOR_MT_add_effects_transform,
	COMPOSITOR_MT_add_effects_features,
	COMPOSITOR_MT_add_effects_features_color,
	COMPOSITOR_MT_add_effects_features_camera,
	COMPOSITOR_MT_add_effects_features_looks,
	COMPOSITOR_MT_add_effects_features_3d,
	COMPOSITOR_MT_add_effects_features_other,
	COMPOSITOR_MT_add_effects_presets,
	COMPOSITOR_MT_add_nodes_features,
	COMPOSITOR_MT_add_nodes_features_color,
	COMPOSITOR_MT_add_nodes_features_camera,
	COMPOSITOR_MT_add_nodes_features_looks,
	COMPOSITOR_MT_add_nodes_features_3d,
	COMPOSITOR_MT_add_nodes_features_other,
	COMPOSITOR_MT_add_nodes_presets,
	COMPOSITOR_MT_add_effects_asset_browser,
	COMPOSITOR_MT_effects_specials,
		  )

def register():
	for cls in classes:
		bpy.utils.register_class(cls)

	bpy.types.NODE_MT_add.append(feature_node_menu)

def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)

	bpy.types.NODE_MT_add.remove(feature_node_menu)
