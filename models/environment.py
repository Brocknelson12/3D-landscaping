import bpy
import math
import random
from mathutils import Vector

def create_backyard_environment():
    """Create a backyard environment with house corner, fence, and grass area"""
    # Create collection for environment objects
    env_collection = bpy.data.collections.new("Environment")
    bpy.context.scene.collection.children.link(env_collection)
    
    # Create corner of house
    house_width = 5.0
    house_depth = 4.0
    house_height = 3.5
    
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(house_width/2, house_depth/2, house_height/2))
    house = bpy.context.object
    house.name = "HouseCorner"
    house.scale = (house_width, house_depth, house_height)
    env_collection.objects.link(house)
    
    # Create house material
    house_mat = bpy.data.materials.new(name="HouseMaterial")
    house_mat.use_nodes = True
    nodes = house_mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.9, 0.85, 0.8, 1.0)  # Light beige
    principled.inputs["Roughness"].default_value = 0.7
    house.data.materials.append(house_mat)
    
    # Create backyard fence
    create_backyard_fence(env_collection)
    
    # Create empty grass area (defined by dotted outline)
    create_garden_outline()
    
    return env_collection

def create_backyard_fence(collection):
    """Create a wooden fence around the backyard"""
    fence_height = 1.8
    fence_length_1 = 12.0
    fence_length_2 = 8.0
    post_spacing = 2.0
    
    # Create fence material
    fence_mat = bpy.data.materials.new(name="FenceMaterial")
    fence_mat.use_nodes = True
    nodes = fence_mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.6, 0.5, 0.4, 1.0)  # Wood brown
    principled.inputs["Roughness"].default_value = 0.9
    
    # Create first fence segment (along x-axis)
    for i in range(0, int(fence_length_1/post_spacing) + 1):
        x_pos = i * post_spacing
        # Create fence post
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(x_pos, 0, fence_height/2))
        post = bpy.context.object
        post.name = f"FencePost_x_{i}"
        post.scale = (0.1, 0.1, fence_height)
        post.data.materials.append(fence_mat)
        collection.objects.link(post)
        
        # Create horizontal planks between posts (except for last post)
        if i < int(fence_length_1/post_spacing):
            for j in range(3):  # Three horizontal planks
                plank_height = 0.5 + j * 0.6
                bpy.ops.mesh.primitive_cube_add(size=0.1, 
                                               location=(x_pos + post_spacing/2, 0, plank_height))
                plank = bpy.context.object
                plank.name = f"FencePlank_x_{i}_{j}"
                plank.scale = (post_spacing, 0.02, 0.1)
                plank.data.materials.append(fence_mat)
                collection.objects.link(plank)
    
    # Create second fence segment (along y-axis)
    for i in range(0, int(fence_length_2/post_spacing) + 1):
        y_pos = i * post_spacing
        # Create fence post
        bpy.ops.mesh.primitive_cube_add(size=0.1, location=(fence_length_1, y_pos, fence_height/2))
        post = bpy.context.object
        post.name = f"FencePost_y_{i}"
        post.scale = (0.1, 0.1, fence_height)
        post.data.materials.append(fence_mat)
        collection.objects.link(post)
        
        # Create horizontal planks between posts (except for last post)
        if i < int(fence_length_2/post_spacing):
            for j in range(3):  # Three horizontal planks
                plank_height = 0.5 + j * 0.6
                bpy.ops.mesh.primitive_cube_add(size=0.1, 
                                               location=(fence_length_1, y_pos + post_spacing/2, plank_height))
                plank = bpy.context.object
                plank.name = f"FencePlank_y_{i}_{j}"
                plank.scale = (0.02, post_spacing, 0.1)
                plank.data.materials.append(fence_mat)
                collection.objects.link(plank)

