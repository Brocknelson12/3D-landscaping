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


def create_printing_particles(garden_path):
    """Create particle effects for the 3D printing process"""
    # Create a particle system that follows the printed path
    bpy.ops.mesh.primitive_plane_add(size=0.1, location=(0, 0, 0))
    particle_emitter = bpy.context.object
    particle_emitter.name = "PrintingParticles"
    
    # Add particle system
    bpy.ops.object.particle_system_add()
    particles = particle_emitter.particle_systems[0]
    settings = particles.settings
    
    # Configure particles for dust/debris
    settings.type = 'EMITTER'
    settings.count = 1000
    settings.lifetime = 20
    settings.emit_from = 'VERT'
    settings.physics_type = 'NEWTON'
    settings.size_random = 0.5
    settings.drag_factor = 0.5
    
    # Parent to garden path
    particle_emitter.parent = garden_path
    
    return particle_emitter

def create_heat_distortion(garden_path):
    """Create heat distortion effect for freshly printed material"""
    # Create a plane that follows the garden path
    bpy.ops.mesh.primitive_plane_add(size=0.2, location=(0, 0, 0.05))
    heat_plane = bpy.context.object
    heat_plane.name = "HeatDistortion"
    
    # Create distortion material
    distortion_mat = bpy.data.materials.new(name="HeatDistortionMaterial")
    distortion_mat.use_nodes = True
    nodes = distortion_mat.node_tree.nodes
    links = distortion_mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add shader nodes for heat distortion
    output = nodes.new(type='ShaderNodeOutputMaterial')
    shader_mix = nodes.new(type='ShaderNodeMixShader')
    transparent = nodes.new(type='ShaderNodeBsdfTransparent')
    refraction = nodes.new(type='ShaderNodeBsdfRefraction')
    
    # Add noise for distortion
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.inputs["Scale"].default_value = 10.0
    noise.inputs["Detail"].default_value = 2.0
    
    # Connect nodes
    links.new(noise.outputs["Fac"], shader_mix.inputs[0])
    links.new(transparent.outputs[0], shader_mix.inputs[1])
    links.new(refraction.outputs[0], shader_mix.inputs[2])
    links.new(shader_mix.outputs[0], output.inputs["Surface"])
    
    # Assign material
    heat_plane.data.materials.append(distortion_mat)
    
    # Parent to garden path
    heat_plane.parent = garden_path
    
    return heat_plane