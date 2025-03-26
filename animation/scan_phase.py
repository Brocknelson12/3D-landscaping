import bpy
import math
from utils.keyframe_utils import set_keyframe

def animate_scan_phase(robot, scan_effect, frame_range):
    """Animate the scanning phase"""
    start_frame, end_frame = frame_range
    mid_frame = start_frame + (end_frame - start_frame) // 2
    
    # Get scanner head object
    scanner_head = None
    for obj in bpy.data.objects:
        if obj.name == "ScannerHead":
            scanner_head = obj
            break
    
    # Set initial robot position
    bpy.context.scene.frame_set(start_frame)
    
    robot.location = (-3, 0, 0)
    set_keyframe(robot, "location", start_frame)
    
    # Show scan effect
    scan_effect.hide_viewport = False
    scan_effect.hide_render = False
    set_keyframe(scan_effect, "hide_viewport", start_frame)
    set_keyframe(scan_effect, "hide_render", start_frame)
    
    # Scanner head rotation
    if scanner_head:
        for i in range(start_frame, end_frame + 1, 5):
            frame_progress = (i - start_frame) / (end_frame - start_frame)
            scanner_head.rotation_euler = (0, 0, math.radians(frame_progress * 360))
            set_keyframe(scanner_head, "rotation_euler", i)
    
    # Robot moves during scanning
    bpy.context.scene.frame_set(mid_frame)
    robot.location = (-1, 1, 0)
    set_keyframe(robot, "location", mid_frame)
    
    bpy.context.scene.frame_set(end_frame)
    robot.location = (1, 0, 0)
    set_keyframe(robot, "location", end_frame)
    
    # Hide scan effect at end of scanning
    scan_effect.hide_viewport = True
    scan_effect.hide_render = True
    set_keyframe(scan_effect, "hide_viewport", end_frame)
    set_keyframe(scan_effect, "hide_render", end_frame)
    
    # Return to start frame
    bpy.context.scene.frame_set(start_frame)