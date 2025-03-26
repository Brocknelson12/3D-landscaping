import bpy
import math
import random
from mathutils import Vector

def create_garden_plants():
    """Create plants that will grow in the garden bed"""
    # Create a collection for plants
    plants_collection = bpy.data.collections.new("GardenPlants")
    bpy.context.scene.collection.children.link(plants_collection)
    
    # Create different types of plants
    plant_types = [
        {"name": "FlowerA", "count": 5, "color": (0.9, 0.2, 0.2, 1.0)},  # Red flowers
        {"name": "FlowerB", "count": 4, "color": (0.9, 0.8, 0.2, 1.0)},  # Yellow flowers
        {"name": "Herb", "count": 6, "color": (0.2, 0.7, 0.3, 1.0)}      # Green herbs
    ]
    
    plants = []
    for plant_type in plant_types:
        for i in range(plant_type["count"]):
            # Calculate position within garden bed
            angle = i * (2 * math.pi / plant_type["count"])
            radius = 2.0 + random.uniform(-0.5, 0.5)  # Vary distance from center
            x = 8 + radius * math.cos(angle)
            y = 4 + radius * math.sin(angle)
            
            plant = create_plant(x, y, 0, plant_type["name"], plant_type["color"], i)
            plants_collection.objects.link(plant)
            plants.append(plant)
    
    return plants

def create_plant(x, y, z, name, color, seed):
    """Create a single plant with stem and flower/leaves"""
    # Set random seed for consistent randomization
    random.seed(seed)
    
    # Create plant empty
    bpy.ops.object.empty_add(location=(x, y, z))
    plant_empty = bpy.context.object
    plant_empty.name = f"{name}_{seed}"
    
    # Create stem
    stem_height = random.uniform(0.3, 0.6)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02,
        depth=stem_height,
        location=(x, y, z + stem_height/2)
    )
    stem = bpy.context.object
    stem.name = f"{name}_Stem_{seed}"
    stem.parent = plant_empty
    
    # Create stem material
    stem_mat = bpy.data.materials.new(name=f"{name}_StemMaterial_{seed}")
    stem_mat.use_nodes = True
    nodes = stem_mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    principled.inputs["Base Color"].default_value = (0.1, 0.5, 0.1, 1.0)  # Green
    principled.inputs["Roughness"].default_value = 0.9
    stem.data.materials.append(stem_mat)
    
    # Slightly bend the stem for realism
    bend_modifier = stem.modifiers.new(name="Bend", type='SIMPLE_DEFORM')
    bend_modifier.deform_method = 'BEND'
    bend_modifier.deform_axis = 'X'
    bend_modifier.angle = random.uniform(-0.2, 0.2)
    
    # Create flower/leaves based on plant type
    if "Flower" in name:
        # Create flower
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.1,
            location=(x, y, z + stem_height)
        )
        flower = bpy.context.object
        flower.name = f"{name}_Flower_{seed}"
        flower.scale = (1.0, 1.0, 0.5)  # Flatten slightly
        flower.parent = plant_empty
        
        # Create flower material
        flower_mat = bpy.data.materials.new(name=f"{name}_FlowerMaterial_{seed}")
        flower_mat.use_nodes = True
        nodes = flower_mat.node_tree.nodes
        principled = nodes["Principled BSDF"]
        
        # Add slight color variation
        hue_shift = random.uniform(-0.1, 0.1)
        adjusted_color = list(color)
        adjusted_color[0] = max(0, min(1, color[0] + hue_shift))
        adjusted_color[1] = max(0, min(1, color[1] + hue_shift))
        principled.inputs["Base Color"].default_value = adjusted_color
        principled.inputs["Roughness"].default_value = 0.9
        principled.inputs["Specular"].default_value = 0.1
        flower.data.materials.append(flower_mat)
        
        # Add flower center (stamen)
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.04,
            location=(x, y, z + stem_height + 0.05)
        )
        stamen = bpy.context.object
        stamen.name = f"{name}_Stamen_{seed}"
        stamen.parent = plant_empty
        
        # Create stamen material
        stamen_mat = bpy.data.materials.new(name=f"{name}_StamenMaterial_{seed}")
        stamen_mat.use_nodes = True
        nodes = stamen_mat.node_tree.nodes
        principled = nodes["Principled BSDF"]
        principled.inputs["Base Color"].default_value = (0.9, 0.9, 0.2, 1.0)  # Yellow
        principled.inputs["Roughness"].default_value = 0.9
        stamen.data.materials.append(stamen_mat)
        
    else:  # Herbs have leaves instead of flowers
        # Create several small leaves
        leaf_count = random.randint(3, 5)
        for i in range(leaf_count):
            leaf_height = stem_height * (0.5 + i * 0.1)
            
            # Position around stem
            angle = i * (2 * math.pi / leaf_count)
            offset_x = math.cos(angle) * 0.1
            offset_y = math.sin(angle) * 0.1
            
            bpy.ops.mesh.primitive_plane_add(
                size=0.1,
                location=(x + offset_x, y + offset_y, z + leaf_height)
            )
            leaf = bpy.context.object
            leaf.name = f"{name}_Leaf_{seed}_{i}"
            
            # Rotate leaf to face outward
            leaf.rotation_euler = (random.uniform(-0.3, 0.3), 
                                  random.uniform(-0.3, 0.3), 
                                  angle)
            leaf.parent = plant_empty
            
            # Create leaf material
            leaf_mat = bpy.data.materials.new(name=f"{name}_LeafMaterial_{seed}_{i}")
            leaf_mat.use_nodes = True
            nodes = leaf_mat.node_tree.nodes
            principled = nodes["Principled BSDF"]
            
            # Slight color variation for leaves
            green_var = random.uniform(-0.1, 0.1)
            leaf_color = (0.1, 0.5 + green_var, 0.1, 1.0)
            principled.inputs["Base Color"].default_value = leaf_color
            principled.inputs["Roughness"].default_value = 0.9
            principled.inputs["Specular"].default_value = 0.1
            leaf.data.materials.append(leaf_mat)
    
    # Set initial scale to zero (for growth animation)
    plant_empty.scale = (0, 0, 0)
    
    return plant_empty

def animate_plant_growth(plants, start_frame, end_frame):
    """Animate plants growing from seeds to full size"""
    growth_start = start_frame + int((end_frame - start_frame) * 0.6)  # Start growing at 60% of animation
    
    for i, plant in enumerate(plants):
        # Stagger growth start times
        plant_start = growth_start + i * 2
        plant_end = end_frame - 5
        
        # Set initial scale (invisible)
        bpy.context.scene.frame_set(growth_start)
        plant.scale = (0, 0, 0)
        plant.keyframe_insert(data_path="scale", frame=plant_start)
        
        # Grow to full size
        bpy.context.scene.frame_set(plant_end)
        plant.scale = (1, 1, 1)
        plant.keyframe_insert(data_path="scale", frame=plant_end)
        
        # Add slight additional movement at the end
        bpy.context.scene.frame_set(end_frame)
        plant.scale = (1.02, 1.02, 1.05)  # Slightly taller at the very end
        plant.keyframe_insert(data_path="scale", frame=end_frame)
        
        # Set easing for natural growth
        fcurves = plant.animation_data.action.fcurves
        for fcurve in fcurves:
            for kfp in fcurve.keyframe_points:
                kfp.interpolation = 'ELASTIC'
                kfp.easing = 'EASE_OUT'