# 👨‍💻 Developer Guide

Guide for developers who want to understand, modify, or extend the Smart File Organizer.

## 🏗️ Architecture Overview

### Component Diagram
```
┌─────────────┐
│   main.py   │  ← CLI Entry Point (Typer)
└──────┬──────┘
       │
       ├─────────────────────────────────────┐
       │                                     │
┌──────▼──────┐                    ┌────────▼────────┐
│  organizer/ │                    │     logs/       │
│   package   │                    │  app.log        │
└──────┬──────┘                    │  history.json   │
       │                           └─────────────────┘
       │
       ├── config.py      (Configuration)
       ├── mover.py       (File Organization)
       ├── duplicate.py   (Duplicate Detection)
       ├── watcher.py     (File System Monitoring)
       ├── stats.py       (Statistics)
       ├── renamer.py     (Bulk Renaming)
       └── history.py     (Undo System)
```

## 📦 Module Breakdown

### 1. main.py - CLI Interface
**Purpose**: Command-line interface using Typer framework

**Key Functions**:
- `organize()`: Organize files by type
- `organize_date()`: Organize files by date
- `rename()`: Bulk rename files
- `duplicates()`: Find duplicate files
- `stats()`: Show folder statistics
- `watch()`: Watch folder for changes
- `undo()`: Undo last operation

**Adding New Commands**:
```python
@app.command()
def my_new_command(
    path: Path = typer.Argument(..., help="Path to process"),
    option: str = typer.Option("default", "--option", help="Custom option")
):
    """Description of new command."""
    # Implementation
    typer.secho("Success!", fg=typer.colors.GREEN)
```

### 2. config.py - Configuration Management
**Purpose**: Load and manage file type categories

**Key Methods**:
- `_load_config()`: Load from JSON or use defaults
- `get_category()`: Map extension to category
- `_save_default_config()`: Create default config.json

**Adding New Categories**:
Edit `config.json`:
```json
{
  "categories": {
    "NewCategory": [".ext1", ".ext2"]
  }
}
```

### 3. mover.py - File Organization
**Purpose**: Core file moving logic

**Key Methods**:
- `organize_by_type()`: Sort by extension
- `organize_by_date()`: Sort by modification date
- `_get_unique_path()`: Handle naming conflicts

**Algorithm Flow**:
```
1. Scan directory for files
2. For each file:
   a. Determine target category/date
   b. Create target directory
   c. Handle naming conflicts
   d. Move file (or preview if dry-run)
3. Log operations
4. Return results
```

### 4. duplicate.py - Duplicate Detection
**Purpose**: Find duplicate files using SHA256 hashing

**Key Methods**:
- `_calculate_hash()`: Compute file hash
- `find_duplicates()`: Scan and group duplicates

**Algorithm**:
```python
hash_map = {}
for file in files:
    hash = SHA256(file)
    hash_map[hash].append(file)

duplicates = {hash: files for hash, files in hash_map.items() if len(files) > 1}
```

### 5. watcher.py - File System Monitoring
**Purpose**: Auto-organize new files in real-time

**Key Classes**:
- `FileOrganizerHandler`: Event handler
- `FolderWatcher`: Observer wrapper

**Event Flow**:
```
File Created → on_created() → Wait 1s → Determine Category → Move File
```

### 6. stats.py - Statistics
**Purpose**: Analyze folder contents

**Key Methods**:
- `get_statistics()`: Calculate file counts and sizes
- `_format_size()`: Convert bytes to human-readable

### 7. renamer.py - Bulk Renaming
**Purpose**: Rename multiple files with pattern

**Key Methods**:
- `bulk_rename()`: Rename with prefix + counter
- `_get_unique_name()`: Handle conflicts

### 8. history.py - Undo System
**Purpose**: Track operations and enable undo

**Key Methods**:
- `save_operation()`: Log operation to JSON
- `undo_last()`: Reverse last operation
- `_load_history()`: Load history from file

**History Format**:
```json
[
  {
    "timestamp": "2024-01-15T10:30:00",
    "type": "organize",
    "directory": "/path/to/folder",
    "result": {
      "operations": [
        {"source": "file.jpg", "destination": "Images/file.jpg"}
      ]
    }
  }
]
```

## 🔧 Common Modifications

### Add New File Category

**Step 1**: Edit `config.json`
```json
{
  "categories": {
    "Ebooks": [".epub", ".mobi", ".azw"]
  }
}
```

**Step 2**: Restart application (config auto-loads)

### Add New CLI Command

**In main.py**:
```python
@app.command()
def compress(
    path: Path = typer.Argument(..., help="Directory to compress"),
    format: str = typer.Option("zip", "--format", help="Archive format")
):
    """Compress old files to save space."""
    typer.secho(f"Compressing files in: {path}", fg=typer.colors.CYAN)
    # Implementation here
```

