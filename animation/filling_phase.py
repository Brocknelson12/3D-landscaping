import bpy
import math
from utils.keyframe_utils import set_keyframe

def animate_filling_phase(robot, soil_fill, frame_range):
    """Animate the soil filling phase"""
    start_frame, end_frame = frame_range
    mid_frame = start_frame + (end_frame - start_frame) // 2
    
    # Show soil fill
    bpy.context.scene.frame_set(start_frame)
    soil_fill.hide_viewport = False
    soil_fill.hide_render = False
    set_keyframe(soil_fill, "hide_viewport", start_frame)
    set_keyframe(soil_fill, "hide_render", start_frame)
    
    # Animate the bevel factor to make soil appear to fill in
    soil_fill.data.bevel_factor_end = 0.0
    soil_fill.data.keyframe_insert("bevel_factor_end", frame=start_frame)
    
    soil_fill.data.bevel_factor_end = 1.0
    soil_fill.data.keyframe_insert("bevel_factor_end", frame=end_frame)
    
    # Robot moves to center of garden
    bpy.context.scene.frame_set(mid_frame)
    robot.location = (0, 0, 0)
    robot.rotation_euler = (0, 0, math.radians(45))
    set_keyframe(robot, "location", mid_frame)
    set_keyframe(robot, "rotation_euler", mid_frame)
    
    # Return to start frame
    bpy.context.scene.frame_set(start_frame)