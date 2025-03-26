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
from models.robot import create_robot, enhance_robot_model
from models.garden_path import create_garden_path, create_soil_fill
from models.effects import create_scan_effect, create_printing_particles, create_heat_distortion
from models.environment import create_backyard_environment, create_sky_and_lighting, animate_day_to_night_cycle
from models.tubes_system import create_tube_system
from models.plants import create_garden_plants, animate_plant_growth
from models.text_overlays import create_process_labels

from animation.scan_phase import animate_scan_phase
from animation.planning_phase import animate_planning_phase
from animation.border_phase import animate_border_phase
from animation.filling_phase import animate_filling_phase
from animation.completion_phase import animate_completion_phase
from animation.tube_interaction import animate_robot_tube_interaction

def main():
    """Main function to set up and run the enhanced landscaping robot animation"""
    print(f"Starting Enhanced Landscaping 3D Printer Robot animation setup at {datetime.now().strftime('%H:%M:%S')}")
    
    # Clear existing scene and set up environment
    clear_scene()
    setup_environment()
    
    # Set up enhanced rendering
    setup_render_settings()
    
    # Create dynamic sky and lighting
    world, sun = create_sky_and_lighting()
    
    # Create backyard environment
    create_backyard_environment()
    
    # Create models
    print("Creating terrain...")
    terrain = create_terrain()
    create_grass(terrain)
    
    print("Creating robot...")
    robot = create_robot()
    enhance_robot_model(robot)  # Add the enhancements to the robot
    
    print("Creating garden path...")
    garden_path = create_garden_path()
    soil_fill = create_soil_fill(garden_path)
    
    print("Creating tube system...")
    tubes = create_tube_system()
    
    print("Creating visual effects...")
    scan_effect = create_scan_effect()
    heat_effect = create_heat_distortion(garden_path)
    particles = create_printing_particles(garden_path)
    
    print("Creating plants...")
    plants = create_garden_plants()
    
    print("Creating process labels...")
    labels = create_process_labels()
    
    # Set up animation phases
    print("Setting up animation phases...")
    
    # Phase 1: Scanning
    animate_scan_phase(robot, scan_effect, ANIMATION_FRAMES["scan"])
    
    # Phase 2: Planning
    animate_planning_phase(robot, ANIMATION_FRAMES["planning"])
    
    # Animate robot interaction with tubes
    animate_robot_tube_interaction(robot, tubes, ANIMATION_FRAMES)
    
    # Phase 3: Border construction
    animate_border_phase(robot, garden_path, ANIMATION_FRAMES["border"])
    
    # Phase 4: Soil filling
    animate_filling_phase(robot, soil_fill, ANIMATION_FRAMES["filling"])
    
    # Phase 5: Completion and moving
    animate_completion_phase(robot, ANIMATION_FRAMES["completion"])
    
    # Animate dynamic day-night cycle
    complete_frame_range = (ANIMATION_FRAMES["scan"][0], ANIMATION_FRAMES["completion"][1])
    animate_day_to_night_cycle(world, sun, complete_frame_range)
    
    # Animate plants growing at the end
    animate_plant_growth(plants, ANIMATION_FRAMES["completion"][0], ANIMATION_FRAMES["completion"][1])
    
    # Return to first frame
    bpy.context.scene.frame_set(1)
    
    print(f"Enhanced landscaping robot animation setup complete at {datetime.now().strftime('%H:%M:%S')}")
    print(f"Total animation length: {ANIMATION_FRAMES['completion'][1]} frames")
    print("Preview the animation with Alt+A or render with Ctrl+F12")

if __name__ == "__main__":
    main()
    
    # Save the file
    output_path = os.path.abspath('/Users/brocket12/Desktop/3D_landscaping/enhanced_landscaping_robot.blend')
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    print(f"File saved to: {output_path}")