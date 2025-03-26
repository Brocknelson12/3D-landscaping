import bpy

def set_keyframe(obj, data_path, frame, interpolation='BEZIER'):
    """Set a keyframe for an object property with specified interpolation"""
    # Insert keyframe
    obj.keyframe_insert(data_path=data_path, frame=frame)
    
    # Set interpolation mode if animation data exists
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            if fc.data_path == data_path:
                for kf in fc.keyframe_points:
                    if kf.co.x == frame:
                        kf.interpolation = interpolation

def clear_keyframes(obj, data_path=None):
    """Clear keyframes for an object, optionally for a specific data path"""
    if obj.animation_data and obj.animation_data.action:
        fcurves = obj.animation_data.action.fcurves
        
        # If a specific data path is provided, only remove those keyframes
        if data_path:
            fcurves_to_remove = [fc for fc in fcurves if fc.data_path == data_path]
            for fc in fcurves_to_remove:
                fcurves.remove(fc)
        else:
            # Otherwise clear all keyframes
            obj.animation_data.action.fcurves.clear()