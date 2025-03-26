import bpy
import math
from mathutils import Vector
from utils.keyframe_utils import set_keyframe

def animate_border_phase(robot, garden_path, frame_range):
    """Animate the border construction phase"""
    start_frame, end_frame = frame_range
    
    # Show garden path
    bpy.context.scene.frame_set(start_frame)
    garden_path.hide_viewport = False
    garden_path.hide_render = False
    set_keyframe(garden_path, "hide_viewport", start_frame)
    set_keyframe(garden_path, "hide_render", start_frame)
    
    # Animate the bevel factor to make it appear to be printed
    garden_path.data.bevel_factor_end = 0.0
    garden_path.data.keyframe_insert("bevel_factor_end", frame=start_frame)
    
    garden_path.data.bevel_factor_end = 1.0
    garden_path.data.keyframe_insert("bevel_factor_end", frame=end_frame)
    
    # Robot follows the path
    # Get curve points for robot movement
    steps = 9  # Number of positions along the curve
    for i in range(steps):
        t = i / (steps - 1)  # Parameter from 0 to 1
        frame = start_frame + int((end_frame - start_frame) * t)
        
        garden_path.data.bevel_factor_end = t
        bpy.context.view_layer.update()
        
        # Find the current end point of the visible part of the curve
        if i == 0:
            pos = Vector((-2, 2, 0))  # Start position
            angle = math.radians(-45)
        elif i == steps - 1:
            pos = Vector((-2, 2, 0))  # End position (closed loop)
            angle = math.radians(-45)
        else:
            # Approximate position along the curve based on current bevel factor
            bezier_points = garden_path.data.splines[0].bezier_points
            num_points = len(bezier_points)
            segment = min(num_points - 1, int(t * num_points))
            segment_t = (t * num_points) % 1.0
            
            # Simple bezier approximation
            p0 = bezier_points[segment].co
            p1 = bezier_points[(segment + 1) % num_points].co
            angle = math.atan2(p1.y - p0.y, p1.x - p0.x)
            
            pos = Vector((
                p0.x + (p1.x - p0.x) * segment_t,
                p0.y + (p1.y - p0.y) * segment_t,
                0
            ))
        
        # Offset robot to place print head on the path
        offset_distance = 0.3  # Distance from robot center to print head
        offset_x = math.cos(angle + math.radians(90)) * offset_distance
        offset_y = math.sin(angle + math.radians(90)) * offset_distance
        
        robot.location = (pos.x + offset_x, pos.y + offset_y, 0)
        robot.rotation_euler = (0, 0, angle)
        set_keyframe(robot, "location", frame)
        set_keyframe(robot, "rotation_euler", frame)
    
    # Return to start frame
    bpy.context.scene.frame_set(start_frame)