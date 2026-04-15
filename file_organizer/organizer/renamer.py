"""Bulk file renaming functionality."""
from pathlib import Path
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class FileRenamer:
    """Handles bulk file renaming operations."""
    
    def bulk_rename(self, directory: Path, prefix: str = "file") -> Dict[str, Any]:
        """Rename all files in directory with custom prefix.
        
        Args:
            directory: Directory containing files to rename
            prefix: Prefix for renamed files
        
        Returns:
            Dictionary with operation results
        """
        renamed_count = 0
        operations = []
        
        try:
            files = sorted([f for f in directory.iterdir() if f.is_file()])
            
            for idx, file in enumerate(files, start=1):
                new_name = f"{prefix}_{idx}{file.suffix}"
                new_path = directory / new_name
                
                # Handle conflicts
                new_path = self._get_unique_name(new_path)
                
                operations.append({
                    'old_name': file.name,
                    'new_name': new_path.name
                })
                
                file.rename(new_path)
                logger.info(f"Renamed {file.name} to {new_path.name}")
                renamed_count += 1
            
            return {
                'renamed': renamed_count,
                'operations': operations,
                'success': True
            }
        
        except Exception as e:
            logger.error(f"Error renaming files: {e}")
            return {
                'renamed': renamed_count,
                'operations': operations,
                'success': False,
                'error': str(e)
            }
    
    def _get_unique_name(self, path: Path) -> Path:
        """Generate unique filename if conflict exists.
        
        Args:
            path: Original path
        
        Returns:
            Unique path
        """
        if not path.exists():
            return path
        
        counter = 1
        while True:
            new_path = path.parent / f"{path.stem}_dup{counter}{path.suffix}"
            if not new_path.exists():
                return new_path
            counter += 1
