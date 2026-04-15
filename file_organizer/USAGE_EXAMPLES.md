# 📚 Usage Examples & Scenarios

## Real-World Use Cases

### 1. Clean Up Downloads Folder

**Scenario**: Your Downloads folder is a mess with hundreds of files.

```bash
# Step 1: Check what you have
python main.py stats ~/Downloads

# Step 2: Preview organization
python main.py organize ~/Downloads --dry-run

# Step 3: Organize for real
python main.py organize ~/Downloads

# Step 4: If you made a mistake, undo it
python main.py undo
```

**Result**: All files sorted into Images/, Documents/, Videos/, etc.

---

### 2. Organize Photo Library by Date

**Scenario**: You have thousands of photos and want them organized by year/month.

```bash
# Organize photos by date taken (modification date)
python main.py organize-date ~/Pictures/Vacation2024

# Result structure:
# 2024/
#   01/
#     photo1.jpg
#     photo2.jpg
#   02/
#     photo3.jpg
```

---

### 3. Rename Batch of Screenshots

**Scenario**: You have 50 screenshots named randomly, want consistent naming.

```bash
# Rename all files with "screenshot" prefix
python main.py rename ~/Desktop/screenshots --prefix screenshot

# Result:
# screenshot_1.png
# screenshot_2.png
# screenshot_3.png
# ...
```

---

### 4. Find Duplicate Files

**Scenario**: You suspect duplicate photos/documents wasting space.

```bash
# Scan for duplicates
python main.py duplicates ~/Documents

# Output shows:
# Hash: a1b2c3d4...
#   - /path/to/file1.pdf
#   - /path/to/copy_of_file1.pdf
#   - /path/to/another_copy.pdf
```

**Action**: Manually review and delete duplicates to save space.

---

### 5. Auto-Organize Desktop

**Scenario**: Keep your desktop clean automatically.

```bash
# Start watching desktop
python main.py watch ~/Desktop

# Now any file you save to desktop gets auto-organized!
# Download a PDF → automatically moves to Documents/
# Save a screenshot → automatically moves to Images/
```

Press `Ctrl+C` when done.

---

### 6. Organize Project Files

**Scenario**: Organize a project folder with mixed file types.

```bash
# First, see what you're working with
python main.py stats ~/Projects/MyProject

# Output:
# Images: 45 files (12.5 MB)
# Documents: 23 files (8.2 MB)
# Code: 156 files (2.1 MB)

# Then organize
python main.py organize ~/Projects/MyProject
```

---

### 7. Custom File Categories

**Scenario**: You work with special file types not in default config.

**Step 1**: Edit `config.json`:
```json
{
  "categories": {
    "Images": [".jpg", ".png", ".gif"],
    "3D Models": [".obj", ".fbx", ".blend"],
    "CAD Files": [".dwg", ".dxf"],
    "Music Production": [".flp", ".als", ".logic"]
  }
}
```

**Step 2**: Run organizer:
```bash
python main.py organize ~/MyFiles
```

Now your custom file types are organized!

---

### 8. Safe Testing with Dry Run

**Scenario**: Not sure what will happen? Test first!

```bash
# Preview without making changes
python main.py organize ~/ImportantFiles --dry-run

# Review the output
# If looks good, run for real:
python main.py organize ~/ImportantFiles
```

---

### 9. Undo Mistakes

**Scenario**: Oops, organized the wrong folder!

```bash
# Immediately undo
python main.py undo

# All files moved back to original locations
```

**Note**: Only works for organize operations, not rename.

---

### 10. Analyze Storage Usage

**Scenario**: Find out what's taking up space.

```bash
python main.py stats ~/

# Output:
# Videos: 45 files (25.3 GB)  ← Aha! Videos taking most space
# Images: 1,234 files (8.7 GB)
# Documents: 567 files (2.1 GB)
```

---

## Advanced Workflows

### Workflow 1: Complete Downloads Cleanup

```bash
# 1. Analyze
python main.py stats ~/Downloads

# 2. Find duplicates
python main.py duplicates ~/Downloads

# 3. Organize by type
python main.py organize ~/Downloads

# 4. Within each category, organize by date
python main.py organize-date ~/Downloads/Documents
python main.py organize-date ~/Downloads/Images
```

---

### Workflow 2: Photo Management

```bash
# 1. Find duplicate photos
python main.py duplicates ~/Pictures

# 2. Organize by date
python main.py organize-date ~/Pictures

# 3. Rename within each month
python main.py rename ~/Pictures/2024/01 --prefix jan_photo
python main.py rename ~/Pictures/2024/02 --prefix feb_photo
```

---

### Workflow 3: Continuous Organization

```bash
# Set up auto-organization for common folders
# Terminal 1:
python main.py watch ~/Downloads

# Terminal 2:
python main.py watch ~/Desktop

# Now both folders stay organized automatically!
```

---

## Tips & Best Practices

### ✅ Do's
- Always use `--dry-run` first on important folders
- Check `logs/app.log` if something goes wrong
- Use `stats` command before organizing to understand your files
- Keep backups of critical files
- Use `undo` immediately if you make a mistake

### ❌ Don'ts
- Don't organize system folders (like C:\Windows)
- Don't run on folders with active applications
- Don't organize without checking dry-run first
- Don't delete the logs/ folder (needed for undo)

---

## Troubleshooting

### Issue: "Permission Denied"
**Solution**: Run with appropriate permissions or choose a different folder.

### Issue: "No operations to undo"
**Solution**: Undo only works for the last organize operation. Check `logs/history.json`.

### Issue: Files not organizing
**Solution**: Check `logs/app.log` for errors. Ensure files aren't locked by other programs.

---

## Integration Ideas

### Cron Job (Linux/Mac)
```bash
# Auto-organize Downloads every day at 2 AM
0 2 * * * /usr/bin/python3 /path/to/main.py organize ~/Downloads
```

### Task Scheduler (Windows)
Create a scheduled task to run:
```
python C:\path\to\main.py organize C:\Users\YourName\Downloads
```

---

**Happy Organizing! 🎉**
