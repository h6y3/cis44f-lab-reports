# Screenshot Organization Script Specification

## Overview
Create a Python script that automatically organizes screenshots from a configurable source directory into the appropriate lab/task structure used by this CIS44F project.

## Configuration Management

### Initial Setup
- **First Run**: If no configuration exists, prompt user for screenshot source directory
- **Default Options**: 
  - Mac: `~/Desktop`
  - Windows: `%USERPROFILE%\Desktop` 
  - Linux: `~/Desktop`
- **User Choice**: Allow manual directory specification
- **Config Storage**: Save to `screenshot_config.json` in project root alongside existing `config.json`
- **Format**: JSON with `{"screenshot_source_directory": "/path/to/screenshots"}`

### Reconfiguration
- Provide command-line flag (e.g., `--reconfigure`) to update screenshot source directory
- Inform user when configuration is created/updated

## Screenshot Detection

### Naming Conventions by Platform
- **Mac**: `Screen Shot YYYY-MM-DD at HH.MM.SS AM/PM.png`
- **Windows**: `Screenshot YYYY-MM-DD HHMMSS.png` or `Annotation YYYY-MM-DD HHMMSS.png`
- **Linux**: `Screenshot from YYYY-MM-DD HH-MM-SS.png`

### File Types
- Support: `.png`, `.jpg`, `.jpeg` (case-insensitive)
- Sort by filename (timestamp) for chronological organization

## Lab/Task Structure Integration

### Directory Structure
- **Lab Pattern**: `Lab{N}` (e.g., `Lab1`, `Lab2`, `Lab6a`)
- **Task Pattern**: `task {N}` (with space, e.g., `task 1`, `task 2`)
- **Target Path**: `Lab{N}/task {M}/` where screenshots are placed

### User Input Collection
- **Interactive Prompts**: 
  - Lab number/identifier (support: `1`, `Lab1`, `lab1`, `6a`, `Lab6a`)
  - Task number (integer)
- **Validation**: Ensure target lab directory exists, create task directory if needed
- **Flexible Matching**: Case-insensitive lab directory matching

## Core Functionality

### Screenshot Processing
1. **Scan** configured source directory for screenshots matching naming conventions
2. **Filter** by timestamp (optional: only move screenshots newer than last run)
3. **Move** (not copy) screenshots to `Lab{N}/task {M}/` directory
4. **Handle Conflicts**: Skip files that already exist in destination
5. **Feedback**: Report number of files moved and any skipped files

### Error Handling
- Invalid/non-existent source directory
- Invalid lab/task numbers
- Permission issues
- File conflicts

## Technical Requirements

### Implementation
- **Language**: Python (leverages existing venv in project)
- **Dependencies**: Use only standard library (os, json, shutil, pathlib, platform)
- **Cross-platform**: Support Mac, Windows, Linux
- **Integration**: Compatible with existing `generate_lab_report.py` workflow

### CLI Interface
```bash
python organize_screenshots.py                    # Normal operation
python organize_screenshots.py --reconfigure      # Update config
python organize_screenshots.py --help            # Show usage
```

## Success Criteria
- Single script works across all platforms
- Minimal code footprint using standard library
- Seamless integration with existing lab report generation
- User-friendly configuration and operation
- Robust error handling and user feedback 
