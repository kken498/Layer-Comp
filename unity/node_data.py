
effect_node_data = {}
effect_node_data['CompositorNodeBrightContrast'] = ['Birghtness / Contrast', 'IMAGE_ALPHA']
effect_node_data['CompositorNodeValToRGB'] = ['Color Ramp', 'NODE_TEXTURE']
effect_node_data['CompositorNodeColorBalance'] = ['Color Balance', 'COLOR']
effect_node_data['CompositorNodeColorCorrection'] = ['Color Correction', 'SHADERFX']
effect_node_data['CompositorNodeExposure'] = ['Exposure', 'SORTBYEXT']
effect_node_data['CompositorNodeGamma'] = ['Gamma', 'SEQ_HISTOGRAM']
effect_node_data['ShaderNodeGamma'] = ['Gamma', 'SEQ_HISTOGRAM']

effect_node_data['CompositorNodeHueCorrect'] = ['Hue Correct', 'MOD_HUE_SATURATION']
effect_node_data['CompositorNodeHueSat'] = ['HSV', 'MOD_HUE_SATURATION']
effect_node_data['CompositorNodeCurveRGB'] = ['RGB Curve', 'NORMALIZE_FCURVES']
effect_node_data['CompositorNodeTonemap'] = ['Tonemap', 'RIGID_BODY']
effect_node_data['CompositorNodeInvert'] = ['Invert Color', 'IMAGE_RGB_ALPHA']
effect_node_data['CompositorNodeRGBToBW'] = ['Black/White', 'IMAGE_RGB']
effect_node_data['CompositorNodeConvertColorSpace'] = ['Convert ColorSpace', 'SEQ_SPLITVIEW']
effect_node_data['CompositorNodeConvertToDisplay'] = ['Convert To Display', 'IMAGE_BACKGROUND']
effect_node_data['CompositorNodeZcombine'] = ['Depth Combine', 'IMAGE_ZDEPTH']
effect_node_data['CompositorNodeSeparateColor'] = ['Separate Color', 'PARTICLES']

effect_node_data['CompositorNodeAlphaOver'] = ['Alpha Over', 'INDIRECT_ONLY_ON']
effect_node_data['CompositorNodeSetAlpha'] = ['Set Alpha', 'INDIRECT_ONLY_ON']
effect_node_data['CompositorNodePremulKey'] = ['Alpha Convert', 'INDIRECT_ONLY_ON']

effect_node_data['CompositorNodeAntiAliasing'] = ['Anti-Aliasing', 'IPO_CONSTANT']
effect_node_data['CompositorNodeConvolve'] = ['Convolve', 'CON_GEOMETRYATTRIBUTE']
effect_node_data['CompositorNodeDespeckle'] = ['Despecklet', 'IPO_EASE_IN_OUT']
effect_node_data['CompositorNodeInpaint'] = ['InPaint', 'BRUSH_DATA']
effect_node_data['CompositorNodeFilter'] = ['Filter', 'FILTER']
effect_node_data['CompositorNodeGlare'] = ['Glare', 'SHADING_RENDERED']
effect_node_data['CompositorNodeKuwahara'] = ['Kuwahara', 'IMAGE_DATA']
effect_node_data['CompositorNodePixelate'] = ['Pixelate', 'MOD_REMESH']
effect_node_data['CompositorNodePosterize'] = ['Posterize', 'COLORSET_10_VEC']
effect_node_data['CompositorNodeSunBeams'] = ['Sun Beams', 'LIGHT_SUN']
effect_node_data['CompositorNodeLensdist'] = ['Lens Distortion', 'RESTRICT_RENDER_OFF']

effect_node_data['CompositorNodeBlur'] = ['Blur', 'CLIPUV_HLT']
effect_node_data['CompositorNodeBokehBlur'] = ['Bokeh Blur', 'CLIPUV_HLT']
effect_node_data['CompositorNodeBilateralblur'] = ['Bilateral Blur', 'CLIPUV_HLT']
effect_node_data['CompositorNodeDefocus'] = ['Defocus', 'CLIPUV_HLT']
effect_node_data['CompositorNodeDBlur'] = ['Directional Blur', 'CLIPUV_HLT']

