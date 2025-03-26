import bpy
import math
from mathutils import Vector

def create_tube_system():
    """Create the three tubes mounted on the fence with motors and plugs"""
    # Create collection for tube system
    tube_collection = bpy.data.collections.new("TubeSystem")
    bpy.context.scene.collection.children.link(tube_collection)
    
    # Define positions for the three tubes along the fence
    tube_positions = [
        {"pos": (4, 0.1, 1.2), "name": "ClayTube", "color": (0.7, 0.5, 0.3, 1.0)},  # Clay tube
        {"pos": (6, 0.1, 1.2), "name": "SoilTube", "color": (0.3, 0.2, 0.1, 1.0)},  # Soil tube
        {"pos": (8, 0.1, 1.2), "name": "SeedTube", "color": (0.2, 0.3, 0.1, 1.0)}   # Seed tube
    ]
    
    tubes = []
    for tube_info in tube_positions:
        tube = create_single_tube(tube_info["pos"], tube_info["name"], tube_info["color"])
        tube_collection.objects.link(tube)
        tubes.append(tube)
    
    return tubes

def create_single_tube(position, name, color):
    """Create a single tube with motor and plug"""
    # Create tube empty to hold all parts
    bpy.ops.object.empty_add(location=position)
    tube_empty = bpy.context.object
    tube_empty.name = name
    
    # Create the motor housing
    motor_size = 0.4
    bpy.ops.mesh.primitive_cylinder_add(
        radius=motor_size, 
        depth=motor_size*1.5,
        location=(position[0], position[1] + 0.3, position[2])
    )
    motor = bpy.context.object
    motor.name = f"{name}_Motor"
    motor.rotation_euler = (math.radians(90), 0, 0)  # Rotate to face outward
    motor.parent = tube_empty
    
    # Create motor material
    motor_mat = bpy.data.materials.new(name=f"{name}_MotorMaterial")
    motor_mat.use_nodes = True
    nodes = motor_mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark
    principled.inputs["Base Color"].default_value = (0.2, 0.2, 0.2, 1.0)  # Dark gray
    principled.inputs["Metallic"].default_value = 0.9
    principled.inputs["Roughness"].default_value = 0.2
    motor.data.materials.append(motor_mat)
    
    # Create the tube
    tube_length = 10.0
    tube_radius = 0.15
    
    # Main tube cylinder
    bpy.ops.mesh.primitive_cylinder_add(
        radius=tube_radius,
        depth=tube_length,
        location=(position[0], position[1] - tube_length/2, position[2])
    )
    tube = bpy.context.object
    tube.name = f"{name}_Pipe"
    tube.rotation_euler = (math.radians(90), 0, 0)  # Align along y-axis
    tube.parent = tube_empty
    
    # Create tube material with transparency
    tube_mat = bpy.data.materials.new(name=f"{name}_TubeMaterial")
    tube_mat.use_nodes = True
    nodes = tube_mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    
    # Mix transparent and solid to see contents
    principled.inputs["Base Color"].default_value = color
    principled.inputs["Metallic"].default_value = 0.0
    principled.inputs["Roughness"].default_value = 0.1
    principled.inputs["Transmission"].default_value = 0.8
    principled.inputs["IOR"].default_value = 1.45
    tube.data.materials.append(tube_mat)
    
    # Create the plug at the end of the tube
    bpy.ops.mesh.primitive_cylinder_add(
        radius=tube_radius * 1.2,
        depth=tube_radius * 2,
        location=(position[0], position[1] - tube_length, position[2])
    )
    plug = bpy.context.object
    plug.name = f"{name}_Plug"
    plug.rotation_euler = (math.radians(90), 0, 0)
    plug.parent = tube_empty
    
    # Create plug material
    plug_mat = bpy.data.materials.new(name=f"{name}_PlugMaterial")
    plug_mat.use_nodes = True
    nodes = plug_mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.8, 0.1, 0.1, 1.0)  # Red
    principled.inputs["Roughness"].default_value = 0.3
    plug.data.materials.append(plug_mat)
    
    # Create a control valve
    bpy.ops.mesh.primitive_torus_add(
        major_radius=tube_radius * 2,
        minor_radius=tube_radius * 0.5,
        location=(position[0], position[1] - tube_length + 1, position[2])
    )
    valve = bpy.context.object
    valve.name = f"{name}_Valve"
    valve.rotation_euler = (0, math.radians(90), 0)
    valve.parent = tube_empty
    
    # Create valve material
    valve_mat = bpy.data.materials.new(name=f"{name}_ValveMaterial")
    valve_mat.use_nodes = True
    nodes = valve_mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.1, 0.1, 0.7, 1.0)  # Blue
    principled.inputs["Metallic"].default_value = 0.9
    principled.inputs["Roughness"].default_value = 0.1
    valve.data.materials.append(valve_mat)
    
    # Add contents inside the transparent tube (visible material)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=tube_radius * 0.6,
        depth=tube_length * 0.9,
        location=(position[0], position[1] - tube_length/2, position[2])
    )
    contents = bpy.context.object
    contents.name = f"{name}_Contents"
    contents.rotation_euler = (math.radians(90), 0, 0)
    contents.parent = tube_empty
    
    # Create contents material
    contents_mat = bpy.data.materials.new(name=f"{name}_ContentsMaterial")
    contents_mat.use_nodes = True
    nodes = contents_mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = color
    principled.inputs["Roughness"].default_value = 1.0
    contents.data.materials.append(contents_mat)
    
    return tube_empty