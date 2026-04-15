"""Tests for duplicate file detection."""
import pytest
from pathlib import Path
from organizer.duplicate import DuplicateFinder
import tempfile
import shutil


def test_calculate_hash():
    """Test file hash calculation."""
    finder = DuplicateFinder()
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("test content")
        temp_path = Path(f.name)
    
    try:
        hash1 = finder._calculate_hash(temp_path)
        assert len(hash1) == 64  # SHA256 produces 64 hex characters
        assert hash1 != ""
    finally:
        temp_path.unlink()


def test_find_duplicates():
    """Test duplicate detection."""
    finder = DuplicateFinder()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create duplicate files
        file1 = tmpdir / "file1.txt"
        file2 = tmpdir / "file2.txt"
        file3 = tmpdir / "file3.txt"
        
        file1.write_text("same content")
        file2.write_text("same content")
        file3.write_text("different content")
        
        duplicates = finder.find_duplicates(tmpdir, recursive=False)
        
        # Should find one group of duplicates (file1 and file2)
        assert len(duplicates) == 1
        
        # Get the duplicate group
        dup_group = list(duplicates.values())[0]
        assert len(dup_group) == 2
