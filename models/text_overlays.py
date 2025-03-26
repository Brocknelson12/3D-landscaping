import bpy
import math

def create_process_labels():
    """Create text overlays to indicate process stages"""
    # Create collection for labels
    labels_collection = bpy.data.collections.new("ProcessLabels")
    bpy.context.scene.collection.children.link(labels_collection)
    
    # Create labels for each phase
    process_phases = [
        {"text": "1. SCANNING TERRAIN", "frame": 5},
        {"text": "2. PLANNING GARDEN LAYOUT", "frame": 35},
        {"text": "3. CREATING GARDEN BORDER", "frame": 50},
        {"text": "4. FILLING WITH SOIL", "frame": 95},
        {"text": "5. PLANTING SEEDS", "frame": 125},
        {"text": "6. GARDEN COMPLETE", "frame": 140}
    ]
    
    labels = []
    for phase in process_phases:
        label = create_text_object(phase["text"], phase["frame"])
        labels_collection.objects.link(label)
        labels.append(label)
    
    return labels

def create_text_object(text, frame):
    """Create a 3D text object that appears at a specific frame"""
    # Create text object
    bpy.ops.object.text_add(location=(4, -6, 3))
    text_obj = bpy.context.object
    text_obj.name = f"Label_{text.replace(' ', '_')}"
    
    # Set text properties
    text_obj.data.body = text
    text_obj.data.size = 0.5
    text_obj.data.extrude = 0.02
    text_obj.data.align_x = 'CENTER'
    
    # Always face camera
    constraint = text_obj.constraints.new(type='TRACK_TO')
    constraint.target = bpy.context.scene.camera
    constraint.track_axis = 'TRACK_Z'
    constraint.up_axis = 'UP_Y'
    
    # Create text material with emission for visibility
    text_mat = bpy.data.materials.new(name=f"LabelMaterial_{frame}")
    text_mat.use_nodes = True
    nodes = text_mat.node_tree.nodes
    links = text_mat.node_tree.links
    
    # Clear existing nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add nodes
    output = nodes.new(type='ShaderNodeOutputMaterial')
    emission = nodes.new(type='ShaderNodeEmission')
    
    # Position nodes
    output.location = (300, 0)
    emission.location = (100, 0)
    
    # Set node properties
    emission.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)  # White
    emission.inputs["Strength"].default_value = 2.0
    
    # Connect nodes
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    
    # Assign material
    text_obj.data.materials.append(text_mat)
    
    # Animate text appearance
    # Hide initially
    text_obj.hide_viewport = True
    text_obj.hide_render = True
    text_obj.keyframe_insert(data_path="hide_viewport", frame=1)
    text_obj.keyframe_insert(data_path="hide_render", frame=1)
    
    # Show at specified frame
    bpy.context.scene.frame_set(frame)
    text_obj.hide_viewport = False
    text_obj.hide_render = False
    text_obj.keyframe_insert(data_path="hide_viewport", frame=frame)
    text_obj.keyframe_insert(data_path="hide_render", frame=frame)
    
    # Hide after 30 frames
    bpy.context.scene.frame_set(frame + 30)
    text_obj.hide_viewport = True
    text_obj.hide_render = True
    text_obj.keyframe_insert(data_path="hide_viewport", frame=frame + 30)
    text_obj.keyframe_insert(data_path="hide_render", frame=frame + 30)
    
    # Reset frame
    bpy.context.scene.frame_set(1)
    
    return text_obj