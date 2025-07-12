#!/usr/bin/env python3

import os
import sys
import re
import json
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from PIL import Image as PILImage

def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent / "config.json"
    default_config = {
        "student_name": "Your Name Here",
        "course_code": "CIS44F",
        "school": "De Anza College"
    }
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            # Merge with defaults to handle missing keys
            return {**default_config, **config}
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: Could not load config.json. Using default values.")
        print(f"Run the installation script or create {config_path} to customize student information.")
        return default_config

def get_lab_description(lab_dir):
    """Extract lab description from directory name"""
    lab_name = Path(lab_dir).name
    # Extract lab number/identifier
    match = re.match(r'Lab(\w+)', lab_name)
    if match:
        lab_num = match.group(1)
        return f"Lab {lab_num}"
    return lab_name

def get_task_folders(lab_dir):
    """Get all task folders in chronological order"""
    lab_path = Path(lab_dir)
    task_folders = []
    
    for item in lab_path.iterdir():
        if item.is_dir() and item.name.lower().startswith('task'):
            # Extract task number for sorting
            match = re.search(r'task\s*(\d+)', item.name.lower())
            if match:
                task_num = int(match.group(1))
                task_folders.append((task_num, item))
    
    # Sort by task number
    task_folders.sort(key=lambda x: x[0])
    return [folder for _, folder in task_folders]

def get_screenshots(task_dir):
    """Get all screenshots from a task directory, sorted by filename"""
    screenshots = []
    for file_path in task_dir.glob('*.png'):
        screenshots.append(file_path)
    for file_path in task_dir.glob('*.jpg'):
        screenshots.append(file_path)
    for file_path in task_dir.glob('*.jpeg'):
        screenshots.append(file_path)
    
    # Sort by filename (which includes timestamp)
    screenshots.sort(key=lambda x: x.name)
    return screenshots

def resize_image(image_path, max_width=6*inch, max_height=4*inch):
    """Resize image to fit within specified dimensions while maintaining aspect ratio"""
    with PILImage.open(image_path) as img:
        # Get current dimensions
        width, height = img.size
        
        # Calculate scaling factor
        width_ratio = max_width / width
        height_ratio = max_height / height
        scale_factor = min(width_ratio, height_ratio, 1.0)  # Don't upscale
        
        new_width = width * scale_factor
        new_height = height * scale_factor
        
        return new_width, new_height

def create_lab_report(lab_dir):
    """Generate PDF report for a lab directory"""
    lab_path = Path(lab_dir)
    
    if not lab_path.exists():
        print(f"Error: Lab directory '{lab_dir}' does not exist.")
        return False
    
    # Load configuration
    config = load_config()
    
    # Output PDF path
    lab_description = get_lab_description(lab_dir)
    match = re.search(r'Lab(\w+)', lab_path.name)
    if match:
        lab_num = match.group(1).lower()
        output_file = lab_path / f"lab{lab_num}.pdf"
    else:
        # If no match, use the directory name as-is but ensure it ends with .pdf
        base_name = lab_path.name.lower()
        if not base_name.endswith('.pdf'):
            base_name += '.pdf'
        output_file = lab_path / base_name
    
    # Create PDF document
    doc = SimpleDocTemplate(str(output_file), pagesize=letter,
                          rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    task_header_style = ParagraphStyle(
        'TaskHeader',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Story (content) list
    story = []
    
    # Add header
    story.append(Paragraph(config["student_name"], title_style))
    story.append(Paragraph(f"{config['course_code']} - {lab_description}", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Get task folders
    task_folders = get_task_folders(lab_dir)
    
    if not task_folders:
        print(f"Warning: No task folders found in '{lab_dir}'")
        return False
    
    # Process each task
    for task_folder in task_folders:
        # Extract task number
        match = re.search(r'task\s*(\d+)', task_folder.name.lower())
        task_num = match.group(1) if match else "?"
        
        # Add task header
        story.append(Paragraph(f"Task {task_num}", task_header_style))
        story.append(Spacer(1, 12))
        
        # Get screenshots for this task
        screenshots = get_screenshots(task_folder)
        
        if not screenshots:
            story.append(Paragraph("No screenshots found for this task.", styles['Normal']))
            story.append(Spacer(1, 12))
            continue
        
        # Add screenshots
        for screenshot in screenshots:
            try:
                # Resize image
                width, height = resize_image(screenshot)
                img = Image(str(screenshot), width=width, height=height)
                story.append(img)
                story.append(Spacer(1, 12))
            except Exception as e:
                print(f"Warning: Could not process image {screenshot}: {e}")
        
        # Add spacing between tasks
        story.append(Spacer(1, 20))
    
    # Build PDF
    try:
        doc.build(story)
        print(f"Successfully generated: {output_file}")
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

def find_lab_directory(input_name):
    """Find the actual lab directory based on flexible input matching"""
    current_dir = Path.cwd()
    
    # If it's an absolute path that exists, use it
    if os.path.isabs(input_name) and Path(input_name).exists():
        return input_name
    
    # Look for directories that match the input
    possible_matches = []
    
    for item in current_dir.iterdir():
        if item.is_dir():
            item_name = item.name.lower()
            input_lower = input_name.lower()
            
            # Exact match (case-insensitive)
            if item_name == input_lower:
                return str(item)
            
            # Check if input is a lab number/identifier
            lab_match = re.search(r'(\d+[a-z]*)', input_lower)
            if lab_match:
                lab_id = lab_match.group(1)
                # Match Lab{number}, lab{number}, Lab{number}a, etc.
                if re.match(rf'lab{re.escape(lab_id)}$', item_name):
                    if str(item) not in possible_matches:
                        possible_matches.append(str(item))
            
            # Partial matching - if input contains part of directory name
            elif input_lower in item_name or item_name in input_lower:
                if str(item) not in possible_matches:
                    possible_matches.append(str(item))
    
    if len(possible_matches) == 1:
        return possible_matches[0]
    elif len(possible_matches) > 1:
        print(f"Multiple directories match '{input_name}':")
        for match in possible_matches:
            print(f"  - {Path(match).name}")
        print("Please be more specific.")
        return None
    else:
        print(f"No lab directory found matching '{input_name}'")
        print("Available lab directories:")
        lab_dirs = [d.name for d in current_dir.iterdir() 
                   if d.is_dir() and re.match(r'lab\w*', d.name.lower())]
        if lab_dirs:
            for lab_dir in sorted(lab_dirs):
                print(f"  - {lab_dir}")
        else:
            print("  No lab directories found")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 generate_lab_report.py <lab_directory>")
        print("Example: python3 generate_lab_report.py Lab1")
        print("         python3 generate_lab_report.py lab1")
        print("         python3 generate_lab_report.py 1")
        print("         python3 generate_lab_report.py 7")
        sys.exit(1)
    
    input_name = sys.argv[1]
    
    # Find the actual lab directory
    lab_directory = find_lab_directory(input_name)
    if not lab_directory:
        sys.exit(1)
    
    success = create_lab_report(lab_directory)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()