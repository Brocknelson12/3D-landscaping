import bpy
import math
from mathutils import Vector
from config import MATERIAL_COLORS

def create_scan_effect():
    """Create a visual effect for the scanning process"""
    # Create a plane for scan effect
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0.1))
    scan_plane = bpy.context.object
    scan_plane.name = "ScanEffect"
    
    # Create scan material
    scan_mat = bpy.data.materials.new(name="ScanMaterial")
    scan_mat.use_nodes = True
    
    # Set up nodes for scan effect
    nodes = scan_mat.node_tree.nodes
    links = scan_mat.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    transparent = nodes.new(type='ShaderNodeBsdfTransparent')
    mix = nodes.new(type='ShaderNodeMixShader')
    noise = nodes.new(type='ShaderNodeTexNoise')
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    
    # Position nodes
    output.location = (600, 0)
    mix.location = (400, 0)
    emission.location = (200, 100)
    transparent.location = (200, -100)
    color_ramp.location = (0, 0)
    noise.location = (-200, 0)
    
    # Connect nodes
    links.new(noise.outputs["Fac"], color_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], mix.inputs["Fac"])
    links.new(transparent.outputs["BSDF"], mix.inputs[1])
    links.new(emission.outputs["Emission"], mix.inputs[2])
    links.new(mix.outputs["Shader"], output.inputs["Surface"])
    
    # Set node properties
    emission.inputs["Color"].default_value = MATERIAL_COLORS["scan_effect"]
    emission.inputs["Strength"].default_value = 2.0
    
    noise.inputs["Scale"].default_value = 10.0
    noise.inputs["Detail"].default_value = 2.0
    
    # Set color ramp for grid-like pattern
    color_ramp.color_ramp.elements[0].position = 0.45
    color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 0.0)
    color_ramp.color_ramp.elements[1].position = 0.5
    color_ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    
    # Add new element
    element = color_ramp.color_ramp.elements.new(0.55)
    element.color = (0.0, 0.0, 0.0, 0.0)
    
    # Assign material
    if scan_plane.data.materials:
        scan_plane.data.materials[0] = scan_mat
    else:
        scan_plane.data.materials.append(scan_mat)
    
    # Hide scan effect initially
    scan_plane.hide_viewport = True
    scan_plane.hide_render = True
    
    return scan_plane