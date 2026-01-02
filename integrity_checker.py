import hashlib
import os
import logging
from datetime import datetime


class IntegrityChecker:
    """Handle file integrity checks using SHA256 and MD5 hashing."""
    
    def __init__(self, algorithm='sha256'):
        self.algorithm = algorithm.lower()
        self.logger = logging.getLogger(__name__)
        self.hash_cache = {}
    
    def calculate_hash(self, file_path, block_size=65536):
        """Calculate hash of a file.
        
        Args:
            file_path: Path to the file
            block_size: Size of blocks to read (default 65KB)
        
        Returns:
            Hash string or None if file doesn't exist
        """
        if not os.path.exists(file_path):
            self.logger.warning(f'File not found: {file_path}')
            return None
        
        try:
            if self.algorithm == 'sha256':
                hasher = hashlib.sha256()
            elif self.algorithm == 'md5':
                hasher = hashlib.md5()
            else:
                hasher = hashlib.sha256()
            
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(block_size)
                    if not data:
                        break
                    hasher.update(data)
            
            hash_value = hasher.hexdigest()
            self.hash_cache[file_path] = hash_value
            return hash_value
        
        except Exception as e:
            self.logger.error(f'Error calculating hash for {file_path}: {str(e)}')
            return None
    
    def verify_integrity(self, file_path, expected_hash):
        """Verify if file hash matches expected value.
        
        Args:
            file_path: Path to the file
            expected_hash: Expected hash value
        
        Returns:
            Tuple: (is_valid, actual_hash)
        """
        actual_hash = self.calculate_hash(file_path)
        
        if actual_hash is None:
            return False, None
        
        is_valid = actual_hash == expected_hash
        
        if not is_valid:
            self.logger.warning(f'Hash mismatch for {file_path}: expected {expected_hash}, got {actual_hash}')
        
        return is_valid, actual_hash
    
    def get_cached_hash(self, file_path):
        """Retrieve cached hash if available.
        
        Args:
            file_path: Path to the file
        
        Returns:
            Cached hash or None
        """
        return self.hash_cache.get(file_path)
    
    def clear_cache(self, file_path=None):
        """Clear hash cache.
        
        Args:
            file_path: Specific file to clear, or None to clear all
        """
        if file_path:
            if file_path in self.hash_cache:
                del self.hash_cache[file_path]
        else:
            self.hash_cache.clear()
    
    def generate_integrity_report(self, file_paths):
        """Generate integrity report for multiple files.
        
        Args:
            file_paths: List of file paths
        
        Returns:
            Dictionary with file hashes and status
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'files': {}
        }
        
        for file_path in file_paths:
            hash_value = self.calculate_hash(file_path)
            report['files'][file_path] = {
                'hash': hash_value,
                'exists': os.path.exists(file_path),
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }
        
        return report
