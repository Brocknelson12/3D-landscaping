import bpy
import math

def clear_scene():
    """Clear all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # Clear all materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    # Clear all meshes
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    
    # Clear all textures
    for texture in bpy.data.textures:
        bpy.data.textures.remove(texture)

def setup_environment():
    """Set up scene, lighting, and render settings"""
    # Create world sky
    world = bpy.data.worlds['World']
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (0.76, 0.83, 1.0, 1.0)  # Light blue
    bg.inputs[1].default_value = 1.0  # Strength
    
    # Create sun light
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.object
    sun.data.energy = 5.0
    sun.rotation_euler = (math.radians(60), 0, math.radians(30))
    
    # Create camera
    bpy.ops.object.camera_add(location=(8, -8, 5))
    camera = bpy.context.object
    camera.rotation_euler = (math.radians(60), 0, math.radians(45))
    bpy.context.scene.camera = camera
    
    # Create a camera animation to circle around the scene
    camera.animation_data_create()
    camera.animation_data.action = bpy.data.actions.new(name="CameraAnimation")
    
    # Keyframe initial position
    camera.keyframe_insert(data_path="location", frame=1)
    
    # Keyframe final position (moved slightly around)
    bpy.context.scene.frame_set(150)
    camera.location = (6, -10, 6)
    camera.rotation_euler = (math.radians(55), 0, math.radians(30))
    camera.keyframe_insert(data_path="location", frame=150)
    camera.keyframe_insert(data_path="rotation_euler", frame=150)
    
    # Return to frame 1
    bpy.context.scene.frame_set(1)