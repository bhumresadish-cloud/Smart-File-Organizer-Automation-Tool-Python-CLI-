"""File moving and organization logic."""
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import shutil
import logging

logger = logging.getLogger(__name__)


class FileMover:
    """Handles file moving operations for organization."""
    
    def __init__(self, config):
        """Initialize FileMover with configuration.
        
        Args:
            config: Config instance with category mappings
        """
        self.config = config
    
    def organize_by_type(self, directory: Path, dry_run: bool = False) -> Dict[str, Any]:
        """Organize files by their type/extension.
        
        Args:
            directory: Directory to organize
            dry_run: If True, only preview changes
        
        Returns:
            Dictionary with operation results
        """
        moved_count = 0
        operations = []
        
        try:
            files = [f for f in directory.iterdir() if f.is_file()]
            
            for file in files:
                category = self.config.get_category(file.suffix)
                target_dir = directory / category
                target_path = target_dir / file.name
                
                # Handle name conflicts
                target_path = self._get_unique_path(target_path)
                
                operations.append({
                    'source': str(file),
                    'destination': str(target_path),
                    'category': category
                })
                
                if not dry_run:
                    target_dir.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_path))
                    logger.info(f"Moved {file.name} to {category}/")
                
                moved_count += 1
            
            return {
                'moved': moved_count,
                'operations': operations,
                'success': True
            }
        
        except Exception as e:
            logger.error(f"Error organizing by type: {e}")
            return {
                'moved': moved_count,
                'operations': operations,
                'success': False,
                'error': str(e)
            }
    
    def organize_by_date(self, directory: Path, dry_run: bool = False) -> Dict[str, Any]:
        """Organize files by modified date (YYYY/MM structure).
        
        Args:
            directory: Directory to organize
            dry_run: If True, only preview changes
        
        Returns:
            Dictionary with operation results
        """
        moved_count = 0
        operations = []
        
        try:
            files = [f for f in directory.iterdir() if f.is_file()]
            
            for file in files:
                # Get modification time
                mod_time = datetime.fromtimestamp(file.stat().st_mtime)
                year_month = mod_time.strftime("%Y/%m")
                
                target_dir = directory / year_month
                target_path = target_dir / file.name
                
                # Handle name conflicts
                target_path = self._get_unique_path(target_path)
                
                operations.append({
                    'source': str(file),
                    'destination': str(target_path),
                    'date': year_month
                })
                
                if not dry_run:
                    target_dir.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(file), str(target_path))
                    logger.info(f"Moved {file.name} to {year_month}/")
                
                moved_count += 1
            
            return {
                'moved': moved_count,
                'operations': operations,
                'success': True
            }
        
        except Exception as e:
            logger.error(f"Error organizing by date: {e}")
            return {
                'moved': moved_count,
                'operations': operations,
                'success': False,
                'error': str(e)
            }
    
    def _get_unique_path(self, path: Path) -> Path:
        """Generate unique path if file already exists.
        
        Args:
            path: Original path
        
        Returns:
            Unique path with counter if needed
        """
        if not path.exists():
            return path
        
        counter = 1
        while True:
            new_path = path.parent / f"{path.stem}_{counter}{path.suffix}"
            if not new_path.exists():
                return new_path
            counter += 1
