import bpy
import bmesh
import math
import random
from mathutils import Vector
from config import TERRAIN_SETTINGS, MATERIAL_COLORS

def create_terrain():
    """Create a more realistic terrain with varied elevation and features"""
    # Create base plane with more subdivisions
    bpy.ops.mesh.primitive_plane_add(size=TERRAIN_SETTINGS["size"], location=(0, 0, 0))
    terrain = bpy.context.object
    terrain.name = "Terrain"
    
    # Add subdivisions for displacement
    bpy.ops.object.modifier_add(type='SUBSURF')
    terrain.modifiers["Subdivision"].levels = TERRAIN_SETTINGS["subdivisions"] + 2  # Increased subdivisions
    terrain.modifiers["Subdivision"].render_levels = TERRAIN_SETTINGS["subdivisions"] + 2
    
    # Add displacement modifier with more variation
    bpy.ops.object.modifier_add(type='DISPLACE')
    terrain.modifiers["Displace"].strength = TERRAIN_SETTINGS["displacement_strength"] * 1.5  # More pronounced terrain
    
    # Create displacement texture
    displace_tex = bpy.data.textures.new("DisplaceTexture", 'CLOUDS')
    displace_tex.noise_scale = TERRAIN_SETTINGS["noise_scale"]
    displace_tex.noise_depth = 3  # More complex noise
    terrain.modifiers["Displace"].texture = displace_tex
    
    # Add another displacement for smaller details
    bpy.ops.object.modifier_add(type='DISPLACE')
    terrain.modifiers[2].name = "MicroDetail"
    terrain.modifiers["MicroDetail"].strength = 0.1
    
    micro_tex = bpy.data.textures.new("MicroDetailTexture", 'VORONOI')
    micro_tex.noise_scale = 5.0
    terrain.modifiers["MicroDetail"].texture = micro_tex
    
    # Apply modifiers
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    bpy.ops.object.modifier_apply(modifier="Displace")
    bpy.ops.object.modifier_apply(modifier="MicroDetail")
    
    # Create more realistic terrain material
    terrain_mat = bpy.data.materials.new(name="TerrainMaterial")
    terrain_mat.use_nodes = True
    nodes = terrain_mat.node_tree.nodes
    links = terrain_mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add new nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    
    # Primary noise for base color
    noise1 = nodes.new(type='ShaderNodeTexNoise')
    noise1.inputs["Scale"].default_value = 2.0
    noise1.inputs["Detail"].default_value = 8.0
    
    # Secondary noise for variation
    noise2 = nodes.new(type='ShaderNodeTexNoise')
    noise2.inputs["Scale"].default_value = 10.0
    noise2.inputs["Detail"].default_value = 6.0
    
    # Color ramps for control
    ramp1 = nodes.new(type='ShaderNodeValToRGB')
    ramp1.color_ramp.elements[0].position = 0.3
    ramp1.color_ramp.elements[0].color = (0.25, 0.15, 0.08, 1.0)  # Dark soil
    ramp1.color_ramp.elements[1].position = 0.7
    ramp1.color_ramp.elements[1].color = (0.4, 0.25, 0.15, 1.0)  # Lighter soil
    
    ramp2 = nodes.new(type='ShaderNodeValToRGB')
    ramp2.color_ramp.elements[0].position = 0.4
    ramp2.color_ramp.elements[0].color = (0.9, 0.9, 0.9, 1.0)  # White for highlights
    ramp2.color_ramp.elements[1].position = 0.8
    ramp2.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)  # Black for lowlights
    
    # Mix node
    mix = nodes.new(type='ShaderNodeMixRGB')
    mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = 0.2
    
    # Bump node for detail
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs["Strength"].default_value = 0.5
    
    # Position nodes
    output.location = (600, 0)
    principled.location = (400, 0)
    bump.location = (200, -200)
    mix.location = (200, 100)
    ramp1.location = (0, 100)
    ramp2.location = (0, -100)
    noise1.location = (-200, 100)
    noise2.location = (-200, -100)
    tex_coord.location = (-600, 0)
    mapping.location = (-400, 0)
    
    # Connect nodes
    links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise1.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise2.inputs["Vector"])
    
    links.new(noise1.outputs["Fac"], ramp1.inputs["Fac"])
    links.new(noise2.outputs["Fac"], ramp2.inputs["Fac"])
    links.new(ramp1.outputs["Color"], mix.inputs[1])
    links.new(ramp2.outputs["Color"], mix.inputs[2])
    
    links.new(mix.outputs["Color"], principled.inputs["Base Color"])
    links.new(noise2.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], principled.inputs["Normal"])
    
    # Set material properties
    principled.inputs["Roughness"].default_value = 0.9
    principled.inputs["Specular"].default_value = 0.1
    
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    
    # Assign material to terrain
    if terrain.data.materials:
        terrain.data.materials[0] = terrain_mat
    else:
        terrain.data.materials.append(terrain_mat)
    
    # Create some rocks on the terrain
    create_rocks(terrain)
    
    return terrain

