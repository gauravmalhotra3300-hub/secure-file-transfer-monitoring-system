import os
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from integrity_checker import IntegrityChecker
from alert_system import AlertSystem
from config import SENSITIVE_PATHS, LOG_FILE


class FileTransferHandler(FileSystemEventHandler):
    """Monitor file system events and detect unauthorized transfers."""
    
    def __init__(self, integrity_checker, alert_system):
        self.integrity_checker = integrity_checker
        self.alert_system = alert_system
        self.logger = logging.getLogger(__name__)
    
    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path, 'created')
    
    def on_moved(self, event):
        if not event.is_directory:
            self.process_file(event.src_path, 'moved')
    
    def on_deleted(self, event):
        if not event.is_directory:
            self.process_file(event.src_path, 'deleted')
    
    def on_modified(self, event):
        if not event.is_directory:
            self.process_file(event.src_path, 'modified')
    
    def process_file(self, file_path, event_type):
        """Process file events and check for violations."""
        try:
            # Check if file is sensitive
            is_sensitive = self._check_if_sensitive(file_path)
            
            # Calculate hash if file exists
            file_hash = None
            if os.path.exists(file_path) and event_type != 'deleted':
                file_hash = self.integrity_checker.calculate_hash(file_path)
            
            # Log event
            log_entry = {
                'timestamp': self._get_timestamp(),
                'event_type': event_type,
                'file_path': file_path,
                'is_sensitive': is_sensitive,
                'file_hash': file_hash,
                'user': self._get_current_user(),
                'process': self._get_process_info()
            }
            
            self.logger.info(f'File Event: {log_entry}')
            
            # Generate alert if sensitive file involved
            if is_sensitive:
                self.alert_system.generate_alert(log_entry)
        
        except Exception as e:
            self.logger.error(f'Error processing file {file_path}: {str(e)}')
    
    def _check_if_sensitive(self, file_path):
        """Check if file is in sensitive directories."""
        for sensitive_path in SENSITIVE_PATHS:
            if sensitive_path in file_path:
                return True
        return False
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _get_current_user(self):
        import getpass
        return getpass.getuser()
    
    def _get_process_info(self):
        import psutil
        try:
            return psutil.Process().name()
        except:
            return 'Unknown'


class FileMonitor:
    """Main file monitoring system."""
    
    def __init__(self):
        self.observer = None
        self.integrity_checker = IntegrityChecker()
        self.alert_system = AlertSystem()
        self.setup_logging()
    
    def setup_logging(self):
        """Configure logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler()
            ]
        )
    
    def start(self, watch_paths):
        """Start monitoring file system."""
        self.observer = Observer()
        event_handler = FileTransferHandler(self.integrity_checker, self.alert_system)
        
        for path in watch_paths:
            if os.path.exists(path):
                self.observer.schedule(event_handler, path, recursive=True)
        
        self.observer.start()
        logging.getLogger(__name__).info('File monitoring started')
    
    def stop(self):
        """Stop monitoring file system."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            logging.getLogger(__name__).info('File monitoring stopped')


if __name__ == '__main__':
    monitor = FileMonitor()
    watch_paths = [os.path.expanduser('~')]
    
    try:
        monitor.start(watch_paths)
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