effect_node_data['CompositorNodeCryptomatte'] = ['Cryptomatte (Legacy)', 'EYEDROPPER']

effect_node_data['CompositorNodeChannelMatte'] = ['Channel Key', 'KEYINGSET']
effect_node_data['CompositorNodeChromaMatte'] = ['Chroma Key', 'KEYINGSET']
effect_node_data['CompositorNodeColorMatte'] = ['Color Key', 'KEYINGSET']
effect_node_data['CompositorNodeColorSpill'] = ['Color Spill', 'KEYINGSET']
effect_node_data['CompositorNodeDistanceMatte'] = ['Distance Key', 'KEYINGSET']
effect_node_data['CompositorNodeKeying'] = ['Keying', 'KEYINGSET']
effect_node_data['CompositorNodeLumaMatte'] = ['Luminance Key', 'KEYINGSET']

effect_node_data['CompositorNodeTransform'] = ['Transform', 'CON_TRANSFORM']
effect_node_data['CompositorNodeTranslate'] = ['Translate', 'CON_LOCLIKE']
effect_node_data['CompositorNodeRotate'] = ['Rotate', 'CON_ROTLIKE']
effect_node_data['CompositorNodeScale'] = ['Scale', 'CON_SIZELIKE']

effect_node_data['CompositorNodeCornerPin'] = ['Corner Pin', 'PINNED']
effect_node_data['CompositorNodeCrop'] = ['Crop', 'AREA_DOCK']
effect_node_data['CompositorNodeDisplace'] = ['Displace', 'MOD_DISPLACE']
effect_node_data['CompositorNodeFlip'] = ['Flip', 'MOD_MIRROR']

source_node_data = {}
source_node_data['CompositorNodeRLayers'] = ['Render Layers', 'RENDER_RESULT']
source_node_data['CompositorNodeImage'] = ['Image', 'OUTLINER_OB_IMAGE']
source_node_data['CompositorNodeMovieClip'] = ['Movie', 'SEQUENCE']
source_node_data['CompositorNodeRGB'] = ['Solid', 'SNAP_FACE']
source_node_data['CompositorNodeBokehImage'] = ['Bokeh Image', 'SEQ_CHROMA_SCOPE']
source_node_data['CompositorNodeGroup'] = ['Compositor', 'NODE_COMPOSITING']

output_node_data = {}
output_node_data['CompositorNodeComposite'] = ['Composite', 'NODE_COMPOSITING']
output_node_data['CompositorNodeOutputFile'] = ['File Output', 'OUTPUT']

layer_node_data = {}
layer_node_data['CompositorNodeRLayers'] = ['Render Layers', 'RENDER_RESULT']
layer_node_data['CompositorNodeImage'] = ['Image', 'OUTLINER_OB_IMAGE']
layer_node_data['CompositorNodeMovieClip'] = ['Movie Clip', 'SEQUENCE']
layer_node_data['CompositorNodeRGB'] = ['Solid', 'SNAP_FACE']
layer_node_data['ShaderNodeTexGradient'] = ['Gradient Texture', 'NODE_TEXTURE']
layer_node_data['CompositorNodeBokehImage'] = ['Bokeh Image', 'SEQ_CHROMA_SCOPE']

texture_node_data = {}
texture_node_data['CompositorNodeTexture'] = ['Texture', 'TEXTURE']
texture_node_data['ShaderNodeTexBrick'] = ['Brick Texture', 'TEXTURE']
texture_node_data['ShaderNodeTexChecker'] = ['Checker Texture', 'TEXTURE']
texture_node_data['ShaderNodeTexGabor'] = ['Gabor Texture', 'TEXTURE']
texture_node_data['ShaderNodeTexGradient'] = ['Gradient Texture', 'TEXTURE']
texture_node_data['ShaderNodeTexMagic'] = ['Magic Texture', 'TEXTURE']
texture_node_data['ShaderNodeTexNoise'] = ['Noise Texture', 'TEXTURE']
texture_node_data['ShaderNodeTexVoronoi'] = ['Voronoi Texture', 'TEXTURE']
texture_node_data['ShaderNodeTexWave'] = ['Wave Texture', 'TEXTURE']
texture_node_data['ShaderNodeTexWhiteNoise'] = ['White Noise Texture', 'TEXTURE']

