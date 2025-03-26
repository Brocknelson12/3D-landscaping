import bpy
from config import MATERIAL_COLORS

def create_metal_material(name, color, roughness=0.4, metallic=0.9):
    """Create a metal material"""
    metal_mat = bpy.data.materials.new(name=name)
    metal_mat.use_nodes = True
    
    # Get Principled BSDF node
    nodes = metal_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    # Set material properties
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Specular"].default_value = 0.5
    
    return metal_mat

def create_glass_material():
    """Create glass material for sensors"""
    glass_mat = bpy.data.materials.new(name="Glass")
    glass_mat.use_nodes = True
    
    # Get Principled BSDF node
    nodes = glass_mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    
    # Set material properties
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["glass"]
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.1
    bsdf.inputs["Transmission"].default_value = 0.9
    bsdf.inputs["IOR"].default_value = 1.45
    
    return glass_mat

def create_robot_materials():
    """Create all materials for the robot"""
    materials = {}
    
    # Metal dark material
    materials["metal_dark"] = create_metal_material(
        "MetalDark", 
        MATERIAL_COLORS["metal_dark"], 
        roughness=0.2
    )
    
    # Metal medium material
    materials["metal_medium"] = create_metal_material(
        "MetalMedium", 
        MATERIAL_COLORS["metal_medium"], 
        roughness=0.3
    )
    
    # Metal light material
    materials["metal_light"] = create_metal_material(
        "MetalLight", 
        MATERIAL_COLORS["metal_light"], 
        roughness=0.4
    )
    
    # Glass material
    materials["glass"] = create_glass_material()
    
    return materials

def add_wear_to_metal(material, amount=0.2):
    """Add wear and tear to metal materials"""
    if not material.use_nodes:
        return
    
    # Get the node tree
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Get the Principled BSDF node
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        return
    
    # Add noise texture for scratches
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.inputs["Scale"].default_value = 20.0
    noise.inputs["Detail"].default_value = 10.0
    noise.inputs["Distortion"].default_value = 0.2
    
    # Add color ramp to control wear intensity
    ramp = nodes.new(type='ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)  # No wear
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (0.3, 0.3, 0.3, 1.0)  # Worn
    
    # Mix node to blend base color with wear
    mix = nodes.new(type='ShaderNodeMixRGB')
    mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = amount  # Wear amount
    
    # Get original base color
    original_color = bsdf.inputs["Base Color"].default_value
    
    # Connect nodes
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], mix.inputs[2])
    
    # Original color input
    if bsdf.inputs["Base Color"].is_linked:
        # If base color already has an input, get that node
        orig_link = bsdf.inputs["Base Color"].links[0]
        orig_node = orig_link.from_node
        orig_socket = orig_link.from_socket
        
        # Remove existing link
        links.remove(orig_link)
        
        # Connect original to mix
        links.new(orig_socket, mix.inputs[1])
    else:
        # No existing link, use the base color directly
        mix.inputs[1].default_value = original_color
    
    # Connect mix to base color
    links.new(mix.outputs["Color"], bsdf.inputs["Base Color"])
    
    # Add some variation to roughness
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs["Strength"].default_value = 0.05 * amount
    
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    
    # Slightly increase roughness
    if not bsdf.inputs["Roughness"].is_linked:
        bsdf.inputs["Roughness"].default_value = min(
            1.0, bsdf.inputs["Roughness"].default_value + (0.1 * amount)
        )