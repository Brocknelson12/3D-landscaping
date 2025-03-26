import bpy
import bmesh
import math
import random
from mathutils import Vector
from config import TERRAIN_SETTINGS, MATERIAL_COLORS

def create_terrain():
    """Create a terrain with slight elevation and texture"""
    # Create base plane
    bpy.ops.mesh.primitive_plane_add(size=TERRAIN_SETTINGS["size"], location=(0, 0, 0))
    terrain = bpy.context.object
    terrain.name = "Terrain"
    
    # Add subdivisions for displacement
    bpy.ops.object.modifier_add(type='SUBSURF')
    terrain.modifiers["Subdivision"].levels = TERRAIN_SETTINGS["subdivisions"]
    terrain.modifiers["Subdivision"].render_levels = TERRAIN_SETTINGS["subdivisions"]
    
    # Add displacement modifier
    bpy.ops.object.modifier_add(type='DISPLACE')
    terrain.modifiers["Displace"].strength = TERRAIN_SETTINGS["displacement_strength"]
    
    # Create displacement texture
    displace_tex = bpy.data.textures.new("DisplaceTexture", 'CLOUDS')
    displace_tex.noise_scale = TERRAIN_SETTINGS["noise_scale"]
    terrain.modifiers["Displace"].texture = displace_tex
    
    # Apply modifiers
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    bpy.ops.object.modifier_apply(modifier="Displace")
    
    # Create material
    terrain_mat = bpy.data.materials.new(name="TerrainMaterial")
    terrain_mat.use_nodes = True
    bsdf = terrain_mat.node_tree.nodes["Principled BSDF"]
    
    # Set material properties for dirt/soil
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["terrain"]
    bsdf.inputs["Roughness"].default_value = 0.9
    
    # Assign material to terrain
    if terrain.data.materials:
        terrain.data.materials[0] = terrain_mat
    else:
        terrain.data.materials.append(terrain_mat)
    
    return terrain

def create_grass(terrain):
    """Create grass particles on the terrain"""
    # Create grass material
    grass_mat = bpy.data.materials.new(name="GrassMaterial")
    grass_mat.use_nodes = True
    bsdf = grass_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["grass"]
    
    # Create simple grass blade mesh
    bpy.ops.mesh.primitive_plane_add(size=0.1, location=(0, 0, 0))
    grass_blade = bpy.context.object
    grass_blade.name = "GrassBlade"
    
    # Add slight bend to grass blade
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(grass_blade.data)
    for v in bm.verts:
        if v.co.z > 0:
            v.co.z += 0.1
    bmesh.update_edit_mesh(grass_blade.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Assign material to grass blade
    if grass_blade.data.materials:
        grass_blade.data.materials[0] = grass_mat
    else:
        grass_blade.data.materials.append(grass_mat)
    
    # Add particle system to terrain
    bpy.context.view_layer.objects.active = terrain
    bpy.ops.object.particle_system_add()
    particle_system = terrain.particle_systems[0]
    settings = particle_system.settings
    
    # Configure particle system
    settings.type = 'HAIR'
    settings.count = TERRAIN_SETTINGS["grass_count"]
    settings.hair_length = TERRAIN_SETTINGS["grass_length"]
    settings.render_type = 'OBJECT'
    settings.instance_object = grass_blade
    settings.use_advanced_hair = True
    settings.factor_random = 0.5
    settings.phase_factor_random = 2.0
    settings.child_nbr = 10
    settings.rendered_child_count = 20
    
    # Hide original grass blade from render
    grass_blade.hide_render = True
    grass_blade.hide_viewport = True
    
    return particle_system