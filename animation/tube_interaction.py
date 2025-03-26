import bpy
import math
from mathutils import Vector
from utils.keyframe_utils import set_keyframe

def animate_robot_tube_interaction(robot, tubes, frame_ranges):
    """Animate the robot interacting with the tubes"""
    # Define the sequence of tube interactions
    tube_sequence = [
        {"tube": "ClayTube", "phase": "border", "description": "Clay border printing"},
        {"tube": "SoilTube", "phase": "filling", "description": "Soil filling"},
        {"tube": "SeedTube", "phase": "seeding", "description": "Seed placement"}
    ]
    
    # Find the tubes by name
    tube_objects = {}
    for tube_name in [seq["tube"] for seq in tube_sequence]:
        for tube in tubes:
            if tube.name == tube_name:
                tube_objects[tube_name] = tube
                break
    
    # Animate each tube interaction
    for i, sequence in enumerate(tube_sequence):
        tube_name = sequence["tube"]
        phase = sequence["phase"]
        
        if tube_name not in tube_objects:
            continue
            
        tube = tube_objects[tube_name]
        
        # Determine frames for interaction
        if phase == "border":
            interaction_start = frame_ranges["planning"][1] - 10
            interaction_end = frame_ranges["border"][0] + 5
        elif phase == "filling":
            interaction_start = frame_ranges["border"][1] - 10
            interaction_end = frame_ranges["filling"][0] + 5
        elif phase == "seeding":
            interaction_start = frame_ranges["filling"][1] - 10
            interaction_end = frame_ranges["completion"][0] + 5
        else:
            continue
            
        # Animate robot moving to tube
        # First approach the tube
        bpy.context.scene.frame_set(interaction_start)
        
        # Move robot to tube position
        tube_pos = tube.location.copy()
        robot_pos = Vector((tube_pos.x, tube_pos.y - 2, 0))  # Position in front of tube
        
        robot.location = robot_pos
        robot.rotation_euler = (0, 0, math.radians(0))  # Face tube
        
        set_keyframe(robot, "location", interaction_start)
        set_keyframe(robot, "rotation_euler", interaction_start)
        
        # Animate removing the plug
        animate_plug_removal(tube, robot, interaction_start, 5)
        
        # Animate tube content movement after plug removal
        animate_tube_contents_flow(tube, interaction_start + 5, 20)
        
        # Animate robot taking tube to the garden area
        bpy.context.scene.frame_set(interaction_start + 25)
        
        # Move to garden position
        if phase == "border":
            target_pos = Vector((8, 6, 0))  # Start of garden outline
        elif phase == "filling":
            target_pos = Vector((8, 4, 0))  # Center of garden
        else:  # seeding
            target_pos = Vector((7, 3, 0))  # Slightly offset center for seeds
            
        robot.location = target_pos
        set_keyframe(robot, "location", interaction_start + 25)
        
        # At the end of each phase, return the tube
        bpy.context.scene.frame_set(interaction_end)
        
        # Move back to tube position
        robot.location = robot_pos
        set_keyframe(robot, "location", interaction_end)
        
        # Animate reinserting the plug
        animate_plug_insertion(tube, robot, interaction_end, 5)

def animate_plug_removal(tube, robot, start_frame, duration):
    """Animate robot removing the plug from the tube"""
    # Find the plug object
    plug = None
    for child in tube.children:
        if "Plug" in child.name:
            plug = child
            break
    
    if not plug:
        return
        
    # Original plug position and rotation
    orig_pos = plug.location.copy()
    orig_rot = plug.rotation_euler.copy()
    
    # Animate plug being removed
    for i in range(duration + 1):
        frame = start_frame + i
        t = i / duration  # Normalize time 0-1
        
        # Move plug downward and slightly toward robot
        new_pos = Vector((
            orig_pos.x,
            orig_pos.y - t * 0.5,  # Move along tube axis
            orig_pos.z
        ))
        
        # Set plug position
        bpy.context.scene.frame_set(frame)
        plug.location = new_pos
        plug.keyframe_insert(data_path="location", frame=frame)
        
    # Make plug a child of robot briefly to move with it
    bpy.context.scene.frame_set(start_frame + duration)
    orig_parent = plug.parent
    plug.parent = robot
    
    # Store this relationship change with a keyframe
    # This is a workaround since parenting doesn't directly support keyframes
    # We'll use a custom property to track this
    if not robot.get('custom_plug_parent'):
        robot['custom_plug_parent'] = True
        robot.id_properties_ui('custom_plug_parent').update(min=0, max=1)
    
    robot['custom_plug_parent'] = 1
    robot.keyframe_insert(data_path='["custom_plug_parent"]', frame=start_frame + duration)

