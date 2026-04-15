# 🗂️ Smart File Organizer Automation Tool

A professional, production-ready Python CLI tool for automated file management and organization.

## ✨ Features

### Core Features
- **Organize by Type**: Automatically categorize files by extension (Images, Documents, Videos, etc.)
- **Organize by Date**: Sort files into YYYY/MM folder structure based on modification date
- **Bulk Rename**: Rename multiple files with custom prefixes
- **Duplicate Finder**: Detect duplicate files using SHA256 hashing
- **Folder Statistics**: Analyze file counts and sizes by category

### Advanced Features
- **Folder Watcher**: Auto-organize new files as they're added
- **Dry Run Mode**: Preview changes before applying them
- **Undo Operations**: Revert the last organize operation
- **Custom Rules**: Configure file categories via JSON config
- **Comprehensive Logging**: Track all operations in logs/app.log

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone or download the project:
```bash
cd file_organizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python main.py --help
```

## 📖 Usage

### Organize Files by Type
```bash
python main.py organize /path/to/folder
```

With dry run (preview only):
```bash
python main.py organize /path/to/folder --dry-run
```

### Organize Files by Date
```bash
python main.py organize-date /path/to/folder
```

### Bulk Rename Files
```bash
python main.py rename /path/to/folder --prefix photo
```
This renames files to: `photo_1.jpg`, `photo_2.png`, etc.

### Find Duplicates
```bash
python main.py duplicates /path/to/folder
```

### View Folder Statistics
```bash
python main.py stats /path/to/folder
```

### Watch Folder (Auto-organize)
```bash
python main.py watch /path/to/folder
```
Press `Ctrl+C` to stop watching.

### Undo Last Operation
```bash
python main.py undo
```

## ⚙️ Configuration

Edit `config.json` to customize file categories:

```json
{
  "categories": {
    "Images": [".jpg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Custom": [".xyz", ".abc"]
  }
}
```

## 📁 Project Structure

```
file_organizer/
│
├── main.py                 # CLI entry point
├── organizer/
│   ├── __init__.py
│   ├── mover.py           # File moving logic
│   ├── duplicate.py       # Duplicate detection
│   ├── watcher.py         # Folder watching
│   ├── stats.py           # Statistics analysis
│   ├── renamer.py         # Bulk renaming
│   ├── history.py         # Undo functionality
│   └── config.py          # Configuration management
│
├── logs/
│   ├── app.log            # Application logs
│   └── history.json       # Operation history
│
├── config.json            # User configuration
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

## 🧪 Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ --cov=organizer --cov-report=html
```

## 🛠️ Technical Details

### Architecture
- **Modular OOP Design**: Each feature in separate class
- **Type Hints**: Full type annotations for better IDE support
- **Error Handling**: Comprehensive try-catch blocks with logging
- **Pathlib**: Modern path handling (no os.path)

### Key Technologies
- **Typer**: Modern CLI framework with auto-completion
- **Watchdog**: File system event monitoring
- **Hashlib**: SHA256 hashing for duplicate detection
- **Logging**: Built-in Python logging with file output

### Code Quality
- PEP8 compliant
- Docstrings for all functions/classes
- Type hints throughout
- Comprehensive error handling

## 📝 Examples

### Example 1: Organize Downloads Folder
```bash
# Preview changes first
python main.py organize ~/Downloads --dry-run

# Apply organization
python main.py organize ~/Downloads
```

### Example 2: Find and Remove Duplicates
```bash
# Find duplicates
python main.py duplicates ~/Pictures

# Review output and manually delete duplicates
```

### Example 3: Auto-organize Desktop
```bash
# Watch desktop folder
python main.py watch ~/Desktop
```

## 🔒 Safety Features

- **Dry Run Mode**: Test before applying changes
- **Undo Functionality**: Revert last operation
- **Conflict Resolution**: Automatic file renaming on conflicts
- **Comprehensive Logging**: Track all operations

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Add more file categories
- Implement GUI interface
- Add cloud storage integration
- Create pip package

## 📄 License

MIT License - feel free to use in your projects!

## 👨‍💻 Author

Built as a professional portfolio project demonstrating:
- Clean Python architecture
- CLI tool development
- File system operations
- Error handling & logging
- Production-ready code quality

---

**Note**: Always backup important files before running organization operations!
