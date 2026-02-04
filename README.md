# Secure File Transfer Monitoring System

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue) ![GitHub Actions](https://github.com/gauravmalhotra3300-hub/secure-file-transfer-monitoring-system/workflows/Python%20CI/CD/badge.svg) ![License](https://img.shields.io/badge/license-MIT-green) ![Status](https://img.shields.io/badge/status-stable-brightgreen)

A comprehensive security project for monitoring and detecting unauthorized file transfers. Implements file integrity checks using hashing, real-time monitoring with watchdog, and generates detailed audit logs for suspicious file movement detection.

## Overview

This project focuses on developing a **Secure File Transfer Monitoring System** designed to ensure data confidentiality and track file movement across a system or network. File transfers—both internal and external—pose significant risks including data leakage, unauthorized access, malware distribution, and insider misuse.

### Key Features

- **File Transfer Logging**: Monitor and log all file copy, move, delete, upload, and download events
- **Unauthorized Movement Detection**: Detect suspicious file transfers to USB drives, network shares, and cloud folders
- **File Integrity Verification**: SHA256/MD5 hash-based integrity checks for tamper detection
- **Real-time Monitoring**: Uses watchdog library for efficient filesystem event detection
- **Alert Generation**: Automatic alerts for policy violations and suspicious activities
- **Audit Logging**: Comprehensive JSON-formatted logs for forensic analysis
- **Blue Team Support**: Defensive monitoring experience for SOC and digital forensics

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/gauravmalhotra3300-hub/secure-file-transfer-monitoring-system.git
cd secure-file-transfer-monitoring-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Optional: Install the package:
```bash
pip install -e .
```

## Usage

### Basic Usage

```python
from file_monitor import FileMonitor

monitor = FileMonitor()
monitor.start(['/home/user/Documents'])

try:
    while True:
        import time
        time.sleep(1)
except KeyboardInterrupt:
    monitor.stop()
```

### Configuration

Edit `config.py` to customize:
- Sensitive file paths to monitor
- Alert thresholds
- Excluded directories
- Monitoring settings
- Email and database options

## Project Structure

```
secure-file-transfer-monitoring-system/
├── file_monitor.py          # Main monitoring module
├── integrity_checker.py      # File hash verification
├── alert_system.py           # Alert generation and management
├── config.py                 # Configuration settings
├── requirements.txt          # Project dependencies
├── setup.py                  # Installation script
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## Core Modules

### file_monitor.py
Main module that handles filesystem event monitoring using the watchdog library. Detects and processes file events (create, modify, move, delete).

### integrity_checker.py
Provides file integrity checking using SHA256/MD5 hashing. Features include:
- Hash calculation with configurable algorithms
- Hash caching for performance
- Integrity verification
- Report generation

### alert_system.py
Manages security alert generation and tracking. Includes:
- Alert creation with severity levels
- Threshold-based escalation
- Alert logging to file
- Alert summary statistics

### config.py
Centralized configuration for:
- Sensitive file paths
- Excluded directories
- Logging settings
- Alert thresholds
- Email notifications (optional)
- Database settings (optional)

## Security Techniques Implemented

- **File System Activity Monitoring**: Real-time detection of file operations
- **Tamper Detection**: Hash comparison to identify file modifications
- **Unauthorized Access Alerting**: Detection of suspicious file access patterns
- **Data Movement Tracking**: Monitoring transfers to external devices and cloud storage

## Learning Outcomes

This project teaches:
- Filesystem event handling and monitoring
- Data loss prevention (DLP) concepts
- Hash-based file integrity verification
- Blue Team defensive security practices
- Real-world file auditing techniques
- Secure logging and alert generation

## Requirements

- watchdog==3.0.0 - Filesystem event monitoring
- psutil==5.9.6 - Process tracking (optional)
- python-json-logger==2.0.7 - JSON logging

## Future Enhancements

- Email alert notifications
- Database integration for centralized logging
- Web-based dashboard
- Machine learning-based anomaly detection
- Integration with SIEM systems
- Support for cloud storage monitoring

## Author

**Gaurav Malhotra**

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is designed for authorized security monitoring only. Unauthorized monitoring of systems or users may be illegal. Always obtain proper authorization before deploying monitoring solutions.

## References

- Watchdog Documentation: https://watchdog.readthedocs.io/
- OWASP Data Loss Prevention: https://owasp.org/
- Python Security Best Practices: https://python.readthedocs.io/


![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![GitHub Actions](https://github.com/gauravmalhotra3300-hub/secure-file-transfer-monitoring-system/workflows/Python%20CI/CD/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
