import bpy
import sys
import os
from datetime import datetime

# Add project directory to path
project_dir = os.path.dirname(os.path.realpath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

# Import project modules
from config import setup_render_settings, ANIMATION_FRAMES
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

def main():
    """Main function to set up and run the landscaping robot animation"""
    print(f"Starting Landscaping 3D Printer Robot animation setup at {datetime.now().strftime('%H:%M:%S')}")
    
    # Clear existing scene and set up environment
    clear_scene()
    setup_environment()
    setup_render_settings()
    
    # Create models
    print("Creating terrain...")
    terrain = create_terrain()
    create_grass(terrain)
    
    print("Creating robot...")
    robot = create_robot()
    
    print("Creating garden path...")
    garden_path = create_garden_path()
    soil_fill = create_soil_fill(garden_path)
    
    print("Creating visual effects...")
    scan_effect = create_scan_effect()
    
    # Set up animation phases
    print("Setting up animation phases...")
    
    # Phase 1: Scanning
    animate_scan_phase(robot, scan_effect, ANIMATION_FRAMES["scan"])
    
    # Phase 2: Planning
    animate_planning_phase(robot, ANIMATION_FRAMES["planning"])
    
    # Phase 3: Border construction
    animate_border_phase(robot, garden_path, ANIMATION_FRAMES["border"])
    
    # Phase 4: Soil filling
    animate_filling_phase(robot, soil_fill, ANIMATION_FRAMES["filling"])
    
    # Phase 5: Completion and moving
    animate_completion_phase(robot, ANIMATION_FRAMES["completion"])
    
    # Return to first frame
    bpy.context.scene.frame_set(1)
    
    print(f"Landscaping robot animation setup complete at {datetime.now().strftime('%H:%M:%S')}")
    print(f"Total animation length: {ANIMATION_FRAMES['completion'][1]} frames")
    print("Preview the animation with Alt+A or render with Ctrl+F12")

if __name__ == "__main__":
    main()
    bpy.ops.wm.save_as_mainfile(filepath="/Users/brocket12/Desktop/3D_landscaping/landscaping_robot.blend")
    print(f"File saved to: {os.path.abspath('l/Users/brocket12/Desktop/3D_landscaping/andscaping_robot.blend')}")