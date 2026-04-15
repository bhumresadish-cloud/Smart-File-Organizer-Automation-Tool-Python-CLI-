"""Duplicate file detection using hash comparison."""
import hashlib
from pathlib import Path
from typing import Dict, List
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class DuplicateFinder:
    """Finds duplicate files using SHA256 hashing."""
    
    @staticmethod
    def _calculate_hash(file_path: Path, chunk_size: int = 8192) -> str:
        """Calculate SHA256 hash of a file.
        
        Args:
            file_path: Path to file
            chunk_size: Size of chunks to read
        
        Returns:
            Hexadecimal hash string
        """
        sha256_hash = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(chunk_size), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception as e:
            logger.error(f"Error hashing {file_path}: {e}")
            return ""
    
    def find_duplicates(self, directory: Path, recursive: bool = True) -> Dict[str, List[Path]]:
        """Find duplicate files in directory.
        
        Args:
            directory: Directory to scan
            recursive: If True, scan subdirectories
        
        Returns:
            Dictionary mapping hash to list of duplicate file paths
        """
        hash_map = defaultdict(list)
        
        try:
            # Get all files
            if recursive:
                files = directory.rglob("*")
            else:
                files = directory.glob("*")
            
            files = [f for f in files if f.is_file()]
            
            logger.info(f"Scanning {len(files)} files for duplicates...")
            
            # Calculate hashes
            for file in files:
                file_hash = self._calculate_hash(file)
                if file_hash:
                    hash_map[file_hash].append(file)
            
            # Filter to only duplicates (hash with multiple files)
            duplicates = {
                hash_val: files 
                for hash_val, files in hash_map.items() 
                if len(files) > 1
            }
            
            logger.info(f"Found {len(duplicates)} groups of duplicates")
            return duplicates
        
        except Exception as e:
            logger.error(f"Error finding duplicates: {e}")
            return {}
