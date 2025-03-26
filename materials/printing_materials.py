import bpy
from config import MATERIAL_COLORS

def create_clay_material():
    """Create material for clay"""
    clay_mat = bpy.data.materials.new(name="Clay")
    clay_mat.use_nodes = True
    
    # Get Principled BSDF node
    nodes = clay_mat.node_tree.nodes
    links = clay_mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    # Set material properties
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["clay"]
    bsdf.inputs["Roughness"].default_value = 0.9
    bsdf.inputs["Specular"].default_value = 0.1
    
    # Add noise texture for clay variation
    tex_noise = nodes.new(type='ShaderNodeTexNoise')
    tex_noise.inputs["Scale"].default_value = 30.0
    tex_noise.inputs["Detail"].default_value = 6.0
    tex_noise.inputs["Distortion"].default_value = 0.5
    
    # Add bump for surface detail
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs["Strength"].default_value = 0.2
    
    # Add color variation
    mix_rgb = nodes.new(type='ShaderNodeMixRGB')
    mix_rgb.blend_type = 'MULTIPLY'
    mix_rgb.inputs[0].default_value = 0.1
    
    # Slightly darker color for variation
    darker_color = (
        MATERIAL_COLORS["clay"][0] * 0.8,
        MATERIAL_COLORS["clay"][1] * 0.8,
        MATERIAL_COLORS["clay"][2] * 0.8,
        1.0
    )
    mix_rgb.inputs[2].default_value = darker_color
    mix_rgb.inputs[1].default_value = MATERIAL_COLORS["clay"]
    
    # Connect nodes
    links.new(tex_noise.outputs["Fac"], bump.inputs["Height"])
    links.new(tex_noise.outputs["Fac"], mix_rgb.inputs[0])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    links.new(mix_rgb.outputs["Color"], bsdf.inputs["Base Color"])
    
    return clay_mat

def create_concrete_material():
    """Create material for concrete"""
    concrete_mat = bpy.data.materials.new(name="Concrete")
    concrete_mat.use_nodes = True
    
    # Get Principled BSDF node
    nodes = concrete_mat.node_tree.nodes
    links = concrete_mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    # Set material properties
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["concrete"]
    bsdf.inputs["Roughness"].default_value = 0.9
    bsdf.inputs["Specular"].default_value = 0.1
    
    # Add noise texture for rough concrete
    tex_noise = nodes.new(type='ShaderNodeTexNoise')
    tex_noise.inputs["Scale"].default_value = 50.0
    tex_noise.inputs["Detail"].default_value = 16.0
    tex_noise.inputs["Roughness"].default_value = 0.7
    
    # Add voronoi texture for aggregate look
    voronoi = nodes.new(type='ShaderNodeTexVoronoi')
    voronoi.voronoi_dimensions = '3D'
    voronoi.inputs["Scale"].default_value = 40.0
    
    # Mix the textures
    mix = nodes.new(type='ShaderNodeMixRGB')
    mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = 0.5
    
    # Add bump for surface detail
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs["Strength"].default_value = 0.1
    
    # Connect nodes
    links.new(tex_noise.outputs["Fac"], mix.inputs[1])
    links.new(voronoi.outputs["Distance"], mix.inputs[2])
    links.new(mix.outputs["Color"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    
    # Add a slight color variation
    mix_rgb = nodes.new(type='ShaderNodeMixRGB')
    mix_rgb.blend_type = 'MULTIPLY'
    mix_rgb.inputs[0].default_value = 0.1
    
    # Slightly varied color
    varied_color = (
        MATERIAL_COLORS["concrete"][0] * 0.95,
        MATERIAL_COLORS["concrete"][1] * 0.95,
        MATERIAL_COLORS["concrete"][2] * 0.95,
        1.0
    )
    mix_rgb.inputs[2].default_value = varied_color
    mix_rgb.inputs[1].default_value = MATERIAL_COLORS["concrete"]
    
    links.new(tex_noise.outputs["Fac"], mix_rgb.inputs[0])
    links.new(mix_rgb.outputs["Color"], bsdf.inputs["Base Color"])
    
    return concrete_mat

def create_soil_material():
    """Create material for soil"""
    soil_mat = bpy.data.materials.new(name="Soil")
    soil_mat.use_nodes = True
    
    # Get Principled BSDF node
    nodes = soil_mat.node_tree.nodes
    links = soil_mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    
    # Set material properties
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["soil"]
    bsdf.inputs["Roughness"].default_value = 1.0
    bsdf.inputs["Specular"].default_value = 0.0
    
    # Add noise texture for soil variation
    tex_noise = nodes.new(type='ShaderNodeTexNoise')
    tex_noise.inputs["Scale"].default_value = 100.0
    tex_noise.inputs["Detail"].default_value = 16.0
    tex_noise.inputs["Distortion"].default_value = 0.5
    
    # Add musgrave texture for more natural soil look
    musgrave = nodes.new(type='ShaderNodeTexMusgrave')
    musgrave.musgrave_type = 'FBM'
    musgrave.inputs["Scale"].default_value = 10.0
    musgrave.inputs["Detail"].default_value = 16.0
    musgrave.inputs["Dimension"].default_value = 2.0
    
    # Mix the textures
    mix = nodes.new(type='ShaderNodeMixRGB')
    mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = 0.7
    
    # Add color variation
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = 0.3
    color_ramp.color_ramp.elements[0].color = (
        MATERIAL_COLORS["soil"][0] * 0.7,
        MATERIAL_COLORS["soil"][1] * 0.7,
        MATERIAL_COLORS["soil"][2] * 0.7,
        1.0
    )
    color_ramp.color_ramp.elements[1].position = 0.7
    color_ramp.color_ramp.elements[1].color = (
        MATERIAL_COLORS["soil"][0] * 1.2,
        MATERIAL_COLORS["soil"][1] * 1.2,
        MATERIAL_COLORS["soil"][2] * 1.2,
        1.0
    )
    
    # Add bump for surface detail
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs["Strength"].default_value = 0.3
    
    # Connect nodes
    links.new(tex_noise.outputs["Fac"], mix.inputs[1])
    links.new(musgrave.outputs["Fac"], mix.inputs[2])
    links.new(mix.outputs["Color"], color_ramp.inputs["Fac"])
    links.new(mix.outputs["Color"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    links.new(color_ramp.outputs["Color"], bsdf.inputs["Base Color"])
    
    return soil_mat

def create_printing_materials():
    """Create all materials used in the printing process"""
    materials = {}
    
    materials["clay"] = create_clay_material()
    materials["concrete"] = create_concrete_material()
    materials["soil"] = create_soil_material()
    
    return materials