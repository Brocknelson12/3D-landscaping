import bpy
import math
from mathutils import Vector
from config import ROBOT_DIMENSIONS, MATERIAL_COLORS

def create_robot():
    """Create the mobile 3D printing robot"""
    # Create materials
    # Metal dark material
    metal_dark = bpy.data.materials.new(name="MetalDark")
    metal_dark.use_nodes = True
    bsdf = metal_dark.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["metal_dark"]
    bsdf.inputs["Metallic"].default_value = 0.9
    bsdf.inputs["Roughness"].default_value = 0.2
    
    # Metal medium material
    metal_med = bpy.data.materials.new(name="MetalMedium")
    metal_med.use_nodes = True
    bsdf = metal_med.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["metal_medium"]
    bsdf.inputs["Metallic"].default_value = 0.9
    bsdf.inputs["Roughness"].default_value = 0.3
    
    # Metal light material
    metal_light = bpy.data.materials.new(name="MetalLight")
    metal_light.use_nodes = True
    bsdf = metal_light.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["metal_light"]
    bsdf.inputs["Metallic"].default_value = 0.9
    bsdf.inputs["Roughness"].default_value = 0.4
    
    # Glass material for sensors
    glass_mat = bpy.data.materials.new(name="Glass")
    glass_mat.use_nodes = True
    bsdf = glass_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["glass"]
    bsdf.inputs["Metallic"].default_value = 0.0
    bsdf.inputs["Roughness"].default_value = 0.1
    bsdf.inputs["Transmission"].default_value = 0.9
    bsdf.inputs["IOR"].default_value = 1.45
    
    # Clay material
    clay_mat = bpy.data.materials.new(name="Clay")
    clay_mat.use_nodes = True
    bsdf = clay_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["clay"]
    bsdf.inputs["Roughness"].default_value = 0.9
    
    # Concrete material
    concrete_mat = bpy.data.materials.new(name="Concrete")
    concrete_mat.use_nodes = True
    bsdf = concrete_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["concrete"]
    bsdf.inputs["Roughness"].default_value = 0.9
    
    # Soil material
    soil_mat = bpy.data.materials.new(name="Soil")
    soil_mat.use_nodes = True
    bsdf = soil_mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = MATERIAL_COLORS["soil"]
    bsdf.inputs["Roughness"].default_value = 1.0
    
    # Create robot empty as parent
    bpy.ops.object.empty_add(location=(0, 0, 0))
    robot_empty = bpy.context.object
    robot_empty.name = "Robot"
    
    # Create robot chassis
    chassis_dims = ROBOT_DIMENSIONS["chassis"]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.4))
    chassis = bpy.context.object
    chassis.name = "RobotChassis"
    chassis.scale = (chassis_dims["width"], chassis_dims["length"], chassis_dims["height"])
    chassis.parent = robot_empty
    
    # Assign material to chassis
    if chassis.data.materials:
        chassis.data.materials[0] = metal_med
    else:
        chassis.data.materials.append(metal_med)
    
    # Create tracks (left)
    track_dims = ROBOT_DIMENSIONS["tracks"]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.8, 0, 0.15))
    track_left = bpy.context.object
    track_left.name = "TrackLeft"
    track_left.scale = (track_dims["width"], track_dims["length"], track_dims["height"])
    track_left.parent = robot_empty
    
    # Assign material to left track
    if track_left.data.materials:
        track_left.data.materials[0] = metal_dark
    else:
        track_left.data.materials.append(metal_dark)
    
    # Create tracks (right)
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.8, 0, 0.15))
    track_right = bpy.context.object
    track_right.name = "TrackRight"
    track_right.scale = (track_dims["width"], track_dims["length"], track_dims["height"])
    track_right.parent = robot_empty
    
    # Assign material to right track
    if track_right.data.materials:
        track_right.data.materials[0] = metal_dark
    else:
        track_right.data.materials.append(metal_dark)
    
    # Create body
    body_dims = ROBOT_DIMENSIONS["body"]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.8))
    body = bpy.context.object
    body.name = "RobotBody"
    body.scale = (body_dims["width"], body_dims["length"], body_dims["height"])
    body.parent = robot_empty
    
    # Assign material to body
    if body.data.materials:
        body.data.materials[0] = metal_light
    else:
        body.data.materials.append(metal_light)
    
    # Create material containers
    # Clay container
    container_dims = ROBOT_DIMENSIONS["material_containers"]["clay"]
    bpy.ops.mesh.primitive_cylinder_add(
        radius=container_dims["radius"], 
        depth=container_dims["height"], 
        location=(-0.5, 0, 1.1)
    )
    clay_container = bpy.context.object
    clay_container.name = "ClayContainer"
    clay_container.parent = robot_empty
    
    # Assign material to clay container
    if clay_container.data.materials:
        clay_container.data.materials[0] = clay_mat
    else:
        clay_container.data.materials.append(clay_mat)
    
    # Soil container
    container_dims = ROBOT_DIMENSIONS["material_containers"]["soil"]
    bpy.ops.mesh.primitive_cylinder_add(
        radius=container_dims["radius"], 
        depth=container_dims["height"], 
        location=(0, 0, 1.1)
    )
    soil_container = bpy.context.object
    soil_container.name = "SoilContainer"
    soil_container.parent = robot_empty
    
    # Assign material to soil container
    if soil_container.data.materials:
        soil_container.data.materials[0] = soil_mat
    else:
        soil_container.data.materials.append(soil_mat)
    
    # Concrete container
    container_dims = ROBOT_DIMENSIONS["material_containers"]["concrete"]
    bpy.ops.mesh.primitive_cylinder_add(
        radius=container_dims["radius"], 
        depth=container_dims["height"], 
        location=(0.5, 0, 1.1)
    )
    concrete_container = bpy.context.object
    concrete_container.name = "ConcreteContainer"
    concrete_container.parent = robot_empty
    
    # Assign material to concrete container
    if concrete_container.data.materials:
        concrete_container.data.materials[0] = concrete_mat
    else:
        concrete_container.data.materials.append(concrete_mat)
    
    # Create scanner mast
    bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.8, location=(0, 0.4, 1.4))
    scanner_mast = bpy.context.object
    scanner_mast.name = "ScannerMast"
    scanner_mast.parent = robot_empty
    
    # Assign material to scanner mast
    if scanner_mast.data.materials:
        scanner_mast.data.materials[0] = metal_med
    else:
        scanner_mast.data.materials.append(metal_med)
    
    # Create scanner head
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0, 0.4, 1.8))
    scanner_head = bpy.context.object
    scanner_head.name = "ScannerHead"
    scanner_head.parent = robot_empty
    
    # Assign material to scanner head
    if scanner_head.data.materials:
        scanner_head.data.materials[0] = glass_mat
    else:
        scanner_head.data.materials.append(glass_mat)
    
    # Create printing arm base
    arm_dims = ROBOT_DIMENSIONS["arm"]
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.5, 0.7))
    arm_base = bpy.context.object
    arm_base.name = "ArmBase"
    arm_base.scale = (arm_dims["width"] * 3, arm_dims["width"], 0.1)
    arm_base.parent = robot_empty
    
    # Assign material to arm base
    if arm_base.data.materials:
        arm_base.data.materials[0] = metal_med
    else:
        arm_base.data.materials.append(metal_med)
    
    # Create printing arm extension
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.8, 0.6))
    arm_extension = bpy.context.object
    arm_extension.name = "ArmExtension"
    arm_extension.scale = (0.1, 0.3, 0.1)
    arm_extension.parent = robot_empty
    
    # Assign material to arm extension
    if arm_extension.data.materials:
        arm_extension.data.materials[0] = metal_med
    else:
        arm_extension.data.materials.append(metal_med)
    
    # Create print head
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.8, 0.4))
    print_head = bpy.context.object
    print_head.name = "PrintHead"
    print_head.scale = (0.3, 0.15, 0.1)
    print_head.parent = robot_empty
    
    # Assign material to print head
    if print_head.data.materials:
        print_head.data.materials[0] = metal_dark
    else:
        print_head.data.materials.append(metal_dark)
    
    # Create print nozzles
    nozzle_positions = [(-0.15, -0.8, 0.3), (0, -0.8, 0.3), (0.15, -0.8, 0.3)]
    nozzle_materials = [clay_mat, soil_mat, concrete_mat]
    nozzle_names = ["ClayNozzle", "SoilNozzle", "ConcreteNozzle"]
    nozzle_dims = [
        ROBOT_DIMENSIONS["nozzles"]["clay"],
        ROBOT_DIMENSIONS["nozzles"]["soil"],
        ROBOT_DIMENSIONS["nozzles"]["concrete"]
    ]
    
    for i, (pos, mat, name, dims) in enumerate(zip(nozzle_positions, nozzle_materials, nozzle_names, nozzle_dims)):
        bpy.ops.mesh.primitive_cylinder_add(radius=dims["radius"], depth=0.1, location=pos)
        nozzle = bpy.context.object
        nozzle.name = name
        nozzle.parent = robot_empty
        
        # Assign material to nozzle
        if nozzle.data.materials:
            nozzle.data.materials[0] = mat
        else:
            nozzle.data.materials.append(mat)
    
    return robot_empty