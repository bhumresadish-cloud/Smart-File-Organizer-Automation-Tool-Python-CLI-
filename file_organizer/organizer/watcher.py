"""Folder watching and auto-organization."""
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import logging

logger = logging.getLogger(__name__)


class FileOrganizerHandler(FileSystemEventHandler):
    """Handles file system events for auto-organization."""
    
    def __init__(self, config):
        """Initialize handler with configuration.
        
        Args:
            config: Config instance with category mappings
        """
        self.config = config
        super().__init__()
    
    def on_created(self, event):
        """Handle file creation event.
        
        Args:
            event: File system event
        """
        if event.is_directory:
            return
        
        try:
            file_path = Path(event.src_path)
            
            # Wait a bit to ensure file is fully written
            time.sleep(1)
            
            if not file_path.exists():
                return
            
            category = self.config.get_category(file_path.suffix)
            target_dir = file_path.parent / category
            target_dir.mkdir(exist_ok=True)
            
            target_path = target_dir / file_path.name
            
            # Handle conflicts
            counter = 1
            while target_path.exists():
                target_path = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1
            
            file_path.rename(target_path)
            logger.info(f"Auto-organized: {file_path.name} → {category}/")
            print(f"✅ Organized: {file_path.name} → {category}/")
        
        except Exception as e:
            logger.error(f"Error auto-organizing file: {e}")


class FolderWatcher:
    """Watches folder and auto-organizes new files."""
    
    def __init__(self, directory: Path, config):
        """Initialize folder watcher.
        
        Args:
            directory: Directory to watch
            config: Config instance
        """
        self.directory = directory
        self.config = config
        self.observer = Observer()
    
    def start(self):
        """Start watching the folder."""
        event_handler = FileOrganizerHandler(self.config)
        self.observer.schedule(event_handler, str(self.directory), recursive=False)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        
        self.observer.join()
