"""Tests for folder statistics."""
import pytest
from pathlib import Path
from organizer.stats import FolderStats
from organizer.config import Config
import tempfile


def test_format_size():
    """Test size formatting."""
    assert FolderStats._format_size(1024) == "1.00 KB"
    assert FolderStats._format_size(1024 * 1024) == "1.00 MB"
    assert FolderStats._format_size(500) == "500.00 B"


def test_get_statistics():
    """Test statistics calculation."""
    config = Config(Path("test_config.json"))
    stats = FolderStats(config)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Create test files
        (tmpdir / "test.jpg").write_text("x" * 1000)
        (tmpdir / "test.pdf").write_text("y" * 2000)
        
        result = stats.get_statistics(tmpdir)
        
        assert result['total_files'] == 2
        assert result['total_size'] == 3000
        assert 'Images' in result['by_category']
        assert 'Documents' in result['by_category']
        assert result['by_category']['Images']['count'] == 1
        assert result['by_category']['Documents']['count'] == 1
