import bpy
import math
from mathutils import Vector
from config import GARDEN_PATH_SETTINGS, MATERIAL_COLORS

def create_garden_path(control_points=None):
    """Create the garden path that will be 3D printed with enhanced materials"""
    # Use provided control points or default from settings
    if control_points is None:
        control_points = GARDEN_PATH_SETTINGS["control_points"]
    
    # Create a path curve
    bpy.ops.curve.primitive_bezier_curve_add(location=(0, 0, 0.05))
    garden_path = bpy.context.object
    garden_path.name = "GardenPath"
    
    # Modify the curve points to create a curved garden bed outline
    points = garden_path.data.splines[0].bezier_points
    
    # If there are more points in control_points than in the curve, add points
    while len(points) < len(control_points):
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.subdivide(number_cuts=1)
        bpy.ops.object.mode_set(mode='OBJECT')
        points = garden_path.data.splines[0].bezier_points
    
    # Update points with the control points
    for i, cp in enumerate(control_points):
        if i < len(points):
            points[i].co = Vector(cp["co"])
            points[i].handle_left = Vector(cp["handle_left"])
            points[i].handle_right = Vector(cp["handle_right"])
    
    # Make the curve closed
    garden_path.data.splines[0].use_cyclic_u = True
    
    # Create enhanced concrete material
    border_mat = create_enhanced_concrete_material()
    
    # Set bevel for the curve with an enhanced profile
    garden_path.data.bevel_depth = GARDEN_PATH_SETTINGS["bevel_depth"] * 1.2  # Slightly thicker
    garden_path.data.bevel_resolution = GARDEN_PATH_SETTINGS["bevel_resolution"] + 2  # Smoother
    
    # Create a U-shaped profile for the garden bed border
    # Create a new curve for the bevel object
    bpy.ops.curve.primitive_bezier_circle_add(radius=1.0, enter_editmode=True, location=(0, 0, 0))
    bevel_curve = bpy.context.object
    bevel_curve.name = "GardenBorderProfile"
    
    # Create U-shape by modifying points
    bpy.ops.curve.select_all(action='SELECT')
    bpy.ops.curve.delete(type='VERT')
    
    # Add points to create U shape
    bpy.ops.curve.select_all(action='DESELECT')
    bpy.ops.curve.vertex_add(location=(0.5, 0, 0))
    bpy.ops.curve.vertex_add(location=(0, 0.5, 0))
    bpy.ops.curve.vertex_add(location=(-0.5, 0, 0))
    
    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Set the curve fill to 'FULL'
    bevel_curve.data.fill_mode = 'FULL'
    garden_path.data.bevel_object = bevel_curve
    
    # Start with bevel factor at 0 (for animation)
    garden_path.data.bevel_factor_end = 0.0
    
    # Assign material
    if garden_path.data.materials:
        garden_path.data.materials[0] = border_mat
    else:
        garden_path.data.materials.append(border_mat)
    
    # Hide path and bevel object initially
    garden_path.hide_viewport = True
    garden_path.hide_render = True
    bevel_curve.hide_viewport = True
    bevel_curve.hide_render = True
    
    return garden_path

