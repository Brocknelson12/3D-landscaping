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


def enhance_robot_model(robot_empty):
    """Add detailed components to the basic robot model"""
    # Add hydraulic system for the printing arm
    create_hydraulic_system(robot_empty)
    
    # Add material flow pipes and tubing
    create_material_flow_system(robot_empty)
    
    # Add status lights and sensors
    add_status_indicators(robot_empty)
    
    # Add wear and tear to robot surfaces
    add_wear_to_all_components(robot_empty)
    
    return robot_empty

def create_hydraulic_system(robot_empty):
    """Create hydraulic pistons for the robot's arm system"""
    # Find the arm components
    arm_base = None
    arm_extension = None
    print_head = None
    
    for child in robot_empty.children:
        if "ArmBase" in child.name:
            arm_base = child
        elif "ArmExtension" in child.name:
            arm_extension = child
        elif "PrintHead" in child.name:
            print_head = child
    
    if not arm_base or not arm_extension or not print_head:
        return
    
    # Create metal material for hydraulics
    hydraulic_mat = bpy.data.materials.new(name="HydraulicMaterial")
    hydraulic_mat.use_nodes = True
    principled = hydraulic_mat.node_tree.nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1.0)  # Light gray
    principled.inputs["Metallic"].default_value = 1.0
    principled.inputs["Roughness"].default_value = 0.2
    
    # Create hydraulic piston from arm base to extension
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.05,
        depth=0.4,
        location=(0, -0.65, 0.7)
    )
    piston1 = bpy.context.object
    piston1.name = "HydraulicPiston1"
    piston1.rotation_euler = (math.radians(90), 0, 0)
    piston1.parent = robot_empty
    piston1.data.materials.append(hydraulic_mat)
    
    # Create piston rod (smaller cylinder)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02,
        depth=0.5,
        location=(0, -0.7, 0.65)
    )
    rod1 = bpy.context.object
    rod1.name = "HydraulicRod1"
    rod1.rotation_euler = (math.radians(70), 0, 0)  # Angled
    rod1.parent = robot_empty
    rod1.data.materials.append(hydraulic_mat)
    
    # Create second hydraulic for up/down movement
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.04,
        depth=0.3,
        location=(0, -0.75, 0.5)
    )
    piston2 = bpy.context.object
    piston2.name = "HydraulicPiston2"
    piston2.rotation_euler = (math.radians(100), 0, 0)
    piston2.parent = robot_empty
    piston2.data.materials.append(hydraulic_mat)
    
    # Create hydraulic connectors (small spheres)
    positions = [(0, -0.65, 0.7), (0, -0.7, 0.43)]
    for i, pos in enumerate(positions):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.03,
            location=pos
        )
        connector = bpy.context.object
        connector.name = f"HydraulicConnector{i}"
        connector.parent = robot_empty
        connector.data.materials.append(hydraulic_mat)

def create_material_flow_system(robot_empty):
    """Create visible piping system from material containers to print head"""
    # Find the relevant components
    containers = []
    nozzles = []
    
    for child in robot_empty.children:
        if "Container" in child.name:
            containers.append(child)
        elif "Nozzle" in child.name:
            nozzles.append(child)
    
    if not containers or not nozzles:
        return
        
    # Create flexible tube material (translucent)
    tube_mat = bpy.data.materials.new(name="FlexibleTubeMaterial")
    tube_mat.use_nodes = True
    principled = tube_mat.node_tree.nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.9, 0.9, 0.9, 1.0)  # Light gray
    principled.inputs["Metallic"].default_value = 0.0
    principled.inputs["Roughness"].default_value = 0.3
    principled.inputs["Transmission"].default_value = 0.2
    principled.inputs["IOR"].default_value = 1.4
    
    # For each container, create a tube to the corresponding nozzle
    for i, container in enumerate(containers):
        if i >= len(nozzles):
            break
            
        nozzle = nozzles[i]
        
        # Get positions
        container_pos = container.matrix_world.translation
        nozzle_pos = nozzle.matrix_world.translation
        
        # Create connection points
        container_bottom = container_pos + Vector((0, 0, -container.dimensions.z/2))
        
        # Create control points for tube path
        points = [
            container_bottom,
            container_bottom + Vector((0, -0.2, -0.1)),
            nozzle_pos + Vector((0, 0.2, 0.1)),
            nozzle_pos
        ]
        
        # Create tube using bezier curve
        bpy.ops.curve.primitive_bezier_curve_add()
        tube_curve = bpy.context.object
        tube_curve.name = f"MaterialTube_{container.name.split('Container')[0]}"
        
        # Update the curve points
        bezier_points = tube_curve.data.splines[0].bezier_points
        
        # Add points if needed
        while len(bezier_points) < len(points):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.curve.select_all(action='SELECT')
            bpy.ops.curve.subdivide(number_cuts=1)
            bpy.ops.object.mode_set(mode='OBJECT')
            bezier_points = tube_curve.data.splines[0].bezier_points
        
        # Set point positions
        for j, point in enumerate(points):
            if j < len(bezier_points):
                bezier_points[j].co = point - robot_empty.matrix_world.translation
                
                # Calculate handle positions for smooth curve
                if j > 0:
                    dir_prev = (points[j] - points[j-1]).normalized()
                    bezier_points[j].handle_left = bezier_points[j].co - dir_prev * 0.2
                if j < len(points) - 1:
                    dir_next = (points[j+1] - points[j]).normalized()
                    bezier_points[j].handle_right = bezier_points[j].co + dir_next * 0.2
        
        # Set tube properties
        tube_curve.data.fill_mode = 'FULL'
        tube_curve.data.bevel_depth = 0.015  # Radius of tube
        tube_curve.data.bevel_resolution = 4  # Smoothness
        
        # Assign material
        tube_curve.data.materials.append(tube_mat)
        
        # Parent to robot
        tube_curve.parent = robot_empty

