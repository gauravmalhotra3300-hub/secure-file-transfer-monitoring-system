# Deployment Guide - Secure File Transfer Monitoring System

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Running the System](#running-the-system)
5. [Docker Deployment](#docker-deployment)
6. [Troubleshooting](#troubleshooting)
7. [Performance Tuning](#performance-tuning)

---

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+, CentOS 8+) or Windows 10/11 with WSL2
- **Python**: 3.9 or higher
- **Memory**: Minimum 2GB RAM
- **Disk Space**: Minimum 5GB for logs and database
- **Network**: Stable internet connection for email notifications

### Required Packages
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.9 python3-pip git

# CentOS/RHEL
sudo yum install python39 python39-pip git

# Windows (using WSL2)
wsl --install
pip install python
```

---

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/gauravmalhotra3300-hub/secure-file-transfer-monitoring-system.git
cd secure-file-transfer-monitoring-system
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python3 -c "import file_monitor; import integrity_checker; import alert_system; print('All modules imported successfully!')"
```

---

## Configuration

### Edit config.py
Create/modify `config.py` with the following settings:

```python
# config.py
MONITORED_DIRECTORIES = [
    '/home/user/sensitive_files',
    '/var/transfer_logs',
    '/opt/secure_data'
]

MONITORED_EXTENSIONS = ['.doc', '.pdf', '.xls', '.csv', '.txt', '.pptx']

ALERT_THRESHOLD = 100  # MB - alert if file transfer > 100MB

# Email Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'your-email@gmail.com'
SMTP_PASSWORD = 'your-app-password'  # Use App Password, not regular password
ALERT_EMAIL = 'security-admin@company.com'

# Logging Configuration
LOG_DIRECTORY = './logs'
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR
LOG_MAX_SIZE = '100MB'
LOG_RETENTION_DAYS = 30

# Database Configuration
DB_TYPE = 'sqlite'  # or 'postgresql'
DB_PATH = './data/monitoring.db'

# Integrity Check Settings
HASH_ALGORITHM = 'sha256'
CHECK_INTERVAL_SECONDS = 3600  # Check every hour

# Dashboard Settings
DASHBOARD_PORT = 5000
DASHBOARD_HOST = '0.0.0.0'
```

### Environment Variables
Alternatively, set environment variables:

```bash
export MONITORED_DIRECTORIES="/home/user/sensitive_files,/var/transfer_logs"
export ALERT_THRESHOLD="100"
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export ALERT_EMAIL="security-admin@company.com"
```

---

## Running the System

### Option 1: Direct Execution
```bash
# Activate virtual environment
source venv/bin/activate

# Run the monitoring system
python3 file_monitor.py &

# Run integrity checker
python3 integrity_checker.py &

# Run alert system
python3 alert_system.py &

# View logs
tail -f logs/monitoring.log
```

### Option 2: Using Main Script
```bash
python3 setup.py install
secure-monitor --config config.py --mode production
```

### Option 3: Systemd Service (Linux)
```bash
# Create systemd service file
sudo nano /etc/systemd/system/secure-monitor.service
```

Add the following content:
```ini
[Unit]
Description=Secure File Transfer Monitoring System
After=network.target

[Service]
Type=simple
User=monitor
WorkingDirectory=/opt/secure-file-transfer-monitoring-system
Environment="PATH=/opt/secure-file-transfer-monitoring-system/venv/bin"
ExecStart=/opt/secure-file-transfer-monitoring-system/venv/bin/python3 file_monitor.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable secure-monitor
sudo systemctl start secure-monitor
sudo systemctl status secure-monitor
```

---

## Docker Deployment

### Dockerfile
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs /app/data

CMD ["python3", "file_monitor.py"]
```

### Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  file-monitor:
    build: .
    container_name: secure-monitor
    volumes:
      - /monitored/path:/monitored:ro
      - ./logs:/app/logs
      - ./data:/app/data
      - ./config.py:/app/config.py:ro
    environment:
      - MONITORED_DIRECTORIES=/monitored
      - LOG_LEVEL=INFO
    restart: unless-stopped
    
  dashboard:
    build: .
    container_name: monitor-dashboard
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=dashboard.py
    depends_on:
      - file-monitor
    restart: unless-stopped
```

Deploy:
```bash
docker-compose up -d
docker-compose logs -f
```

---

## Troubleshooting

### Issue: Module Not Found Error
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Permission Denied for Directories
```bash
# Add user to group
sudo usermod -a -G security monitor_user
sudo chmod g+rx /monitored/directory
```

### Issue: Email Notifications Not Working
```bash
# Verify SMTP credentials
# Gmail: Use App Password (not regular password)
# Check firewall rules for SMTP port 587
telnet smtp.gmail.com 587
```

### Issue: High CPU Usage
```bash
# Adjust check intervals in config.py
CHECK_INTERVAL_SECONDS = 7200  # Increase to 2 hours
FILE_SCAN_INTERVAL = 300  # Increase to 5 minutes
```

### Issue: Disk Space Issues
```bash
# Implement log rotation
# Add to config.py:
LOG_ROTATION_SIZE = '50MB'
LOG_RETENTION_DAYS = 15
```

---

## Performance Tuning

### Optimize Monitoring
```python
# In config.py
# Monitor specific extensions only
MONITORED_EXTENSIONS = ['.pdf', '.doc', '.xls']  # Don't monitor all files

# Increase scan interval for less frequent monitoring
FILE_SCAN_INTERVAL = 600  # 10 minutes instead of 1 minute

# Exclude directories
EXCLUDE_DIRECTORIES = ['.cache', '__pycache__', '.git']
```

### Database Optimization
```bash
# Create indexes for faster queries
sqlite3 data/monitoring.db "CREATE INDEX idx_file_hash ON files(hash_value);"
sqlite3 data/monitoring.db "CREATE INDEX idx_timestamp ON events(timestamp);"
```

### Memory Management
```python
# Implement batch processing
BATCH_SIZE = 100  # Process 100 files at a time
MEMORY_LIMIT = 500  # MB - free memory if exceeds
```

---

## Health Checks

Monitor system health:
```bash
# Check if services are running
pssp aux | grep "file_monitor\|integrity_checker\|alert_system"

# Check disk usage
df -h /monitored/path

# Check logs for errors
grep ERROR logs/monitoring.log | tail -20

# Check database integrity
sqlite3 data/monitoring.db "PRAGMA integrity_check;"
```

---

## Uninstallation

To remove the system:
```bash
# Stop services
sudo systemctl stop secure-monitor
sudo systemctl disable secure-monitor

# Remove files
rm -rf /opt/secure-file-transfer-monitoring-system

# Remove systemd service
sudo rm /etc/systemd/system/secure-monitor.service
sudo systemctl daemon-reload
```

---

## Support & Documentation

For more information, see:
- [README.md](README.md) - Project overview
- [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) - System architecture
- [SAMPLE_OUTPUTS.md](SAMPLE_OUTPUTS.md) - Example monitoring outputs