def create_rocks(terrain):
    """Add some rocks to the terrain for visual interest and to demonstrate robot navigation"""
    rock_collection = bpy.data.collections.new("Rocks")
    bpy.context.scene.collection.children.link(rock_collection)
    
    # Create a few different rock shapes to reuse
    rock_meshes = []
    
    # Rock 1 - Rounded
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.2, subdivisions=2, location=(0, 0, 0))
    rock1 = bpy.context.object
    rock1.name = "RockBase1"
    
    # Add some random displacement
    bpy.ops.object.modifier_add(type='DISPLACE')
    rock1.modifiers["Displace"].strength = 0.05
    rock_tex = bpy.data.textures.new("RockTexture1", 'VORONOI')
    rock_tex.noise_scale = 1.0
    rock1.modifiers["Displace"].texture = rock_tex
    
    # Apply modifier
    bpy.ops.object.modifier_apply(modifier="Displace")
    rock_meshes.append(rock1.data)
    
    # Rock 2 - More angular
    bpy.ops.mesh.primitive_ico_sphere_add(radius=0.15, subdivisions=1, location=(0, 0, 0))
    rock2 = bpy.context.object
    rock2.name = "RockBase2"
    
    # Add some random displacement
    bpy.ops.object.modifier_add(type='DISPLACE')
    rock2.modifiers["Displace"].strength = 0.1
    rock_tex2 = bpy.data.textures.new("RockTexture2", 'MUSGRAVE')
    rock_tex2.noise_scale = 1.0
    rock2.modifiers["Displace"].texture = rock_tex2
    
    # Apply modifier
    bpy.ops.object.modifier_apply(modifier="Displace")
    rock_meshes.append(rock2.data)
    
    # Create rock material
    rock_mat = bpy.data.materials.new(name="RockMaterial")
    rock_mat.use_nodes = True
    nodes = rock_mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.3, 0.3, 0.3, 1.0)  # Grey
    principled.inputs["Roughness"].default_value = 0.8
    
    # Place rocks on the terrain
    for i in range(20):  # Create 20 rocks
        # Random position within terrain bounds
        x = random.uniform(-9, 9)
        y = random.uniform(-9, 9)
        
        # Find z position (height) at this point on terrain
        # This is approximate - we're casting a ray from above
        highest_z = 0
        for v in terrain.data.vertices:
            terrain_x, terrain_y, terrain_z = terrain.matrix_world @ v.co
            distance = math.sqrt((x - terrain_x)**2 + (y - terrain_y)**2)
            if distance < 0.5:  # If point is close enough
                highest_z = max(highest_z, terrain_z)
        
        # Create rock instance
        mesh = random.choice(rock_meshes)
        rock = bpy.data.objects.new(f"Rock_{i}", mesh)
        rock_collection.objects.link(rock)
        
        # Position and scale rock
        rock.location = (x, y, highest_z)
        scale = random.uniform(0.5, 2.0)
        rock.scale = (scale, scale, scale * random.uniform(0.7, 1.3))  # Slightly varied scale
        
        # Rotate randomly
        rock.rotation_euler = (
            random.uniform(0, 3.14),
            random.uniform(0, 3.14),
            random.uniform(0, 3.14)
        )
        
        # Apply material
        if rock.data.materials:
            rock.data.materials[0] = rock_mat
        else:
            rock.data.materials.append(rock_mat)
    
    # Hide original rock bases
    rock1.hide_viewport = True
    rock1.hide_render = True
    rock2.hide_viewport = True
    rock2.hide_render = True
    
    return rock_collection

