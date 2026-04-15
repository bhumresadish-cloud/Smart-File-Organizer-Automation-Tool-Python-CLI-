"""Tests for file moving operations."""
import pytest
from pathlib import Path
from organizer.mover import FileMover
from organizer.config import Config
import tempfile


def test_organize_by_type_dry_run():
    """Test organize by type in dry run mode."""
    config = Config(Path("test_config.json"))
    mover = FileMover(config)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create test files
        (tmpdir / "test.jpg").touch()
        (tmpdir / "test.pdf").touch()
        (tmpdir / "test.mp3").touch()
        
        result = mover.organize_by_type(tmpdir, dry_run=True)
        
        assert result['success'] is True
        assert result['moved'] == 3
        
        # Files should still be in root (dry run)
        assert (tmpdir / "test.jpg").exists()
        assert not (tmpdir / "Images").exists()


def test_organize_by_type_actual():
    """Test actual file organization by type."""
    config = Config(Path("test_config.json"))
    mover = FileMover(config)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create test files
        (tmpdir / "photo.jpg").touch()
        (tmpdir / "document.pdf").touch()
        
        result = mover.organize_by_type(tmpdir, dry_run=False)
        
        assert result['success'] is True
        assert result['moved'] == 2
        
        # Check files moved to correct folders
        assert (tmpdir / "Images" / "photo.jpg").exists()
        assert (tmpdir / "Documents" / "document.pdf").exists()
        assert not (tmpdir / "photo.jpg").exists()


def test_unique_path_generation():
    """Test unique path generation for conflicts."""
    config = Config(Path("test_config.json"))
    mover = FileMover(config)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        existing = tmpdir / "test.txt"
        existing.touch()
        
        unique = mover._get_unique_path(existing)
        assert unique == tmpdir / "test_1.txt"