def create_garden_outline():
    """Create a dotted outline for the garden bed"""
    # Create a rounded square/oval shape
    bpy.ops.curve.primitive_bezier_circle_add(radius=3.0, location=(8, 4, 0.01))
    outline = bpy.context.object
    outline.name = "GardenOutline"
    
    # Modify to make it more oval-square
    if outline.data.splines and outline.data.splines[0].bezier_points:
        points = outline.data.splines[0].bezier_points
        # Adjust the 4 primary control points for a rounded square
        if len(points) >= 4:
            points[0].co.x += 0.5  # Top right - move right
            points[0].co.y += 0.5  # Top right - move up
            
            points[1].co.x -= 0.5  # Top left - move left
            points[1].co.y += 0.5  # Top left - move up
            
            points[2].co.x -= 0.5  # Bottom left - move left
            points[2].co.y -= 0.5  # Bottom left - move down
            
            points[3].co.x += 0.5  # Bottom right - move right
            points[3].co.y -= 0.5  # Bottom right - move down
    
    # For Blender 3.2.1, we'll use a different approach for outline
    outline.data.fill_mode = 'HALF'
    outline.data.bevel_depth = 0.0
    outline.data.resolution_u = 12
    
    # Create material for visibility - using emissive material
    outline_mat = bpy.data.materials.new(name="OutlineMaterial")
    outline_mat.use_nodes = True
    nodes = outline_mat.node_tree.nodes
    links = outline_mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
    
    # Create new nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # Set emission color and strength
    emission.inputs["Color"].default_value = (1.0, 0.3, 0.3, 1.0)  # Bright red
    emission.inputs["Strength"].default_value = 2.0
    
    # Connect nodes
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    
    outline.data.materials.append(outline_mat)
    
    # Create fake dotted appearance by using small cubes along the path
    # This simulates dotted line in a compatible way
    points_count = 24
    for i in range(points_count):
        angle = i * (2 * math.pi / points_count)
        radius = 3.0 + (0.2 if i % 2 == 0 else 0)  # Alternate slight radius variation
        
        # Calculate position
        x = 8 + radius * math.cos(angle)
        y = 4 + radius * math.sin(angle)
        
        # Create small cube for dot
        if i % 2 == 0:  # Place marker every other position for dotted effect
            bpy.ops.mesh.primitive_cube_add(
                size=0.1,
                location=(x, y, 0.01)
            )
            dot = bpy.context.object
            dot.name = f"OutlineDot_{i}"
            dot.data.materials.append(outline_mat)
    
    return outline

def create_sky_and_lighting():
    """Create a dynamic sky that changes from day to night"""
    # Create environment world
    world = bpy.data.worlds['World']
    world.use_nodes = True
    
    # Clear existing nodes
    node_tree = world.node_tree
    nodes = node_tree.nodes
    links = node_tree.links
    for node in nodes:
        nodes.remove(node)
    
    # Add basic nodes for sky (compatible with 3.2.1)
    output = nodes.new(type='ShaderNodeOutputWorld')
    background = nodes.new(type='ShaderNodeBackground')
    
    # Connect nodes
    links.new(background.outputs["Background"], output.inputs["Surface"])
    
    # Create sun lamp for main lighting
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.object
    sun.name = "Sun"
    sun.data.energy = 5.0
    sun.rotation_euler = (math.radians(60), 0, math.radians(45))
    
    return world, sun

def animate_day_to_night_cycle(world, sun, frame_range):
    """Animate the lighting from day to evening/night at end of animation"""
    start_frame, end_frame = frame_range
    
    # Get the background node
    nodes = world.node_tree.nodes
    background = None
    
    for node in nodes:
        if node.type == 'BACKGROUND':
            background = node
            break
    
    if not background:
        return
    
    # Mid-animation frames (daylight)
    mid_frame = (start_frame + end_frame) // 2
    
    # Starting daylight (morning)
    bpy.context.scene.frame_set(start_frame)
    background.inputs["Color"].default_value = (0.8, 0.9, 1.0, 1.0)  # Light blue sky
    background.inputs["Color"].keyframe_insert(frame=start_frame)
    background.inputs["Strength"].default_value = 0.8
    background.inputs["Strength"].keyframe_insert(frame=start_frame)
    
    sun.data.energy = 3.0
    sun.data.keyframe_insert(data_path="energy", frame=start_frame)
    sun.rotation_euler = (math.radians(30), 0, math.radians(20))
    sun.keyframe_insert(data_path="rotation_euler", frame=start_frame)
    
    # Mid-day (bright daylight)
    bpy.context.scene.frame_set(mid_frame)
    background.inputs["Color"].default_value = (0.5, 0.7, 1.0, 1.0)  # Brighter blue
    background.inputs["Color"].keyframe_insert(frame=mid_frame)
    background.inputs["Strength"].default_value = 1.0
    background.inputs["Strength"].keyframe_insert(frame=mid_frame)
    
    sun.data.energy = 5.0
    sun.data.keyframe_insert(data_path="energy", frame=mid_frame)
    sun.rotation_euler = (math.radians(60), 0, math.radians(45))
    sun.keyframe_insert(data_path="rotation_euler", frame=mid_frame)
    
    # End evening/night
    bpy.context.scene.frame_set(end_frame)
    background.inputs["Color"].default_value = (0.1, 0.1, 0.3, 1.0)  # Dark blue evening
    background.inputs["Color"].keyframe_insert(frame=end_frame)
    background.inputs["Strength"].default_value = 0.3
    background.inputs["Strength"].keyframe_insert(frame=end_frame)
    
    sun.data.energy = 1.5
    sun.data.keyframe_insert(data_path="energy", frame=end_frame)
    sun.rotation_euler = (math.radians(15), 0, math.radians(70))
    sun.keyframe_insert(data_path="rotation_euler", frame=end_frame)