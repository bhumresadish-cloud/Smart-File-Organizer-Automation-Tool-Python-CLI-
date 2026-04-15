"""Configuration management for file organization rules."""
import json
from pathlib import Path
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class Config:
    """Manages configuration and file type mappings."""
    
    DEFAULT_CATEGORIES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".odt"],
        "Videos": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv"],
        "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Code": [".py", ".js", ".java", ".cpp", ".c", ".html", ".css", ".json", ".xml"],
        "Misc": []
    }
    
    def __init__(self, config_path: Path = Path("config.json")):
        """Initialize configuration.
        
        Args:
            config_path: Path to configuration JSON file
        """
        self.config_path = config_path
        self.categories = self._load_config()
    
    def _load_config(self) -> Dict[str, List[str]]:
        """Load configuration from JSON file or use defaults.
        
        Returns:
            Dictionary mapping categories to file extensions
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    custom_config = json.load(f)
                logger.info(f"Loaded custom configuration from {self.config_path}")
                return custom_config.get('categories', self.DEFAULT_CATEGORIES)
            except Exception as e:
                logger.error(f"Error loading config: {e}. Using defaults.")
                return self.DEFAULT_CATEGORIES
        else:
            self._save_default_config()
            return self.DEFAULT_CATEGORIES
    
    def _save_default_config(self):
        """Save default configuration to file."""
        try:
            config_data = {
                "categories": self.DEFAULT_CATEGORIES,
                "description": "Custom file organization rules"
            }
            with open(self.config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            logger.info(f"Created default config at {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving default config: {e}")
    
    def get_category(self, extension: str) -> str:
        """Get category for a file extension.
        
        Args:
            extension: File extension (e.g., '.jpg')
        
        Returns:
            Category name or 'Misc' if not found
        """
        extension = extension.lower()
        for category, extensions in self.categories.items():
            if extension in extensions:
                return category
        return "Misc"
