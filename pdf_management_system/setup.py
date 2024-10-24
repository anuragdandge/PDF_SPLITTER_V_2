import os
from pathlib import Path
import json

def create_project_structure(base_path):
    """Create the project directory structure"""
    # Create base directory if it doesn't exist
    base_dir = Path(base_path)
    base_dir.mkdir(exist_ok=True)
    
    # Create required subdirectories
    directories = [
        'input',          # For input PDF files
        'processed',      # For processed files
        'duplicates',     # For duplicate files
        'logs',          # For log files
        'config'         # For configuration files
    ]
    
    for dir_name in directories:
        (base_dir / dir_name).mkdir(exist_ok=True)
    
    # Create default configuration file
    config = {
        'coordinates': {
            'company_id': {'x1': 100, 'y1': 100, 'x2': 300, 'y2': 150},
            'docket_id': {'x1': 400, 'y1': 100, 'x2': 600, 'y2': 150}
        },
        'preprocessing_methods': ['threshold', 'denoise', 'sharpen'],
        'reference_page_size': {'width': 2480, 'height': 3508}  # A4 at 300 DPI
    }
    
    config_path = base_dir / 'config' / 'ocr_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"Created project structure at: {base_dir}")
    print("Directory structure:")
    for path in sorted(base_dir.rglob('*')):
        depth = len(path.relative_to(base_dir).parts)
        print(f"{'  ' * depth}├── {path.name}")

if __name__ == "__main__":
    # Change this to your desired project location
    BASE_PATH = "pdf_management_system"
    create_project_structure(BASE_PATH)