def add_status_indicators(robot_empty):
    """Add LED status lights and display panel to the robot"""
    # Create emission material for LEDs
    led_materials = {
        "red": create_led_material((1.0, 0.1, 0.1, 1.0), "RedLED"),
        "green": create_led_material((0.1, 1.0, 0.1, 1.0), "GreenLED"),
        "blue": create_led_material((0.1, 0.1, 1.0, 1.0), "BlueLED"),
        "yellow": create_led_material((1.0, 1.0, 0.1, 1.0), "YellowLED")
    }
    
    # Create LED positions on the robot body
    body = None
    for child in robot_empty.children:
        if "Body" in child.name:
            body = child
            break
    
    if not body:
        return
        
    # Get body position and dimensions
    body_pos = body.matrix_world.translation
    body_dim = body.dimensions
    
    # Create LED strip on front of robot
    led_positions = [
        {"pos": Vector((0.4, 0.35, 0.9)), "color": "red", "name": "StatusLED"},
        {"pos": Vector((0.2, 0.35, 0.9)), "color": "yellow", "name": "ProcessLED"},
        {"pos": Vector((0.0, 0.35, 0.9)), "color": "green", "name": "PowerLED"},
        {"pos": Vector((-0.2, 0.35, 0.9)), "color": "blue", "name": "ConnectionLED"}
    ]
    
    for led_info in led_positions:
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.02,
            depth=0.01,
            location=led_info["pos"]
        )
        led = bpy.context.object
        led.name = led_info["name"]
        led.rotation_euler = (math.radians(90), 0, 0)
        led.parent = robot_empty
        led.data.materials.append(led_materials[led_info["color"]])
        
    # Create a small display screen
    bpy.ops.mesh.primitive_cube_add(
        size=1.0,
        location=(0, 0.35, 0.75)
    )
    display = bpy.context.object
    display.name = "ControlDisplay"
    display.scale = (0.5, 0.02, 0.2)
    display.parent = robot_empty
    
    # Create display material
    display_mat = bpy.data.materials.new(name="DisplayMaterial")
    display_mat.use_nodes = True
    nodes = display_mat.node_tree.nodes
    links = display_mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # Add screen texture
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    
    # Create a grid pattern for the display
    grid = nodes.new(type='ShaderNodeTexChecker')
    grid.inputs["Scale"].default_value = 10.0
    
    color_ramp = nodes.new(type='ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = 0.4
    color_ramp.color_ramp.elements[0].color = (0.0, 0.2, 0.4, 1.0)  # Dark blue
    color_ramp.color_ramp.elements[1].position = 0.6
    color_ramp.color_ramp.elements[1].color = (0.0, 0.5, 1.0, 1.0)  # Light blue
    
    # Connect nodes
    links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], grid.inputs["Vector"])
    links.new(grid.outputs["Color"], color_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], emission.inputs["Color"])
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    
    # Assign material
    display.data.materials.append(display_mat)
    
    # Animate LED blinking
    for led_info in led_positions:
        led_name = led_info["name"]
        led = bpy.data.objects.get(led_name)
        
        if not led:
            continue
            
        # Create animation data if needed
        if not led.animation_data:
            led.animation_data_create()
            
        # Find material
        mat = led.data.materials[0]
        
        # Animate emission strength
        nodes = mat.node_tree.nodes
        emission = None
        
        for node in nodes:
            if node.type == 'EMISSION':
                emission = node
                break
                
        if not emission:
            continue
            
        # Animate based on LED type
        if "Status" in led_name:
            # Regular blinking
            for i in range(0, 150, 30):
                # On
                bpy.context.scene.frame_set(i)
                emission.inputs["Strength"].default_value = 5.0
                emission.inputs["Strength"].keyframe_insert(frame=i)
                
                # Off
                bpy.context.scene.frame_set(i + 15)
                emission.inputs["Strength"].default_value = 0.5
                emission.inputs["Strength"].keyframe_insert(frame=i + 15)
                
        elif "Process" in led_name:
            # Slow pulsing
            for i in range(0, 150, 60):
                # Glow start
                bpy.context.scene.frame_set(i)
                emission.inputs["Strength"].default_value = 1.0
                emission.inputs["Strength"].keyframe_insert(frame=i)
                
                # Peak
                bpy.context.scene.frame_set(i + 30)
                emission.inputs["Strength"].default_value = 5.0
                emission.inputs["Strength"].keyframe_insert(frame=i + 30)
                
                # Glow end
                bpy.context.scene.frame_set(i + 60)
                emission.inputs["Strength"].default_value = 1.0
                emission.inputs["Strength"].keyframe_insert(frame=i + 60)
        
        elif "Power" in led_name:
            # Steady with occasional pulse
            # Base steady state
            bpy.context.scene.frame_set(1)
            emission.inputs["Strength"].default_value = 3.0
            emission.inputs["Strength"].keyframe_insert(frame=1)
            
            # Just a few pulses
            pulse_frames = [40, 90, 140]
            for i in pulse_frames:
                # Brighter
                bpy.context.scene.frame_set(i)
                emission.inputs["Strength"].default_value = 3.0
                emission.inputs["Strength"].keyframe_insert(frame=i)
                
                # Peak
                bpy.context.scene.frame_set(i + 5)
                emission.inputs["Strength"].default_value = 6.0
                emission.inputs["Strength"].keyframe_insert(frame=i + 5)
                
                # Back to normal
                bpy.context.scene.frame_set(i + 10)
                emission.inputs["Strength"].default_value = 3.0
                emission.inputs["Strength"].keyframe_insert(frame=i + 10)
        
        elif "Connection" in led_name:
            # Rapid data-like blinking pattern
            for i in range(0, 150, 5):
                # Random pattern of bright and dim
                bpy.context.scene.frame_set(i)
                if random.random() > 0.3:  # 70% chance of being bright
                    emission.inputs["Strength"].default_value = 4.0
                else:
                    emission.inputs["Strength"].default_value = 0.5
                emission.inputs["Strength"].keyframe_insert(frame=i)