def create_grass(terrain):
    """Create more realistic grass particles on the terrain"""
    # Create grass material with more realism
    grass_mat = bpy.data.materials.new(name="GrassMaterial")
    grass_mat.use_nodes = True
    
    # Get node tree
    nodes = grass_mat.node_tree.nodes
    links = grass_mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
        
    # Add new nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Add color variation to grass
    colorRamp = nodes.new(type='ShaderNodeValToRGB')
    noise = nodes.new(type='ShaderNodeTexNoise')
    
    # Position nodes
    output.location = (300, 0)
    principled.location = (100, 0)
    colorRamp.location = (-100, 0)
    noise.location = (-300, 0)
    
    # Setup color ramp for grass variation
    colorRamp.color_ramp.elements[0].position = 0.3
    colorRamp.color_ramp.elements[0].color = (0.05, 0.3, 0.05, 1.0)  # Darker green
    colorRamp.color_ramp.elements[1].position = 0.7
    colorRamp.color_ramp.elements[1].color = (0.2, 0.5, 0.1, 1.0)  # Lighter green
    
    # Setup noise
    noise.inputs["Scale"].default_value = 20.0
    noise.inputs["Detail"].default_value = 2.0
    
    # Connect nodes
    links.new(noise.outputs["Fac"], colorRamp.inputs["Fac"])
    links.new(colorRamp.outputs["Color"], principled.inputs["Base Color"])
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    
    # Set material properties
    principled.inputs["Specular"].default_value = 0.1
    principled.inputs["Roughness"].default_value = 0.9
    principled.inputs["Transmission"].default_value = 0.2
    
    # Create more realistic grass blade mesh
    bpy.ops.mesh.primitive_plane_add(size=0.05, location=(0, 0, 0))
    grass_blade = bpy.context.object
    grass_blade.name = "GrassBlade"
    
    # Switch to edit mode to modify the grass blade
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(grass_blade.data)
    
    # Create a more tapered grass blade shape
    for v in bm.verts:
        # Move top vertices up to create blade
        if v.co.y > 0:
            v.co.z += 0.15
            v.co.y += 0.02
    
    # Add a slight curve to the grass blade
    for v in bm.verts:
        # Calculate curve amount based on height
        curve_amt = v.co.z * 0.3
        v.co.x += curve_amt
    
    bmesh.update_edit_mesh(grass_blade.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create a small amount of random rotation
    bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
    grass_blade.modifiers["SimpleDeform"].deform_method = 'TWIST'
    grass_blade.modifiers["SimpleDeform"].angle = 0.2
    bpy.ops.object.modifier_apply(modifier="SimpleDeform")
    
    # Assign material to grass blade
    if grass_blade.data.materials:
        grass_blade.data.materials[0] = grass_mat
    else:
        grass_blade.data.materials.append(grass_mat)
    
    # Create another grass blade variation
    bpy.ops.object.duplicate()
    grass_blade2 = bpy.context.object
    grass_blade2.name = "GrassBlade2"
    
    # Modify second blade to be different
    bpy.ops.transform.resize(value=(0.8, 1.2, 1.3))
    bpy.ops.transform.rotate(value=0.3, orient_axis='Z')
    
    # Add particle system to terrain with improved settings
    bpy.context.view_layer.objects.active = terrain
    
    # Create main grass patch
    bpy.ops.object.particle_system_add()
    particle_system = terrain.particle_systems[0]
    settings = particle_system.settings
    
    # Configure particle system for realistic grass
    settings.type = 'HAIR'
    settings.count = TERRAIN_SETTINGS["grass_count"] * 2  # More grass
    settings.hair_length = TERRAIN_SETTINGS["grass_length"] * 1.5  # Longer grass
    settings.render_type = 'COLLECTION'
    
    # Create collection for grass variations
    grass_collection = bpy.data.collections.new("GrassBlades")
    bpy.context.scene.collection.children.link(grass_collection)
    grass_collection.objects.link(grass_blade)
    grass_collection.objects.link(grass_blade2)
    
    # Use collection instance for variation
    settings.instance_collection = grass_collection
    settings.use_collection_pick_random = True
    
    # More natural distribution
    settings.use_advanced_hair = True
    settings.factor_random = 0.7
    settings.phase_factor_random = 2.0
    settings.brownian_factor = 0.05
    settings.child_nbr = 15
    settings.rendered_child_count = 30
    settings.clump_factor = 0.2
    
    # Vertex group for grass distribution
    # Create a vertex group to control where grass appears
    group = terrain.vertex_groups.new(name="GrassArea")
    
    # Add random vertices to the group with varying weights
    for v in terrain.data.vertices:
        # Convert vertex position to world space
        world_pos = terrain.matrix_world @ v.co
        
        # Don't add grass on steep slopes or at edges
        slope = 1.0 - abs(v.normal.z)  # 0 for flat, 1 for vertical
        edge_factor = min(1.0, (10.0 - abs(world_pos.x)) / 3.0) * min(1.0, (10.0 - abs(world_pos.y)) / 3.0)
        
        if slope < 0.7 and edge_factor > 0.2:  # Only moderate slopes away from edges
            # Create patches of grass with some bare spots
            noise_val = noise_2d(world_pos.x * 0.2, world_pos.y * 0.2)
            if noise_val > 0.3:  # Threshold for grass patches
                weight = (1.0 - slope) * edge_factor * (noise_val - 0.3) * 1.4
                group.add([v.index], min(1.0, max(0.0, weight)), 'REPLACE')
    
    # Use vertex group for distribution
    settings.vertex_group_density = "GrassArea"
    
    # Hide original grass blades from render
    grass_blade.hide_render = True
    grass_blade.hide_viewport = True
    grass_blade2.hide_render = True
    grass_blade2.hide_viewport = True
    
    return particle_system

def noise_2d(x, y):
    """Simple 2D noise function for grass distribution"""
    return (math.sin(x * 5.0) * math.cos(y * 5.0) + 1.0) / 2.0 * 0.5 + \
           (math.sin(x * 20.0) * math.cos(y * 20.0) + 1.0) / 2.0 * 0.25 + \
           (math.sin(x * 50.0) * math.cos(y * 50.0) + 1.0) / 2.0 * 0.125