def create_soil_fill(garden_path):
    """Create the soil that will fill the garden bed with enhanced appearance"""
    # Create a copy of the garden path for the soil fill
    soil_fill = garden_path.copy()
    soil_fill.data = garden_path.data.copy()
    soil_fill.name = "SoilFill"
    bpy.context.collection.objects.link(soil_fill)
    
    # Adjust the bevel to be higher (deeper soil)
    soil_fill.data.bevel_depth = GARDEN_PATH_SETTINGS["bevel_depth"] * 0.9  # Slightly lower than border
    
    # Create a different bevel object for the soil (flat bottom)
    bpy.ops.curve.primitive_bezier_circle_add(radius=1.0, enter_editmode=True, location=(0, 0, 0))
    soil_bevel = bpy.context.object
    soil_bevel.name = "SoilProfile"
    
    # Create flat-bottom shape
    bpy.ops.curve.select_all(action='SELECT')
    bpy.ops.curve.delete(type='VERT')
    
    # Add points for flat bottom shape
    bpy.ops.curve.select_all(action='DESELECT')
    bpy.ops.curve.vertex_add(location=(0.5, -0.1, 0))  # Right edge
    bpy.ops.curve.vertex_add(location=(0, -0.1, 0))    # Bottom center
    bpy.ops.curve.vertex_add(location=(-0.5, -0.1, 0)) # Left edge
    
    # Exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Set the curve fill to 'FULL'
    soil_bevel.data.fill_mode = 'FULL'
    soil_fill.data.bevel_object = soil_bevel
    
    # Start with bevel factor at 0 (for animation)
    soil_fill.data.bevel_factor_end = 0.0
    
    # Create enhanced soil material
    soil_mat = create_enhanced_soil_material()
    
    # Assign material
    if soil_fill.data.materials:
        soil_fill.data.materials[0] = soil_mat
    else:
        soil_fill.data.materials.append(soil_mat)
    
    # Hide soil and its bevel object initially
    soil_fill.hide_viewport = True
    soil_fill.hide_render = True
    soil_bevel.hide_viewport = True
    soil_bevel.hide_render = True
    
    return soil_fill

def create_seed_placement(garden_path):
    """Create visual markers for seed placement"""
    # Create a collection for seeds
    seed_collection = bpy.data.collections.new("Seeds")
    bpy.context.scene.collection.children.link(seed_collection)
    
    # Get the path of the garden bed
    curve_length = get_curve_length(garden_path)
    
    # Determine number of seeds based on garden size
    num_seeds = int(curve_length / 0.5)  # One seed every ~0.5 blender units
    
    # Create seed markers along the path
    seed_markers = []
    
    for i in range(num_seeds):
        # Get position along curve
        t = i / num_seeds
        position = get_point_on_curve(garden_path, t)
        
        # Create seed marker
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=position)
        seed = bpy.context.object
        seed.name = f"Seed_{i}"
        
        # Add to collection
        seed_collection.objects.link(seed)
        bpy.context.scene.collection.objects.unlink(seed)
        
        # Create seed material if needed
        if i == 0:
            seed_mat = bpy.data.materials.new(name="SeedMaterial")
            seed_mat.use_nodes = True
            principled = seed_mat.node_tree.nodes["Principled BSDF"]
            principled.inputs["Base Color"].default_value = (0.35, 0.2, 0.05, 1.0)  # Dark brown
            principled.inputs["Roughness"].default_value = 0.6
            principled.inputs["Specular"].default_value = 0.2
        
        # Assign material
        if seed.data.materials:
            seed.data.materials[0] = seed_mat
        else:
            seed.data.materials.append(seed_mat)
        
        # Hide initially
        seed.hide_viewport = True
        seed.hide_render = True
        
        seed_markers.append(seed)
    
    return seed_markers

