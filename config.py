"""Configuration settings for Secure File Transfer Monitoring System."""

import os
from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).parent

# Logging Configuration
LOG_DIR = PROJECT_ROOT / 'logs'
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / 'file_monitor.log'
ALERT_LOG_FILE = LOG_DIR / 'alerts.log'

# Sensitive File Paths to Monitor
SENSITIVE_PATHS = [
    'Documents',
    'Desktop',
    'Downloads',
    'Pictures',
    'Music',
    'Videos',
    'AppData',  # Windows
    '.ssh',  # SSH keys
    '.gnupg',  # GPG keys
    'confidential',
    'private',
    'secrets',
    '/etc/passwd',  # Linux
    '/etc/shadow',  # Linux
]

# Excluded Paths from Monitoring
EXCLUDED_PATHS = [
    '.git',
    '__pycache__',
    '.venv',
    'node_modules',
    '.cache',
    'temp',
    'tmp',
]

# File Hashing Configuration
HASH_ALGORITHM = 'sha256'  # 'sha256' or 'md5'
BLOCK_SIZE = 65536  # 64KB blocks for hash calculation

# Alert Configuration
ALERT_THRESHOLD = 5  # Number of high-severity alerts before escalation
ALERT_SEVERITY_LEVELS = {
    'LOW': 1,
    'MEDIUM': 2,
    'HIGH': 3,
    'CRITICAL': 4
}

# File Transfer Detection
MONITORED_EXTENSIONS = [
    '.doc', '.docx', '.pdf', '.xls', '.xlsx',  # Office
    '.zip', '.rar', '.7z',  # Archives
    '.sql', '.db', '.sqlite',  # Databases
    '.config', '.conf', '.ini',  # Configuration
    '.key', '.pem', '.ppk',  # Encryption keys
]

# USB and Network Drive Paths
USB_PATHS = [
    '/media',  # Linux
    '/mnt',  # Linux
    'D:', 'E:', 'F:',  # Windows
]

CLOUD_SYNC_PATHS = [
    'Dropbox',
    'Google Drive',
    'OneDrive',
    'iCloud',
]

# Monitoring Settings
RECURSIVE_MONITORING = True
WATCH_INTERVAL = 1  # seconds
MAX_ALERT_HISTORY = 1000

# Report Generation
REPORT_FORMAT = 'json'  # 'json' or 'csv'
REPORT_DIR = PROJECT_ROOT / 'reports'
REPORT_DIR.mkdir(exist_ok=True)

# Email Configuration (Optional)
ENABLE_EMAIL_ALERTS = False
EMAIL_SENDER = 'alerts@example.com'
EMAIL_RECIPIENTS = ['admin@example.com']
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Database Configuration (Optional)
ENABLE_DATABASE = False
DATABASE_PATH = PROJECT_ROOT / 'file_monitor.db'