def add_wear_to_all_components(robot_empty):
    """Add wear and tear to all robot components"""
    for child in robot_empty.children:
        if child.type == 'MESH' and child.data.materials:
            for slot in child.material_slots:
                material = slot.material
                if material and material.use_nodes:
                    add_wear_to_material(material, child.name)

def add_wear_to_material(material, object_name):
    """Add wear and tear to a material based on object type"""
    # Determine wear amount based on part type
    wear_amount = 0.2  # Default
    
    if "Track" in object_name:
        wear_amount = 0.4  # More wear on tracks
    elif "Arm" in object_name or "Print" in object_name:
        wear_amount = 0.3  # Medium wear on moving parts
    elif "Body" in object_name or "Chassis" in object_name:
        wear_amount = 0.15  # Less wear on main body
    
    # Get material nodes
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    # Find Principled BSDF
    principled = None
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled = node
            break
    
    if not principled:
        return
        
    # Original color and roughness
    orig_color = principled.inputs["Base Color"].default_value
    orig_roughness = principled.inputs["Roughness"].default_value
    
    # Add noise texture for wear pattern
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.inputs["Scale"].default_value = 20.0
    noise.inputs["Detail"].default_value = 10.0
    
    # Add color ramp to control wear intensity
    ramp = nodes.new(type='ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.4
    ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)  # No wear
    ramp.color_ramp.elements[1].position = 0.6
    ramp.color_ramp.elements[1].color = (0.3, 0.3, 0.3, 1.0)  # Worn
    
    # Mix node to blend base color with wear
    mix = nodes.new(type='ShaderNodeMixRGB')
    mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = wear_amount
    mix.inputs[1].default_value = orig_color
    
    # Connect nodes
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], mix.inputs[2])
    links.new(mix.outputs["Color"], principled.inputs["Base Color"])
    
    # Add bump for surface scratches
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs["Strength"].default_value = wear_amount * 0.3
    
    # Connect noise to bump
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], principled.inputs["Normal"])
    
    # Increase roughness slightly
    principled.inputs["Roughness"].default_value = min(1.0, orig_roughness + (wear_amount * 0.3))

def create_led_material(color, name):
    """Create an emissive material for LEDs"""
    led_mat = bpy.data.materials.new(name=name)
    led_mat.use_nodes = True
    nodes = led_mat.node_tree.nodes
    links = led_mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add emission node
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # Set emission color and strength
    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = 3.0
    
    # Connect nodes
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    
    return led_mat