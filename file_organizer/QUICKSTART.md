# 🚀 Quick Start Guide

Get started with Smart File Organizer in 5 minutes!

## Installation

```bash
# Navigate to project directory
cd file_organizer

# Install dependencies
pip install -r requirements.txt
```

## First Run

```bash
# Test the CLI
python main.py --help
```

You should see all available commands.

## Try It Out

### 1. Create a Test Folder

```bash
# Create test directory with sample files
mkdir test_folder
cd test_folder

# Create some test files (Windows)
echo "test" > document.pdf
echo "test" > photo.jpg
echo "test" > video.mp4
echo "test" > song.mp3

cd ..
```

### 2. Preview Organization (Dry Run)

```bash
python main.py organize test_folder --dry-run
```

You'll see what would happen without actually moving files.

### 3. Organize for Real

```bash
python main.py organize test_folder
```

Check `test_folder/` - files are now organized into categories!

### 4. View Statistics

```bash
python main.py stats test_folder
```

See file counts and sizes by category.

### 5. Undo If Needed

```bash
python main.py undo
```

Files return to original locations.

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for real-world scenarios
- Customize [config.json](config.json) for your file types
- Run tests: `pytest tests/ -v`

## Common Commands Cheat Sheet

```bash
# Organize by type
python main.py organize <path>

# Organize by date
python main.py organize-date <path>

# Bulk rename
python main.py rename <path> --prefix myprefix

# Find duplicates
python main.py duplicates <path>

# View stats
python main.py stats <path>

# Watch folder
python main.py watch <path>

# Undo last operation
python main.py undo
```

## Tips

- Always use `--dry-run` first on important folders
- Check `logs/app.log` for detailed operation logs
- Backup important files before organizing
- Use `stats` command to understand your files first

**Happy organizing! 🎉**
