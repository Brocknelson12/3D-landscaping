import bpy
import math

# Animation frame ranges for each phase
ANIMATION_FRAMES = {
    "scan": (1, 30),      # Scanning phase
    "planning": (31, 45), # Planning phase
    "border": (46, 90),   # Border construction
    "filling": (91, 120), # Soil filling
    "completion": (121, 150) # Completion and moving
}

# Scene and rendering settings
RENDER_SETTINGS = {
    "engine": "CYCLES",
    "device": "GPU",
    "samples": 128,       # Increase for final render
    "resolution_x": 1920,
    "resolution_y": 1080,
    "fps": 30
}

# Robot dimensions and properties
ROBOT_DIMENSIONS = {
    "chassis": {
        "width": 1.5,
        "length": 1.0,
        "height": 0.3
    },
    "tracks": {
        "width": 0.2,
        "length": 1.2,
        "height": 0.15
    },
    "body": {
        "width": 1.2,
        "length": 0.8,
        "height": 0.4
    },
    "material_containers": {
        "clay": {"radius": 0.15, "height": 0.5},
        "concrete": {"radius": 0.15, "height": 0.5},
        "soil": {"radius": 0.2, "height": 0.5}
    },
    "arm": {
        "length": 0.6,
        "width": 0.2
    },
    "nozzles": {
        "clay": {"radius": 0.03},
        "concrete": {"radius": 0.03},
        "soil": {"radius": 0.04}
    }
}

# Terrain settings
TERRAIN_SETTINGS = {
    "size": 20,
    "displacement_strength": 0.3,
    "noise_scale": 2.0,
    "subdivisions": 5,
    "grass_count": 5000,
    "grass_length": 0.2
}

# Garden path settings
GARDEN_PATH_SETTINGS = {
    "bevel_depth": 0.05,
    "bevel_resolution": 4,
    "control_points": [
        {"co": (-2, 2, 0.05), "handle_left": (-2.5, 2, 0.05), "handle_right": (-1.5, 2, 0.05)},
        {"co": (2, 1, 0.05), "handle_left": (0, 1.5, 0.05), "handle_right": (3, 0.5, 0.05)},
        {"co": (1, -1.5, 0.05), "handle_left": (2, -0.5, 0.05), "handle_right": (0, -2, 0.05)},
        {"co": (-2, -1, 0.05), "handle_left": (-1, -1.5, 0.05), "handle_right": (-3, -0.5, 0.05)}
    ]
}

# Material color settings
MATERIAL_COLORS = {
    "metal_dark": (0.1, 0.1, 0.1, 1.0),
    "metal_medium": (0.3, 0.3, 0.3, 1.0),
    "metal_light": (0.6, 0.6, 0.6, 1.0),
    "glass": (0.8, 0.8, 0.8, 1.0),
    "clay": (0.65, 0.45, 0.31, 1.0),
    "concrete": (0.7, 0.7, 0.7, 1.0),
    "soil": (0.25, 0.16, 0.1, 1.0),
    "terrain": (0.34, 0.24, 0.15, 1.0),
    "grass": (0.15, 0.5, 0.15, 1.0),
    "scan_effect": (1.0, 0.1, 0.1, 1.0)
}

def setup_render_settings():
    """Apply render settings from configuration"""
    bpy.context.scene.render.engine = RENDER_SETTINGS["engine"]
    
    if RENDER_SETTINGS["engine"] == "CYCLES":
        bpy.context.scene.cycles.device = RENDER_SETTINGS["device"]
        bpy.context.scene.cycles.samples = RENDER_SETTINGS["samples"]
    
    bpy.context.scene.render.resolution_x = RENDER_SETTINGS["resolution_x"]
    bpy.context.scene.render.resolution_y = RENDER_SETTINGS["resolution_y"]
    bpy.context.scene.render.fps = RENDER_SETTINGS["fps"]
    
    # Set animation length
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = ANIMATION_FRAMES["completion"][1]