# Landscaping 3D Printer Robot Animation Project

## Project Overview
This project creates a realistic 3D animation of an autonomous mobile landscaping robot that 3D prints garden beds. The robot scans terrain, analyzes it, and constructs garden beds by extruding different materials (concrete borders, soil filling, and precise seed placement).

## Running the Project

### Basic Animation
```bash
blender --background --python main.py
```

### Custom Garden Service
```bash
blender --background --python run_service.py -- --service garden_bed --shape rectangular --border-material clay
```

For more options, see the command-line usage documentation:
```bash
blender --background --python run_service.py -- --help
```

## Project Structure
- `main.py`: Entry point script for default animation
- `run_service.py`: Command-line service runner for custom animations
- `config.py`: Central configuration file
- `models/`: 3D model creation scripts
- `animation/`: Animation phase scripts
- `materials/`: Material definition scripts
- `utils/`: Utility functions
- `assets/`: External assets (textures, references)

## Customization
See the command-line usage instructions for details on customizing garden shapes, materials, and other parameters.