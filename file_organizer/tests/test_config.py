"""Tests for configuration management."""
import pytest
from pathlib import Path
from organizer.config import Config


def test_default_categories():
    """Test default category loading."""
    config = Config(Path("test_config.json"))
    
    assert "Images" in config.categories
    assert "Documents" in config.categories
    assert ".jpg" in config.categories["Images"]


def test_get_category():
    """Test category detection."""
    config = Config(Path("test_config.json"))
    
    assert config.get_category(".jpg") == "Images"
    assert config.get_category(".pdf") == "Documents"
    assert config.get_category(".mp4") == "Videos"
    assert config.get_category(".unknown") == "Misc"


def test_case_insensitive():
    """Test case-insensitive extension matching."""
    config = Config(Path("test_config.json"))
    
    assert config.get_category(".JPG") == "Images"
    assert config.get_category(".PDF") == "Documents"
