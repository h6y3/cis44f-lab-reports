# CIS44F Lab Report Generator

A Python-based tool for automatically generating professional PDF lab reports from organized screenshot directories. Originally created for CIS44F (Introduction to Big Data Analytics) at De Anza College during Summer 2025.

## Quick Start

```bash
git clone https://github.com/h6y3/cis44f-lab-reports.git
cd cis44f-lab-reports
./install.sh                    # Will prompt for your name and course info
source lab_report_env/bin/activate
python3 generate_lab_report.py Lab1
```

## Overview

This tool automates the creation of lab reports by scanning directories containing task-organized screenshots and generating formatted PDF documents. Perfect for students who need to submit lab documentation with consistent formatting.

## Features

- **Automatic PDF Generation**: Converts directory structures with screenshots into professional lab reports
- **Flexible Directory Structure**: Supports both "task1" and "task 1" naming conventions  
- **Smart Lab Matching**: Case-insensitive and flexible lab directory matching (supports "Lab1", "lab1", "1", etc.)
- **Professional Formatting**: Generates reports with proper headers, task sections, and image optimization
- **Image Optimization**: Automatically resizes and optimizes screenshots for reasonable PDF file sizes
- **Cross-Platform**: Works on macOS, Windows, and Linux
- **Easy Installation**: Simple setup with virtual environment management
- **Batch Processing**: Generate reports for multiple labs quickly
- **Automated Screenshot Organization**: Smart tool to organize screenshots from any directory into proper lab/task structure

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### macOS Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/h6y3/cis44f-lab-reports.git
   cd cis44f-lab-reports
   ```

2. **Run the installation script:**
   ```bash
   ./install.sh
   ```
   *The installer will prompt you to enter your name and course information which will be saved to `config.json`*

3. **Activate the virtual environment:**
   ```bash
   source lab_report_env/bin/activate
   ```

### Windows Installation

1. **Clone the repository:**
   ```cmd
   git clone https://github.com/h6y3/cis44f-lab-reports.git
   cd cis44f-lab-reports
   ```

2. **Create virtual environment:**
   ```cmd
   python -m venv lab_report_env
   ```

3. **Activate virtual environment:**
   ```cmd
   lab_report_env\Scripts\activate
   ```

4. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

### Linux Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/h6y3/cis44f-lab-reports.git
   cd cis44f-lab-reports
   ```

2. **Run the installation script:**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **Activate the virtual environment:**
   ```bash
   source lab_report_env/bin/activate
   ```

## Usage

### Directory Structure

Organize your lab materials in the following structure:

```
Lab1/
├── task 1/
│   ├── Screenshot1.png
│   └── Screenshot2.png
├── task 2/
│   ├── Screenshot3.png
│   └── Screenshot4.png
└── task 3/
    └── Screenshot5.png
```

### Generating Reports

1. **Activate the virtual environment** (if not already active):
   ```bash
   source lab_report_env/bin/activate  # macOS/Linux
   lab_report_env\Scripts\activate     # Windows
   ```

2. **Generate a lab report:**
   ```bash
   # All of these work the same way:
   python3 generate_lab_report.py Lab1   # Exact directory name
   python3 generate_lab_report.py lab1   # Case-insensitive
   python3 generate_lab_report.py LAB1   # Any case
   python3 generate_lab_report.py 1      # Just the number
   ```

3. **Find your generated PDF:**
   The report will be saved as `Lab1/lab1.pdf`

### Creating Lab Structure

Use the included helper script to create organized lab directories:

```bash
./create_lab_structure.sh
```

This will prompt you for:
- Lab number (e.g., 1, 6a, 6b)
- Number of tasks

### Organizing Screenshots

The tool includes an automated screenshot organizer that can move screenshots from any directory (like Desktop) into the proper lab/task structure:

```bash
# First time setup - configure screenshot source directory
python3 organize_screenshots.py --reconfigure

# Organize screenshots into lab/task directories
python3 organize_screenshots.py
```

**Supported Screenshot Formats:**
- **Mac**: `Screen Shot YYYY-MM-DD at HH.MM.SS AM/PM.png`
- **Windows**: `Screenshot YYYY-MM-DD HHMMSS.png` or `Annotation YYYY-MM-DD HHMMSS.png`
- **Linux**: `Screenshot from YYYY-MM-DD HH-MM-SS.png`

The organizer will:
- Detect screenshots using platform-specific naming conventions
- Prompt you for lab and task numbers
- Move screenshots to the appropriate `Lab{N}/task {M}/` directory
- Skip files that already exist (no overwrites)
- Create task directories automatically if needed

## Report Format

Generated reports include:

- **Header**: Student name and course information
- **Task Sections**: Organized by task number with appropriate screenshots
- **Professional Layout**: Consistent formatting with proper spacing and image sizing

Example header format:
```
Your Name Here
CIS44F - Lab 1

Task 1
[Screenshots for Task 1]

Task 2
[Screenshots for Task 2]
```

## Configuration

### Student Information Setup

The tool uses a `config.json` file to store your personal information. This file is automatically created during installation, but you can also create or edit it manually:

```json
{
  "student_name": "Your Full Name",
  "course_code": "CIS44F", 
  "school": "De Anza College"
}
```

### Screenshot Organization Setup

The screenshot organizer uses `screenshot_config.json` to remember your screenshot source directory:

```json
{
  "screenshot_source_directory": "/Users/username/Desktop"
}
```

### Updating Your Information

To change your name or course information:

1. **Edit the config file directly:**
   ```bash
   nano config.json
   # or
   code config.json
   ```

2. **Re-run the installer:**
   ```bash
   rm config.json
   ./install.sh
   ```

The configuration file is automatically excluded from git commits (in `.gitignore`) to keep your personal information private.

### Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)

## Troubleshooting

### Common Issues

**ImportError: No module named 'reportlab'**
- Ensure you've activated the virtual environment
- Run `pip install -r requirements.txt`

**No lab directory found matching 'xyz'**
- The script will show available lab directories to help you choose the correct one
- Use any case (Lab1, lab1, LAB1) or just the number (1, 7, 6a)

**No screenshots found**
- Verify screenshots are in the correct task directories
- Check file extensions are supported (.png, .jpg, .jpeg)
- Use the screenshot organizer to move screenshots from your source directory

**Screenshot organizer not finding screenshots**
- Ensure screenshots follow platform naming conventions
- Check that the source directory is correctly configured
- Use `--reconfigure` to update the screenshot source directory

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed
2. Verify your directory structure matches the expected format
3. Ensure you're in the correct working directory when running the script

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Created for CIS44F (Introduction to Big Data Analytics) at De Anza College
- Summer 2025 semester
- Built with ReportLab and Pillow for professional PDF generation

---

**Note**: This tool was specifically designed for CIS44F coursework but can be adapted for other courses requiring similar lab report formatting.