def create_enhanced_concrete_material():
    """Create an enhanced concrete material for garden border"""
    concrete_mat = bpy.data.materials.new(name="ConcretePath")
    concrete_mat.use_nodes = True
    
    # Get node tree
    nodes = concrete_mat.node_tree.nodes
    links = concrete_mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add new nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    
    # Noise texture for base variation
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.inputs["Scale"].default_value = 30.0
    noise.inputs["Detail"].default_value = 10.0
    noise.inputs["Roughness"].default_value = 0.7
    
    # Voronoi texture for aggregate appearance
    voronoi = nodes.new(type='ShaderNodeTexVoronoi')
    voronoi.voronoi_dimensions = '3D'
    voronoi.inputs["Scale"].default_value = 50.0
    
    # Color ramps for control
    color_ramp1 = nodes.new(type='ShaderNodeValToRGB')
    color_ramp1.color_ramp.elements[0].position = 0.4
    color_ramp1.color_ramp.elements[0].color = (0.6, 0.6, 0.6, 1.0)  # Light gray
    color_ramp1.color_ramp.elements[1].position = 0.6
    color_ramp1.color_ramp.elements[1].color = (0.75, 0.75, 0.75, 1.0)  # Lighter gray
    
    color_ramp2 = nodes.new(type='ShaderNodeValToRGB')
    color_ramp2.color_ramp.elements[0].position = 0.4
    color_ramp2.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)  # White
    color_ramp2.color_ramp.elements[1].position = 0.6
    color_ramp2.color_ramp.elements[1].color = (0.2, 0.2, 0.2, 1.0)  # Dark
    
    # Mix nodes
    mix1 = nodes.new(type='ShaderNodeMixRGB')
    mix1.blend_type = 'MULTIPLY'
    mix1.inputs[0].default_value = 0.1
    
    # Bump node for surface detail
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs["Strength"].default_value = 0.3
    bump.inputs["Distance"].default_value = 0.02
    
    # Position nodes
    output.location = (600, 0)
    principled.location = (400, 0)
    bump.location = (200, -150)
    mix1.location = (200, 100)
    color_ramp1.location = (0, 150)
    color_ramp2.location = (0, 0)
    noise.location = (-200, 150)
    voronoi.location = (-200, 0)
    tex_coord.location = (-600, 0)
    mapping.location = (-400, 0)
    
    # Connect nodes
    links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise.inputs["Vector"])
    links.new(mapping.outputs["Vector"], voronoi.inputs["Vector"])
    
    links.new(noise.outputs["Fac"], color_ramp1.inputs["Fac"])
    links.new(voronoi.outputs["Distance"], color_ramp2.inputs["Fac"])
    
    links.new(color_ramp1.outputs["Color"], mix1.inputs[1])
    links.new(color_ramp2.outputs["Color"], mix1.inputs[2])
    
    links.new(mix1.outputs["Color"], principled.inputs["Base Color"])
    links.new(noise.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], principled.inputs["Normal"])
    
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    
    # Set material properties
    principled.inputs["Roughness"].default_value = 0.9
    principled.inputs["Specular"].default_value = 0.1
    
    return concrete_mat

