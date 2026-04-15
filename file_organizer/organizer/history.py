"""Operation history tracking and undo functionality."""
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import shutil
import logging

logger = logging.getLogger(__name__)


class OperationHistory:
    """Tracks operations and enables undo functionality."""
    
    def __init__(self, history_file: Path = Path("logs/history.json")):
        """Initialize operation history.
        
        Args:
            history_file: Path to history JSON file
        """
        self.history_file = history_file
        self.history_file.parent.mkdir(exist_ok=True)
    
    def save_operation(self, operation_type: str, directory: Path, result: Dict[str, Any]):
        """Save operation to history.
        
        Args:
            operation_type: Type of operation (organize, organize_date, rename)
            directory: Directory where operation was performed
            result: Operation result dictionary
        """
        try:
            history = self._load_history()
            
            operation = {
                'timestamp': datetime.now().isoformat(),
                'type': operation_type,
                'directory': str(directory),
                'result': result
            }
            
            history.append(operation)
            
            # Keep only last 50 operations
            history = history[-50:]
            
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            logger.info(f"Saved operation to history: {operation_type}")
        
        except Exception as e:
            logger.error(f"Error saving operation history: {e}")
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """Load operation history from file.
        
        Returns:
            List of operation dictionaries
        """
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading history: {e}")
                return []
        return []
    
    def undo_last(self) -> Dict[str, Any]:
        """Undo the last operation.
        
        Returns:
            Dictionary with undo results
        """
        try:
            history = self._load_history()
            
            if not history:
                return {
                    'success': False,
                    'message': 'No operations to undo',
                    'reverted': 0
                }
            
            last_operation = history[-1]
            
            # Only undo organize operations (not rename)
            if last_operation['type'] not in ['organize', 'organize_date']:
                return {
                    'success': False,
                    'message': f"Cannot undo {last_operation['type']} operations",
                    'reverted': 0
                }
            
            operations = last_operation['result'].get('operations', [])
            reverted = 0
            
            # Reverse the operations
            for op in reversed(operations):
                try:
                    source = Path(op['destination'])
                    destination = Path(op['source'])
                    
                    if source.exists():
                        shutil.move(str(source), str(destination))
                        reverted += 1
                        logger.info(f"Reverted: {source} → {destination}")
                except Exception as e:
                    logger.error(f"Error reverting {op}: {e}")
            
            # Remove last operation from history
            history = history[:-1]
            with open(self.history_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return {
                'success': True,
                'message': 'Operation undone successfully',
                'reverted': reverted
            }
        
        except Exception as e:
            logger.error(f"Error undoing operation: {e}")
            return {
                'success': False,
                'message': f'Error: {str(e)}',
                'reverted': 0
            }
