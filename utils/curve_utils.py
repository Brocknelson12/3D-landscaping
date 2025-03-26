import bpy
import math
from mathutils import Vector

def get_point_on_curve(curve_obj, t):
    """Get a point on a curve at parameter t (0 to 1)"""
    # Make sure t is in range 0-1
    t = max(0, min(1, t))
    
    # Get the curve data
    curve = curve_obj.data
    
    # Check if the curve has any splines
    if not curve.splines:
        return Vector((0, 0, 0))
    
    # Get the first spline
    spline = curve.splines[0]
    
    # Check if it's a Bezier curve
    if spline.type != 'BEZIER':
        return Vector((0, 0, 0))
    
    # Get Bezier points
    points = spline.bezier_points
    num_points = len(points)
    
    # If only one point, return its position
    if num_points < 2:
        return points[0].co
    
    # Determine which segment t falls in
    segment = int(t * (num_points - 1 if not spline.use_cyclic_u else num_points))
    segment_t = (t * (num_points - 1 if not spline.use_cyclic_u else num_points)) % 1.0
    
    # Get the current segment's points
    p0 = points[segment]
    p1 = points[(segment + 1) % num_points]
    
    # Simple linear interpolation for demonstration
    # For accurate Bezier interpolation, we'd need to use the handle points
    pos = p0.co.lerp(p1.co, segment_t)
    
    return pos

def get_direction_on_curve(curve_obj, t):
    """Get direction vector (tangent) on a curve at parameter t (0 to 1)"""
    # Make sure t is in range 0-1
    t = max(0, min(1, t))
    
    # Get the curve data
    curve = curve_obj.data
    
    # Check if the curve has any splines
    if not curve.splines:
        return Vector((1, 0, 0))
    
    # Get the first spline
    spline = curve.splines[0]
    
    # Check if it's a Bezier curve
    if spline.type != 'BEZIER':
        return Vector((1, 0, 0))
    
    # Get Bezier points
    points = spline.bezier_points
    num_points = len(points)
    
    # Determine which segment t falls in
    segment = int(t * (num_points - 1 if not spline.use_cyclic_u else num_points))
    
    # Get the current segment's points
    p0 = points[segment]
    p1 = points[(segment + 1) % num_points]
    
    # Calculate direction (simplified, not using handles)
    direction = (p1.co - p0.co).normalized()
    
    return direction