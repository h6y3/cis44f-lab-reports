# CIS44F Lab Report Generator

A Python-based tool for automatically generating professional PDF lab reports from organized screenshot directories. Originally created for CIS44F (Introduction to Big Data Analytics) at De Anza College during Summer 2025.

## Quick Start

```bash
git clone https://github.com/h6y3/cis44f-lab-reports.git
cd cis44f-lab-reports
./install.sh
source lab_report_env/bin/activate
python3 generate_lab_report.py Lab1
```

## Overview

This tool automates the creation of lab reports by scanning directories containing task-organized screenshots and generating formatted PDF documents. Perfect for students who need to submit lab documentation with consistent formatting.

## Features

- **Automatic PDF Generation**: Converts directory structures with screenshots into professional lab reports
- **Flexible Directory Structure**: Supports both "task1" and "task 1" naming conventions  
- **Professional Formatting**: Generates reports with proper headers, task sections, and image optimization
- **Image Optimization**: Automatically resizes and optimizes screenshots for reasonable PDF file sizes
- **Cross-Platform**: Works on macOS, Windows, and Linux
- **Easy Installation**: Simple setup with virtual environment management
- **Batch Processing**: Generate reports for multiple labs quickly

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
   python3 generate_lab_report.py Lab1
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

## Report Format

Generated reports include:

- **Header**: Student name and course information
- **Task Sections**: Organized by task number with appropriate screenshots
- **Professional Layout**: Consistent formatting with proper spacing and image sizing

Example header format:
```
Han-Shen Yuan
CIS44F - Lab 1

Task 1
[Screenshots for Task 1]

Task 2
[Screenshots for Task 2]
```

## Customization

### Modifying Student Information

Edit the script to change the student name and course information:

```python
# In generate_lab_report.py, line ~120
story.append(Paragraph("Your Name Here", title_style))
story.append(Paragraph(f"CIS44F - {lab_description}", subtitle_style))
```

### Supported Image Formats

- PNG (.png)
- JPEG (.jpg, .jpeg)

## Troubleshooting

### Common Issues

**ImportError: No module named 'reportlab'**
- Ensure you've activated the virtual environment
- Run `pip install -r requirements.txt`

**AttributeError: 'NoneType' object has no attribute 'group'**
- Check that your directory follows the naming convention (e.g., "Lab1", "Lab6a")

**No screenshots found**
- Verify screenshots are in the correct task directories
- Check file extensions are supported (.png, .jpg, .jpeg)

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