### Add New Organization Strategy

**Create new module**: `organizer/size_organizer.py`
```python
class SizeOrganizer:
    """Organize files by size (Small, Medium, Large)."""
    
    def organize_by_size(self, directory: Path) -> Dict[str, Any]:
        # Implementation
        pass
```

**Add to main.py**:
```python
from organizer.size_organizer import SizeOrganizer

@app.command()
def organize_size(path: Path):
    """Organize files by size."""
    organizer = SizeOrganizer()
    result = organizer.organize_by_size(path)
```

### Customize Logging

**In main.py**, modify logging setup:
```python
logging.basicConfig(
    level=logging.DEBUG,  # More verbose
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.FileHandler('logs/debug.log'),  # Additional log file
        logging.StreamHandler()
    ]
)
```

## 🧪 Testing Guidelines

### Writing New Tests

**Template**:
```python
"""Tests for new feature."""
import pytest
from pathlib import Path
from organizer.new_module import NewClass
import tempfile


def test_new_feature():
    """Test description."""
    # Setup
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create test data
        test_file = tmpdir / "test.txt"
        test_file.write_text("content")
        
        # Execute
        result = NewClass().method(tmpdir)
        
        # Assert
        assert result['success'] is True
        assert test_file.exists()
```

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific test
pytest tests/test_mover.py::test_organize_by_type_actual -v

# With coverage
pytest tests/ --cov=organizer --cov-report=html

# View coverage report
# Open htmlcov/index.html in browser
```

## 🐛 Debugging Tips

### Enable Debug Logging
```python
# In main.py
logging.basicConfig(level=logging.DEBUG)
```

### Check Logs
```bash
# View recent logs
tail -f logs/app.log

# Search for errors
grep ERROR logs/app.log
```

### Use Python Debugger
```python
import pdb

def organize_by_type(self, directory: Path):
    pdb.set_trace()  # Breakpoint
    # Code continues...
```

### Common Issues

**Issue**: Files not moving
- Check file permissions
- Verify path exists
- Check logs for errors

**Issue**: Config not loading
- Verify JSON syntax
- Check file path
- Look for config.json in working directory

**Issue**: Tests failing
- Ensure pytest installed
- Check test file paths
- Verify temp directories cleaned up

## 📚 Code Style Guide

### Naming Conventions
```python
# Classes: PascalCase
class FileMover:
    pass

# Functions/Methods: snake_case
def organize_by_type():
    pass

# Constants: UPPER_SNAKE_CASE
DEFAULT_CATEGORIES = {}

# Private methods: _leading_underscore
def _get_unique_path():
    pass
```

### Type Hints
```python
from typing import Dict, List, Any
from pathlib import Path

def process_files(
    directory: Path,
    extensions: List[str],
    dry_run: bool = False
) -> Dict[str, Any]:
    """Always use type hints."""
    pass
```

### Docstrings
```python
def function_name(param1: str, param2: int) -> bool:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When invalid input
    """
    pass
```

### Error Handling
```python
try:
    # Risky operation
    result = process_file(path)
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    return {'success': False, 'error': str(e)}
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

## 🚀 Performance Optimization

### Large Directories
```python
# Use generator for memory efficiency
files = (f for f in directory.rglob("*") if f.is_file())

# Process in batches
for batch in chunks(files, 100):
    process_batch(batch)
```

### Duplicate Detection
```python
# Skip small files (< 1KB) for speed
if file.stat().st_size < 1024:
    continue

# Use multiprocessing for large scans
from multiprocessing import Pool
with Pool() as pool:
    hashes = pool.map(calculate_hash, files)
```

## 📦 Packaging & Distribution

### Create Wheel Package
```bash
python setup.py sdist bdist_wheel
```

### Install Locally
```bash
pip install -e .
```

### Upload to PyPI
```bash
pip install twine
twine upload dist/*
```

## 🔐 Security Considerations

### Path Traversal Prevention
```python
# Validate paths
if not path.resolve().is_relative_to(base_dir):
    raise ValueError("Invalid path")
```

### Safe File Operations
```python
# Use context managers
with open(file, 'r') as f:
    content = f.read()

# Validate file sizes
if file.stat().st_size > MAX_SIZE:
    raise ValueError("File too large")
```

## 📖 Additional Resources

- [Typer Documentation](https://typer.tiangolo.com/)
- [Watchdog Documentation](https://python-watchdog.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Pathlib Guide](https://docs.python.org/3/library/pathlib.html)
- [PEP 8 Style Guide](https://pep8.org/)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Write tests for new features
4. Ensure all tests pass: `pytest tests/`
5. Follow code style guidelines
6. Submit pull request with description

---

**Happy Coding! 🎉**
