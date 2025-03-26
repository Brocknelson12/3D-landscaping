import bpy
import math
from utils.keyframe_utils import set_keyframe

def animate_planning_phase(robot, frame_range):
    """Animate the planning phase"""
    start_frame, end_frame = frame_range
    
    # Set initial position (from scan phase end)
    bpy.context.scene.frame_set(start_frame)
    # Robot position already set by scan phase
    
    # Move robot to start position of garden
    bpy.context.scene.frame_set(end_frame)
    robot.location = (-2, 2, 0)
    robot.rotation_euler = (0, 0, math.radians(-45))
    set_keyframe(robot, "location", end_frame)
    set_keyframe(robot, "rotation_euler", end_frame)
    
    # Return to start frame
    bpy.context.scene.frame_set(start_frame)