def animate_plug_insertion(tube, robot, start_frame, duration):
    """Animate robot inserting the plug back into the tube"""
    # Find the plug object
    plug = None
    for child in robot.children:
        if "Plug" in child.name and tube.name in child.name:
            plug = child
            break
    
    if not plug:
        return
        
    # Get the original tube to reparent to
    orig_parent = None
    for obj in bpy.data.objects:
        if obj.name == tube.name:
            orig_parent = obj
            break
            
    if not orig_parent:
        return
        
    # Animate plug being inserted
    for i in range(duration + 1):
        frame = start_frame + i
        t = i / duration  # Normalize time 0-1
        
        # Calculate position moving back to original
        # We need to transform to the correct space
        world_pos = robot.matrix_world @ plug.location
        target_local_pos = orig_parent.matrix_world.inverted() @ world_pos
        
        # Move plug toward original position
        new_local_pos = Vector((
            target_local_pos.x,
            target_local_pos.y + t * 0.5,  # Move along tube axis
            target_local_pos.z
        ))
        
        # Set plug position
        bpy.context.scene.frame_set(frame)
        plug.location = robot.matrix_world.inverted() @ (orig_parent.matrix_world @ new_local_pos)
        plug.keyframe_insert(data_path="location", frame=frame)
        
    # Return plug as child of original tube
    bpy.context.scene.frame_set(start_frame + duration)
    plug.parent = orig_parent
    
    # Update the custom property
    if not robot.get('custom_plug_parent'):
        robot['custom_plug_parent'] = True
        robot.id_properties_ui('custom_plug_parent').update(min=0, max=1)
    
    robot['custom_plug_parent'] = 0
    robot.keyframe_insert(data_path='["custom_plug_parent"]', frame=start_frame + duration)

def animate_tube_contents_flow(tube, start_frame, duration):
    """Animate the contents of the tube flowing after plug removal"""
    # Find the contents object
    contents = None
    for child in tube.children:
        if "Contents" in child.name:
            contents = child
            break
    
    if not contents:
        return
        
    # Original scale
    orig_scale = contents.scale.copy()
    
    # Animate contents flowing out (shrinking)
    for i in range(duration + 1):
        frame = start_frame + i
        t = i / duration  # Normalize time 0-1
        
        # Scale down contents to simulate flow
        new_scale = Vector((
            orig_scale.x,
            orig_scale.y * (1 - t * 0.4),  # Shrink along length
            orig_scale.z
        ))
        
        # Set contents scale
        bpy.context.scene.frame_set(frame)
        contents.scale = new_scale
        contents.keyframe_insert(data_path="scale", frame=frame)
        
    # Animate valve turning to control flow
    valve = None
    for child in tube.children:
        if "Valve" in child.name:
            valve = child
            break
    
    if valve:
        # Original rotation
        orig_rot = valve.rotation_euler.copy()
        
        # Animate valve turning
        bpy.context.scene.frame_set(start_frame)
        valve.rotation_euler = orig_rot
        valve.keyframe_insert(data_path="rotation_euler", frame=start_frame)
        
        # Turn valve
        bpy.context.scene.frame_set(start_frame + 5)
        valve.rotation_euler = (orig_rot.x, orig_rot.y, orig_rot.z + math.radians(90))
        valve.keyframe_insert(data_path="rotation_euler", frame=start_frame + 5)
        
        # Turn back
        bpy.context.scene.frame_set(start_frame + duration - 5)
        valve.rotation_euler = (orig_rot.x, orig_rot.y, orig_rot.z + math.radians(90))
        valve.keyframe_insert(data_path="rotation_euler", frame=start_frame + duration - 5)
        
        bpy.context.scene.frame_set(start_frame + duration)
        valve.rotation_euler = orig_rot
        valve.keyframe_insert(data_path="rotation_euler", frame=start_frame + duration)