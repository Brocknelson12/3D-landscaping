# Landscaping 3D Printer Robot - Command-line Usage

## Overview

The "Landscaping 3D Printer Robot" animation system can be run from the command line to easily generate animations of different garden layouts and services. This document explains how to use the command-line interface to create custom landscaping service animations.

## Basic Usage

The animation generator is run through Blender's command-line interface. The basic command structure is:

```bash
blender --background --python run_service.py -- [service_arguments]
```

Where:
- `--background` runs Blender without the GUI (headless mode)
- `--python run_service.py` specifies the Python script to execute
- `--` separates Blender's arguments from the script's arguments
- `[service_arguments]` are the arguments for configuring the animation

## Example Commands

### Basic Garden Bed Creation

To create a default curved garden bed animation:

```bash
blender --background --python run_service.py -- --service garden_bed
```

### Customized Garden Animation

Create a larger rectangular garden bed with clay borders and render the animation:

```bash
blender --background --python run_service.py -- --service garden_bed --shape rectangular --size 1.5 --border-material clay --render --output-dir //my_renders/garden1/
```

### High-Resolution Circular Garden

Create a circular garden bed and render it at 4K resolution with slower animation:

```bash
blender --background --python run_service.py -- --service garden_bed --shape circular --resolution 4k --duration 1.5 --render
```

## Available Options

### Service Types

- `--service garden_bed` - Standard garden bed (default)
- `--service raised_bed` - Elevated garden bed
- `--service terraced_garden` - Multi-level garden
- `--service swale` - Water management landscaping

### Garden Shapes

- `--shape curved` - Organic curved shape (default)
- `--shape rectangular` - Rectangular with rounded corners
- `--shape circular` - Circular garden bed

### Size and Scale

- `--size 1.0` - Scale factor for garden size (default=1.0)
- `--duration 1.0` - Animation speed factor (smaller values = faster)

### Materials

- `--border-material concrete` - Concrete borders (default)
- `--border-material clay` - Clay borders
- `--border-material stone` - Stone borders
- `--border-material wood` - Wooden borders

### Rendering Options

- `--render` - Render the animation after setup
- `--output-dir //renders/` - Output directory for rendered frames (use // for relative paths)
- `--resolution 1080p` - Output resolution (720p, 1080p, 1440p, 4k)

## Integration with Other Tools

### Batch Processing

You can use shell scripts to batch process multiple configurations:

```bash
#!/bin/bash
# Generate multiple garden designs

# Circular garden
blender --background --python run_service.py -- --service garden_bed --shape circular --render --output-dir //renders/circular/

# Rectangular garden
blender --background --python run_service.py -- --service garden_bed --shape rectangular --render --output-dir //renders/rectangular/

# Curved garden
blender --background --python run_service.py -- --service garden_bed --shape curved --render --output-dir //renders/curved/
```

### Rendering Farm Integration

For integration with render farms, you can use the command-line interface with frame range specifications:

```bash
# Render specific frame range on node 1
blender --background --python run_service.py -- --service garden_bed --render -- -s 1 -e 50 -o //renders/garden_node1/

# Render next frame range on node 2
blender --background --python run_service.py -- --service garden_bed --render -- -s 51 -e 100 -o //renders/garden_node2/
```

## Troubleshooting

### Common Issues:

1. **Missing modules error**: Ensure all project files are in the correct directory structure
2. **GPU not found**: Add `--cycles-device CPU` to the Blender arguments if no GPU is available
3. **File path errors**: Use double slashes for Blender relative paths: `//renders/`

### Getting Help

Run with `--help` to see all available options:

```bash
blender --background --python run_service.py -- --help
```