"""Folder statistics and analysis."""
from pathlib import Path
from typing import Dict, Any
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class FolderStats:
    """Analyzes folder statistics by category."""
    
    def __init__(self, config):
        """Initialize with configuration.
        
        Args:
            config: Config instance with category mappings
        """
        self.config = config
    
    def get_statistics(self, directory: Path) -> Dict[str, Any]:
        """Get comprehensive folder statistics.
        
        Args:
            directory: Directory to analyze
        
        Returns:
            Dictionary with statistics by category
        """
        stats = defaultdict(lambda: {'count': 0, 'size': 0})
        total_files = 0
        total_size = 0
        
        try:
            files = [f for f in directory.rglob("*") if f.is_file()]
            
            for file in files:
                try:
                    category = self.config.get_category(file.suffix)
                    file_size = file.stat().st_size
                    
                    stats[category]['count'] += 1
                    stats[category]['size'] += file_size
                    
                    total_files += 1
                    total_size += file_size
                except Exception as e:
                    logger.warning(f"Error processing {file}: {e}")
            
            # Convert to human-readable format
            for category in stats:
                stats[category]['size_human'] = self._format_size(stats[category]['size'])
            
            return {
                'by_category': dict(stats),
                'total_files': total_files,
                'total_size': total_size,
                'total_size_human': self._format_size(total_size)
            }
        
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {
                'by_category': {},
                'total_files': 0,
                'total_size': 0,
                'total_size_human': '0 B'
            }
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format bytes to human-readable size.
        
        Args:
            size_bytes: Size in bytes
        
        Returns:
            Formatted string (e.g., '1.5 MB')
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