feature_node_data = {}
feature_node_data['CompositorNodeFill'] = ['Fill', 'SNAP_FACE']
feature_node_data['CompositorNodeSpotFill'] = ['Spot Fill', 'SURFACE_NCIRCLE']
feature_node_data['CompositorNodeColorSelection'] = ['ColorSelection', 'VIS_SEL_11']
feature_node_data['CompositorNodeColorReplace'] = ['ColorReplace', 'OVERLAY']
feature_node_data['CompositorNodeColorInnerShadow'] = ['Color InnerShadow', 'ANTIALIASED']
feature_node_data['CompositorNodeColorInnerShadowSingle'] = ['Color InnerShadow(Single)', 'ANTIALIASED']
feature_node_data['CompositorNodeDropShadow'] = ['DropShadow', 'SELECT_SUBTRACT']
feature_node_data['CompositorNodeInnerShadow'] = ['InnerShadow', 'SELECT_INTERSECT']
feature_node_data['CompositorNodeRimLight'] = ['Rim Light', 'LIGHT_AREA']
feature_node_data['CompositorNodeOuterGlow'] = ['Outer Glow', 'LIGHT_SUN']
feature_node_data['CompositorNodeBoundaryLine'] = ['BoundaryLine', 'MOD_LINEART']
feature_node_data['CompositorNodePaintFilter'] = ['Paint Filter', 'BRUSHES_ALL']
feature_node_data['CompositorNodeSpotExposure'] = ['Spot Exposure', 'LIGHT_SPOT']
feature_node_data['CompositorNodeCameraLensBlur'] = ['Camera Lens Blur', 'VIEW_CAMERA']
feature_node_data['CompositorNodeChromaticAberration'] = ['Chromatic Aberration', 'SEQ_CHROMA_SCOPE']
feature_node_data['CompositorNodeVignette'] = ['Vignette', 'MOD_MASK']
feature_node_data['CompositorNodeEdgeSoftness'] = ['Edge Softness', 'PROP_OFF']
feature_node_data['CompositorNodeSwingTilt'] = ['Swing-Tilt', 'AREA_SWAP']
feature_node_data['CompositorNodeShutterStreak'] = ['Shutter Streak', 'CAMERA_STEREO']
feature_node_data['CompositorNodeHalation'] = ['Halation', 'SHADERFX']
feature_node_data['CompositorNodeBlurRGB'] = ['Blur RGB', 'PROP_CON']
feature_node_data['CompositorNodeTwitch'] = ['Twitch', 'GHOST_ENABLED']
feature_node_data['CompositorNodeRenoiser'] = ['Renoiser', 'TEXTURE']
feature_node_data['CompositorNodeSeparateRGBA'] = ['Separate RGBA', 'PARTICLES']
feature_node_data['CompositorNodeWiggleTransfrom'] = ['Wiggle Transfrom', 'CON_ROTLIKE']
feature_node_data['CompositorNodeTile'] = ['Tile', 'SNAP_VERTEX']

feature_node_data_4_5 = ['CompositorNodeSwingTilt', 'CompositorNodeTwitch', 'CompositorNodeWiggleTransfrom']
feature_node_data_5_0 = ['CompositorNodeTile']

socket_data = {}
socket_data['RGBA'] = 'NODE_SOCKET_RGBA'
socket_data['VALUE'] = 'NODE_SOCKET_FLOAT'
socket_data['FLOAT'] = 'NODE_SOCKET_FLOAT'
socket_data['VECTOR'] = 'NODE_SOCKET_VECTOR'
socket_data['BOOLEAN'] = 'NODE_SOCKET_BOOLEAN'
socket_data['INT'] = 'NODE_SOCKET_INT'
socket_data['IMAGE'] = 'NODE_SOCKET_IMAGE'
socket_data['MENU'] = 'NODE_SOCKET_MENU'
