#!/usr/bin/env python3
"""
Landscaping 3D Printer Robot - Service Runner

This script provides a command-line interface to generate animations of various 
landscaping services performed by the 3D printer robot.

Usage:
    blender --background --python run_service.py -- [arguments]
"""

import bpy
import sys
import os
import argparse
import math
import json
from mathutils import Vector

# Add the project directory to the path so we can import modules
project_dir = os.path.dirname(os.path.realpath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

# Import project modules - these will be available after directory setup
from config import GARDEN_PATH_SETTINGS, MATERIAL_COLORS, ANIMATION_FRAMES, setup_render_settings
from utils.blender_utils import clear_scene, setup_environment
from models.terrain import create_terrain, create_grass
from models.robot import create_robot
from models.garden_path import create_garden_path, create_soil_fill
from models.effects import create_scan_effect
from animation.scan_phase import animate_scan_phase
from animation.planning_phase import animate_planning_phase
from animation.border_phase import animate_border_phase
from animation.filling_phase import animate_filling_phase
from animation.completion_phase import animate_completion_phase

def parse_args():
    """Parse command line arguments passed after '--'"""
    parser = argparse.ArgumentParser(description='Generate a landscaping service animation')
    
    # Service type
    parser.add_argument('--service', type=str, default='garden_bed',
                        choices=['garden_bed', 'raised_bed', 'terraced_garden', 'swale'],
                        help='Type of landscaping service to animate')
    
    # Garden shape
    parser.add_argument('--shape', type=str, default='curved',
                        choices=['curved', 'rectangular', 'circular', 'custom'],
                        help='Shape of the garden to create')
    
    # Garden size
    parser.add_argument('--size', type=float, default=1.0,
                        help='Scale factor for garden size (default=1.0)')
    
    # Materials
    parser.add_argument('--border-material', type=str, default='concrete',
                        choices=['concrete', 'clay', 'stone', 'wood'],
                        help='Material for garden borders')
    
    # Output options
    parser.add_argument('--render', action='store_true',
                        help='Render the animation after setup')
    parser.add_argument('--output-dir', type=str, default='//renders/',
                        help='Output directory for rendered frames')
    parser.add_argument('--resolution', type=str, default='1080p',
                        choices=['720p', '1080p', '1440p', '4k'],
                        help='Output resolution')
    
    # Animation options
    parser.add_argument('--duration', type=float, default=1.0,
                        help='Duration scale factor (default=1.0, faster<1.0<slower)')
    
    # Parse known args
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    
    return parser.parse_args(argv)

def get_garden_shape(shape_type, size):
    """Return control points for the specified garden shape"""
    if shape_type == 'curved':
        # Curved garden bed shape (default)
        return [
            {"co": (-2*size, 2*size, 0.05), "handle_left": (-2.5*size, 2*size, 0.05), "handle_right": (-1.5*size, 2*size, 0.05)},
            {"co": (2*size, 1*size, 0.05), "handle_left": (0*size, 1.5*size, 0.05), "handle_right": (3*size, 0.5*size, 0.05)},
            {"co": (1*size, -1.5*size, 0.05), "handle_left": (2*size, -0.5*size, 0.05), "handle_right": (0*size, -2*size, 0.05)},
            {"co": (-2*size, -1*size, 0.05), "handle_left": (-1*size, -1.5*size, 0.05), "handle_right": (-3*size, -0.5*size, 0.05)}
        ]
    elif shape_type == 'rectangular':
        # Rectangular garden bed with rounded corners
        return [
            {"co": (-2*size, 1.5*size, 0.05), "handle_left": (-2.3*size, 1.5*size, 0.05), "handle_right": (-1.7*size, 1.5*size, 0.05)},
            {"co": (2*size, 1.5*size, 0.05), "handle_left": (1.7*size, 1.5*size, 0.05), "handle_right": (2.3*size, 1.5*size, 0.05)},
            {"co": (2*size, -1.5*size, 0.05), "handle_left": (2.3*size, -1.5*size, 0.05), "handle_right": (1.7*size, -1.5*size, 0.05)},
            {"co": (-2*size, -1.5*size, 0.05), "handle_left": (-1.7*size, -1.5*size, 0.05), "handle_right": (-2.3*size, -1.5*size, 0.05)}
        ]
    elif shape_type == 'circular':
        # Circular garden bed
        points = []
        segments = 8
        radius = 2 * size
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            co_x = math.cos(angle) * radius
            co_y = math.sin(angle) * radius
            
            # Calculate handle points for smooth circle
            handle_angle = 2 * math.pi / segments / 3
            hl_x = math.cos(angle - handle_angle) * radius
            hl_y = math.sin(angle - handle_angle) * radius
            hr_x = math.cos(angle + handle_angle) * radius
            hr_y = math.sin(angle + handle_angle) * radius
            
            points.append({
                "co": (co_x, co_y, 0.05),
                "handle_left": (hl_x, hl_y, 0.05),
                "handle_right": (hr_x, hr_y, 0.05)
            })
        return points
    else:
        # Default to curved if something else is specified
        return get_garden_shape('curved', size)

def get_material_properties(material_name):
    """Get properties for specified material"""
    if material_name == 'concrete':
        return {
            "color": (0.7, 0.7, 0.7, 1.0),
            "roughness": 0.9,
            "metallic": 0.0
        }
    elif material_name == 'clay':
        return {
            "color": (0.65, 0.45, 0.31, 1.0),
            "roughness": 0.8,
            "metallic": 0.0
        }
    elif material_name == 'stone':
        return {
            "color": (0.5, 0.5, 0.5, 1.0),
            "roughness": 0.7,
            "metallic": 0.1
        }
    elif material_name == 'wood':
        return {
            "color": (0.55, 0.35, 0.15, 1.0),
            "roughness": 0.6,
            "metallic": 0.0
        }
    else:
        # Default to concrete
        return get_material_properties('concrete')

def get_resolution_settings(resolution):
    """Get resolution width and height"""
    if resolution == '720p':
        return 1280, 720
    elif resolution == '1080p':
        return 1920, 1080
    elif resolution == '1440p':
        return 2560, 1440
    elif resolution == '4k':
        return 3840, 2160
    else:
        # Default to 1080p
        return 1920, 1080

def setup_service_animation(args):
    """Set up the animation based on service parameters"""
    print(f"Setting up {args.service} service with {args.shape} shape...")
    
    # Clear existing scene and set up environment
    clear_scene()
    setup_environment()
    
    # Update render settings based on arguments
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    bpy.context.scene.cycles.samples = 128
    
    res_x, res_y = get_resolution_settings(args.resolution)
    bpy.context.scene.render.resolution_x = res_x
    bpy.context.scene.render.resolution_y = res_y
    
    # Set output path if rendering
    if args.render:
        output_path = args.output_dir
        if not os.path.isabs(output_path):
            # Make relative paths relative to blend file
            if output_path.startswith('//'):
                # Already a Blender relative path
                pass
            else:
                # Convert to Blender relative path
                output_path = '//' + output_path
        
        # Make sure path ends with separator
        if not output_path.endswith('/'):
            output_path += '/'
            
        bpy.context.scene.render.filepath = output_path
    
    # Calculate frame ranges based on duration scale
    duration_scale = args.duration
    frame_ranges = {}
    for phase, (start, end) in ANIMATION_FRAMES.items():
        phase_duration = end - start + 1
        new_duration = max(1, int(phase_duration * duration_scale))
        if phase == "scan":
            frame_ranges[phase] = (1, new_duration)
        else:
            prev_end = frame_ranges[list(ANIMATION_FRAMES.keys())[list(ANIMATION_FRAMES.keys()).index(phase) - 1]][1]
            frame_ranges[phase] = (prev_end + 1, prev_end + new_duration)
    
    # Create models
    print("Creating terrain...")
    terrain = create_terrain()
    create_grass(terrain)
    
    print("Creating robot...")
    robot = create_robot()
    
    print("Creating garden path...")
    # Update garden path settings with shape from arguments
    shape_control_points = get_garden_shape(args.shape, args.size)
    garden_path = create_garden_path(shape_control_points)
    
    # Get material properties for border
    border_material_props = get_material_properties(args.border_material)
    
    # Update border material
    for mat in bpy.data.materials:
        if "Concrete" in mat.name or "ConcretePath" in mat.name:
            if mat.use_nodes:
                bsdf = mat.node_tree.nodes.get("Principled BSDF")
                if bsdf:
                    bsdf.inputs["Base Color"].default_value = border_material_props["color"]
                    bsdf.inputs["Roughness"].default_value = border_material_props["roughness"]
                    bsdf.inputs["Metallic"].default_value = border_material_props["metallic"]
    
    soil_fill = create_soil_fill(garden_path)
    
    print("Creating visual effects...")
    scan_effect = create_scan_effect()
    
    # Set up animation phases
    print("Setting up animation phases...")
    
    # Phase 1: Scanning
    animate_scan_phase(robot, scan_effect, frame_ranges["scan"])
    
    # Phase 2: Planning
    animate_planning_phase(robot, frame_ranges["planning"])
    
    # Phase 3: Border construction
    animate_border_phase(robot, garden_path, frame_ranges["border"])
    
    # Phase 4: Soil filling
    animate_filling_phase(robot, soil_fill, frame_ranges["filling"])
    
    # Phase 5: Completion and moving
    animate_completion_phase(robot, frame_ranges["completion"])
    
    # Set end frame
    bpy.context.scene.frame_end = frame_ranges["completion"][1]
    
    # Return to first frame
    bpy.context.scene.frame_set(1)
    
    print(f"Service animation setup complete!")
    print(f"Total animation length: {frame_ranges['completion'][1]} frames")
    
    # Start render if requested
    if args.render:
        print(f"Starting render to {bpy.context.scene.render.filepath}...")
        bpy.ops.render.render(animation=True)

def main():
    """Main function"""
    # Parse arguments
    args = parse_args()
    
    # Set up and run the service animation
    setup_service_animation(args)
    
    print("Done!")

if __name__ == "__main__":
    main()