#!/bin/bash
# Launcher script for the Landscaping 3D Printer Robot Animation

# Set text colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Display banner
echo -e "${GREEN}=======================================================${NC}"
echo -e "${GREEN}   Landscaping 3D Printer Robot Animation Launcher    ${NC}"
echo -e "${GREEN}=======================================================${NC}"

# Function to validate Blender installation
check_blender() {
    if ! command -v blender &> /dev/null; then
        echo -e "${YELLOW}Blender not found in PATH. Please make sure Blender is installed.${NC}"
        echo -e "You can download Blender from: https://www.blender.org/"
        exit 1
    fi
}

# Function to filter out the BlenderGPT addon error
run_blender_and_filter() {
    # Run the command and filter out the specific error message
    "$@" 2> >(grep -v "register_class.*GPT4_OT_ShowCode" >&2)
}

# Display menu
display_menu() {
    echo -e "\n${BLUE}Select animation option:${NC}"
    echo -e "  1) Run standard animation (main.py)"
    echo -e "  2) Create curved garden bed"
    echo -e "  3) Create rectangular garden bed"
    echo -e "  4) Create circular garden bed"
    echo -e "  5) Custom garden settings"
    echo -e "  0) Exit"
    echo -n -e "\nEnter your choice [0-5]: "
    read choice
}

# Run standard animation
run_standard() {
    echo -e "\n${BLUE}Running standard animation...${NC}"
    run_blender_and_filter /Applications/Blender.app/Contents/MacOS/Blender --background --python main.py
}

# Run with specific garden shape
run_garden_shape() {
    local shape=$1
    local material=$2
    local size=$3
    
    echo -e "\n${BLUE}Creating $shape garden bed with $material borders...${NC}"
    run_blender_and_filter /Applications/Blender.app/Contents/MacOS/Blender --background --python run_service.py -- --service garden_bed --shape $shape --border-material $material --size $size
}

# Get material type
get_material() {
    echo -e "\n${BLUE}Select border material:${NC}"
    echo -e "  1) Concrete (default)"
    echo -e "  2) Clay"
    echo -e "  3) Stone"
    echo -e "  4) Wood"
    echo -n -e "\nEnter your choice [1-4]: "
    read material_choice
    
    case $material_choice in
        1) echo "concrete" ;;
        2) echo "clay" ;;
        3) echo "stone" ;;
        4) echo "wood" ;;
        *) echo "concrete" ;; # Default
    esac
}

# Get size
get_size() {
    echo -n -e "\n${BLUE}Enter garden size factor (default: 1.0): ${NC}"
    read size_input
    
    # Set default if empty
    if [[ -z "$size_input" ]]; then
        size_input="1.0"
    fi
    
    # Validate if it's a number
    if [[ "$size_input" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        echo "$size_input"
    else
        echo "1.0" # Default if not a valid number
    fi
}

# Custom garden settings
custom_garden() {
    # Get shape
    echo -e "\n${BLUE}Select garden shape:${NC}"
    echo -e "  1) Curved (default)"
    echo -e "  2) Rectangular"
    echo -e "  3) Circular"
    echo -n -e "\nEnter your choice [1-3]: "
    read shape_choice
    
    case $shape_choice in
        1) shape="curved" ;;
        2) shape="rectangular" ;;
        3) shape="circular" ;;
        *) shape="curved" ;; # Default
    esac
    
    # Get material
    material=$(get_material)
    
    # Get size
    size=$(get_size)
    
    # Get resolution
    echo -e "\n${BLUE}Select resolution:${NC}"
    echo -e "  1) 720p"
    echo -e "  2) 1080p (default)"
    echo -e "  3) 1440p"
    echo -e "  4) 4K"
    echo -n -e "\nEnter your choice [1-4]: "
    read res_choice
    
    case $res_choice in
        1) resolution="720p" ;;
        2) resolution="1080p" ;;
        3) resolution="1440p" ;;
        4) resolution="4k" ;;
        *) resolution="1080p" ;; # Default
    esac
    
    # Render option
    echo -n -e "\n${BLUE}Render the animation? (y/n, default: n): ${NC}"
    read render_choice
    
    if [[ "$render_choice" == "y" || "$render_choice" == "Y" ]]; then
        render="--render"
        
        # Output directory
        echo -n -e "\n${BLUE}Enter output directory (default: renders): ${NC}"
        read output_dir
        
        if [[ -z "$output_dir" ]]; then
            output_dir="renders"
        fi
        
        output_arg="--output-dir //$output_dir/"
    else
        render=""
        output_arg=""
    fi
    
    # Animation duration
    echo -n -e "\n${BLUE}Enter animation duration factor (default: 1.0): ${NC}"
    read duration_input
    
    if [[ -z "$duration_input" || ! "$duration_input" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
        duration_arg="--duration 1.0"
    else
        duration_arg="--duration $duration_input"
    fi
    
    # Run with custom settings
    echo -e "\n${BLUE}Running with custom settings...${NC}"
    echo -e "Shape: $shape"
    echo -e "Material: $material" 
    echo -e "Size: $size"
    echo -e "Resolution: $resolution"
    
    if [[ "$render" == "--render" ]]; then
        echo -e "Rendering: Yes"
        echo -e "Output directory: //$output_dir/"
    else
        echo -e "Rendering: No"
    fi
    
    echo -e "Duration factor: ${duration_arg#--duration }"
    
    echo -e "\n${YELLOW}Command:${NC} blender --background --python run_service.py -- --service garden_bed --shape $shape --border-material $material --size $size --resolution $resolution $render $output_arg $duration_arg"
    
    # Run the command
    run_blender_and_filter /Applications/Blender.app/Contents/MacOS/Blender --background --python run_service.py -- --service garden_bed --shape $shape --border-material $material --size $size --resolution $resolution $render $output_arg $duration_arg
}

# Check if Blender is installed
# check_blender

# Main loop
while true; do
    display_menu
    
    case $choice in
        0)
            echo -e "\n${GREEN}Exiting...${NC}"
            exit 0
            ;;
        1)
            run_standard
            ;;
        2)
            material=$(get_material)
            size=$(get_size)
            run_garden_shape "curved" "$material" "$size"
            ;;
        3)
            material=$(get_material)
            size=$(get_size)
            run_garden_shape "rectangular" "$material" "$size"
            ;;
        4)
            material=$(get_material)
            size=$(get_size)
            run_garden_shape "circular" "$material" "$size"
            ;;
        5)
            custom_garden
            ;;
        *)
            echo -e "\n${YELLOW}Invalid choice. Please try again.${NC}"
            ;;
    esac
    
    # Ask to continue
    echo -n -e "\n${BLUE}Run another animation? (y/n, default: y): ${NC}"
    read continue_choice
    
    if [[ "$continue_choice" == "n" || "$continue_choice" == "N" ]]; then
        echo -e "\n${GREEN}Exiting...${NC}"
        exit 0
    fi
done