def create_enhanced_soil_material():
    """Create an enhanced soil material for garden fill"""
    soil_mat = bpy.data.materials.new(name="SoilFill")
    soil_mat.use_nodes = True
    
    # Get node tree
    nodes = soil_mat.node_tree.nodes
    links = soil_mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add new nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    tex_coord = nodes.new(type='ShaderNodeTexCoord')
    mapping = nodes.new(type='ShaderNodeMapping')
    
    # Noise texture for soil variation
    noise1 = nodes.new(type='ShaderNodeTexNoise')
    noise1.inputs["Scale"].default_value = 20.0
    noise1.inputs["Detail"].default_value = 12.0
    noise1.inputs["Distortion"].default_value = 1.0
    
    # Second noise for micro detail
    noise2 = nodes.new(type='ShaderNodeTexNoise')
    noise2.inputs["Scale"].default_value = 50.0
    noise2.inputs["Detail"].default_value = 6.0
    
    # Voronoi for soil clumps
    voronoi = nodes.new(type='ShaderNodeTexVoronoi')
    voronoi.voronoi_dimensions = '3D'
    voronoi.inputs["Scale"].default_value = 30.0
    
    # Color ramps
    color_ramp1 = nodes.new(type='ShaderNodeValToRGB')
    color_ramp1.color_ramp.elements[0].position = 0.4
    color_ramp1.color_ramp.elements[0].color = (0.2, 0.12, 0.05, 1.0)  # Dark soil
    color_ramp1.color_ramp.elements[1].position = 0.7
    color_ramp1.color_ramp.elements[1].color = (0.3, 0.2, 0.1, 1.0)  # Lighter soil
    
    color_ramp2 = nodes.new(type='ShaderNodeValToRGB')
    color_ramp2.color_ramp.elements[0].position = 0.3
    color_ramp2.color_ramp.elements[0].color = (0.9, 0.9, 0.9, 1.0)  # Light for highlights
    color_ramp2.color_ramp.elements[1].position = 0.7
    color_ramp2.color_ramp.elements[1].color = (0.1, 0.1, 0.1, 1.0)  # Dark for lowlights
    
    # Mix nodes
    mix1 = nodes.new(type='ShaderNodeMixRGB')
    mix1.blend_type = 'MULTIPLY'
    mix1.inputs[0].default_value = 0.2
    
    # Bump node for surface detail
    bump = nodes.new(type='ShaderNodeBump')
    bump.inputs["Strength"].default_value = 0.5
    bump.inputs["Distance"].default_value = 0.03
    
    # Mix for bump influence
    mix_bump = nodes.new(type='ShaderNodeMixRGB')
    mix_bump.blend_type = 'ADD'
    mix_bump.inputs[0].default_value = 0.5
    
    # Position nodes
    output.location = (700, 0)
    principled.location = (500, 0)
    bump.location = (300, -150)
    mix1.location = (300, 100)
    mix_bump.location = (100, -150)
    color_ramp1.location = (100, 150)
    color_ramp2.location = (100, 0)
    noise1.location = (-100, 150)
    noise2.location = (-100, -150)
    voronoi.location = (-100, 0)
    tex_coord.location = (-500, 0)
    mapping.location = (-300, 0)
    
    # Connect nodes
    links.new(tex_coord.outputs["Generated"], mapping.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise1.inputs["Vector"])
    links.new(mapping.outputs["Vector"], noise2.inputs["Vector"])
    links.new(mapping.outputs["Vector"], voronoi.inputs["Vector"])
    
    links.new(noise1.outputs["Fac"], color_ramp1.inputs["Fac"])
    links.new(voronoi.outputs["Distance"], color_ramp2.inputs["Fac"])
    
    links.new(color_ramp1.outputs["Color"], mix1.inputs[1])
    links.new(color_ramp2.outputs["Color"], mix1.inputs[2])
    
    links.new(noise1.outputs["Fac"], mix_bump.inputs[1])
    links.new(noise2.outputs["Fac"], mix_bump.inputs[2])
    
    links.new(mix1.outputs["Color"], principled.inputs["Base Color"])
    links.new(mix_bump.outputs["Color"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], principled.inputs["Normal"])
    
    links.new(principled.outputs["BSDF"], output.inputs["Surface"])
    
    # Set material properties
    principled.inputs["Roughness"].default_value = 1.0
    principled.inputs["Specular"].default_value = 0.0
    
    return soil_mat

def get_curve_length(curve_obj):
    """Calculate the approximate length of a curve"""
    total_length = 0
    points = curve_obj.data.splines[0].bezier_points
    num_points = len(points)
    
    # Simple approximation using straight lines between points
    for i in range(num_points):
        p1 = curve_obj.matrix_world @ points[i].co
        p2 = curve_obj.matrix_world @ points[(i + 1) % num_points].co
        segment_length = (p2 - p1).length
        total_length += segment_length
    
    return total_length

def get_point_on_curve(curve_obj, t):
    """Get a point on a curve at parameter t (0 to 1)"""
    # Sample the curve at parameter t
    spline = curve_obj.data.splines[0]
    points = spline.bezier_points
    num_points = len(points)
    
    # Determine which segment t falls in
    segment = int(t * num_points)
    segment_t = (t * num_points) % 1.0  # Parameter within segment (0-1)
    
    # Get the control points for this segment
    p0 = curve_obj.matrix_world @ points[segment].co
    p1 = curve_obj.matrix_world @ points[segment].handle_right
    p2 = curve_obj.matrix_world @ points[(segment + 1) % num_points].handle_left
    p3 = curve_obj.matrix_world @ points[(segment + 1) % num_points].co
    
    # Calculate position using cubic Bezier formula
    u = segment_t
    uu = u * u
    uuu = uu * u
    
    v = 1.0 - u
    vv = v * v
    vvv = vv * v
    
    position = vvv * p0 + 3.0 * vv * u * p1 + 3.0 * v * uu * p2 + uuu * p3
    
    # Set height based on terrain
    position.z = 0.1  # Slightly above terrain
    
    return position