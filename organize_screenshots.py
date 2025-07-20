#!/usr/bin/env python3
"""
Screenshot Organization Script
Automatically organizes screenshots into appropriate lab/task directories
"""

import os
import json
import shutil
import argparse
import platform
import re
from pathlib import Path


class ScreenshotOrganizer:
    def __init__(self):
        self.config_file = Path("screenshot_config.json")
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_config(self, config):
        """Save configuration to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        self.config = config
    
    def get_default_screenshot_dir(self):
        """Get platform-specific default screenshot directory"""
        system = platform.system().lower()
        if system == "darwin":  # macOS
            return str(Path.home() / "Desktop")
        elif system == "windows":
            return str(Path.home() / "Desktop")
        else:  # Linux and others
            return str(Path.home() / "Desktop")
    
    def configure_screenshot_directory(self, reconfigure=False):
        """Configure screenshot source directory"""
        if not reconfigure and "screenshot_source_directory" in self.config:
            return self.config["screenshot_source_directory"]
        
        default_dir = self.get_default_screenshot_dir()
        print(f"\n{'Reconfiguring' if reconfigure else 'Configuring'} screenshot source directory...")
        print(f"Default directory for your platform: {default_dir}")
        
        choice = input(f"Use default directory? (y/n): ").strip().lower()
        
        if choice == 'y':
            screenshot_dir = default_dir
        else:
            while True:
                screenshot_dir = input("Enter screenshot directory path: ").strip()
                if screenshot_dir and Path(screenshot_dir).exists():
                    break
                print("Directory does not exist. Please enter a valid path.")
        
        config = self.config.copy()
        config["screenshot_source_directory"] = screenshot_dir
        self.save_config(config)
        
        print(f"Configuration {'updated' if reconfigure else 'saved'}: {self.config_file}")
        print(f"Screenshot source: {screenshot_dir}")
        
        return screenshot_dir
    
    def detect_screenshots(self, directory):
        """Detect screenshots in directory based on naming conventions"""
        screenshot_patterns = [
            # macOS patterns - support both 12-hour (AM/PM) and 24-hour formats
            r"^Screen Shot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2} (AM|PM)\.(png|jpg|jpeg)$",  # macOS traditional 12-hour
            r"^Screen Shot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2}\.(png|jpg|jpeg)$",  # macOS traditional 24-hour
            r"^Screenshot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2} (AM|PM)\.(png|jpg|jpeg)$",  # macOS modern 12-hour
            r"^Screenshot \d{4}-\d{2}-\d{2} at \d{1,2}\.\d{2}\.\d{2}\.(png|jpg|jpeg)$",  # macOS modern 24-hour
            
            # Windows patterns - support different locale date separators
            r"^Screenshot \d{4}[-./]\d{2}[-./]\d{2} \d{6}\.(png|jpg|jpeg)$",  # Windows various locales
            r"^Annotation \d{4}[-./]\d{2}[-./]\d{2} \d{6}\.(png|jpg|jpeg)$",  # Windows Snip & Sketch various locales
            
            # Linux GNOME patterns - support various time separators and formats
            r"^Screenshot from \d{4}-\d{2}-\d{2} \d{2}[-:]\d{2}[-:]\d{2}\.(png|jpg|jpeg)$",  # Linux GNOME
            r"^Screenshot from \d{4}[-./]\d{2}[-./]\d{2} \d{2}[-:]\d{2}[-:]\d{2}\.(png|jpg|jpeg)$",  # Linux GNOME locale variants
        ]
        
        screenshots = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            return screenshots
        
        for file_path in directory_path.iterdir():
            if file_path.is_file():
                filename = file_path.name
                for pattern in screenshot_patterns:
                    if re.match(pattern, filename, re.IGNORECASE):
                        screenshots.append(file_path)
                        break
        
        # Sort by filename (timestamp) for chronological order
        return sorted(screenshots, key=lambda x: x.name)
    
    def find_lab_directory(self, lab_input):
        """Find lab directory with flexible matching"""
        lab_input = lab_input.strip()
        
        # Try exact match first
        for path in Path(".").iterdir():
            if path.is_dir() and path.name.lower() == f"lab{lab_input.lower()}":
                return path
        
        # Try with "Lab" prefix
        for path in Path(".").iterdir():
            if path.is_dir() and path.name.lower() == f"lab{lab_input.lower()}":
                return path
        
        # Try removing "lab" prefix if provided
        if lab_input.lower().startswith("lab"):
            lab_num = lab_input[3:]
            for path in Path(".").iterdir():
                if path.is_dir() and path.name.lower() == f"lab{lab_num.lower()}":
                    return path
        
        return None
    
    def get_lab_and_task(self):
        """Get lab and task information from user"""
        while True:
            lab_input = input("Enter lab number/identifier (e.g., 1, Lab1, 6a): ").strip()
            if not lab_input:
                print("Lab identifier cannot be empty.")
                continue
            
            lab_dir = self.find_lab_directory(lab_input)
            if not lab_dir:
                print(f"Lab directory not found for: {lab_input}")
                print("Available lab directories:")
                lab_dirs = [d.name for d in Path(".").iterdir() if d.is_dir() and d.name.lower().startswith("lab")]
                if lab_dirs:
                    print(", ".join(sorted(lab_dirs)))
                else:
                    print("No lab directories found.")
                continue
            
            break
        
        while True:
            try:
                task_num = int(input("Enter task number: ").strip())
                if task_num < 1:
                    print("Task number must be positive.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer for task number.")
        
        return lab_dir, task_num
    
    def create_task_directory(self, lab_dir, task_num):
        """Create task directory if it doesn't exist"""
        task_dir = lab_dir / f"task {task_num}"
        task_dir.mkdir(exist_ok=True)
        return task_dir
    
    def move_screenshots(self, screenshots, target_dir):
        """Move screenshots to target directory"""
        moved_count = 0
        skipped_count = 0
        skipped_files = []
        
        for screenshot in screenshots:
            target_path = target_dir / screenshot.name
            
            if target_path.exists():
                print(f"Skipping (already exists): {screenshot.name}")
                skipped_count += 1
                skipped_files.append(screenshot.name)
                continue
            
            try:
                shutil.move(str(screenshot), str(target_path))
                print(f"Moved: {screenshot.name}")
                moved_count += 1
            except Exception as e:
                print(f"Error moving {screenshot.name}: {e}")
                skipped_count += 1
                skipped_files.append(screenshot.name)
        
        return moved_count, skipped_count, skipped_files
    
    def run(self, reconfigure=False):
        """Main execution function"""
        try:
            # Configure screenshot directory
            screenshot_dir = self.configure_screenshot_directory(reconfigure)
            
            if reconfigure:
                return
            
            # Detect screenshots
            print(f"\nScanning for screenshots in: {screenshot_dir}")
            screenshots = self.detect_screenshots(screenshot_dir)
            
            if not screenshots:
                print("No screenshots found matching expected naming conventions.")
                return
            
            print(f"Found {len(screenshots)} screenshot(s):")
            for screenshot in screenshots:
                print(f"  - {screenshot.name}")
            
            # Get lab and task information
            print()
            lab_dir, task_num = self.get_lab_and_task()
            
            # Create task directory
            task_dir = self.create_task_directory(lab_dir, task_num)
            print(f"\nTarget directory: {task_dir}")
            
            # Move screenshots
            print(f"\nMoving screenshots...")
            moved_count, skipped_count, skipped_files = self.move_screenshots(screenshots, task_dir)
            
            # Report results
            print(f"\nOperation complete:")
            print(f"  - Moved: {moved_count} file(s)")
            print(f"  - Skipped: {skipped_count} file(s)")
            
            if skipped_files:
                print("Skipped files:")
                for filename in skipped_files:
                    print(f"  - {filename}")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Organize screenshots into lab/task directories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python organize_screenshots.py                    # Normal operation
  python organize_screenshots.py --reconfigure      # Update configuration
        """
    )
    
    parser.add_argument(
        "--reconfigure",
        action="store_true",
        help="Reconfigure screenshot source directory"
    )
    
    args = parser.parse_args()
    
    organizer = ScreenshotOrganizer()
    organizer.run(reconfigure=args.reconfigure)


if __name__ == "__main__":
    main()