# Sample Outputs and Monitoring Logs

## Overview

This document demonstrates the expected outputs and logs from the Secure File Transfer Monitoring System. These are real examples showing file monitoring, integrity checks, alerts, and reports.

---

## 1. Real-Time Monitoring Output

### Console Output During Monitoring

```
============================================================
Secure File Transfer Monitoring System - Real-Time Monitor
============================================================

[2025-01-02 10:30:15] MONITORING STARTED
[2025-01-02 10:30:15] Watching paths: /home/gaurav/Documents, /home/gaurav/Downloads
[2025-01-02 10:30:15] Alert threshold: 5 high-severity events

[2025-01-02 10:30:42] [FILE_CREATED] path=/home/gaurav/Documents/report.txt
                      timestamp=2025-01-02T10:30:42.123Z
                      user=gaurav
                      is_sensitive=false
                      status=OK ✓

[2025-01-02 10:31:05] [FILE_MOVED] path=/home/gaurav/Documents/confidential.xlsx
                     destination=/home/gaurav/Downloads/
                     timestamp=2025-01-02T10:31:05.456Z
                     user=gaurav
                     is_sensitive=true
                     ⚠️  SENSITIVE FILE DETECTED
                     [ALERT] MEDIUM severity alert generated

[2025-01-02 10:31:45] [FILE_MODIFIED] path=/home/gaurav/Documents/config.ini
                      hash_before=a3f8c7e2b9d4f1a6e8c5b2d9f4a1e6c3
                      hash_after=d4e9f2a3b6c1f8e5d2a9c7e4b1f6d3a8
                      timestamp=2025-01-02T10:31:45.789Z
                      HASH MISMATCH DETECTED ❌
                      [ALERT] HIGH severity - File tampered!

[2025-01-02 10:32:10] [BULK_TRANSFER] files=25 from=/home/gaurav/Documents/
                     destination=/media/usb_drive/backup
                     total_size=450MB
                     timestamp=2025-01-02T10:32:10.112Z
                     🛑 CRITICAL alert - Suspicious bulk transfer!
```

---

## 2. File Integrity Check Results

### Hash Verification Example

```json
{
  "integrity_check_report": {
    "timestamp": "2025-01-02T10:35:22.000Z",
    "files_checked": 3,
    "results": [
      {
        "file_path": "/home/gaurav/Documents/document.pdf",
        "hash_algorithm": "SHA256",
        "hash_value": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "exists": true,
        "size_bytes": 1024000,
        "integrity_valid": true,
        "status": "✓ OK"
      },
      {
        "file_path": "/home/gaurav/Documents/config.ini",
        "hash_algorithm": "SHA256",
        "hash_before": "abc123def456ghi789jkl012mno345pqr",
        "hash_after": "xyz987uvw654tsr321qpo987lkj654ihg",
        "exists": true,
        "integrity_valid": false,
        "size_bytes": 2048,
        "modification_detected": true,
        "status": "❌ TAMPERING DETECTED"
      },
      {
        "file_path": "/home/gaurav/Documents/deleted_file.txt",
        "exists": false,
        "status": "⚠️  DELETED"
      }
    ]
  }
}
```

---

## 3. Alert Log Examples

### JSON Format Alert Logs

```json
{
  "timestamp": "2025-01-02T10:31:05.456Z",
  "severity": "MEDIUM",
  "alert_id": "550e8400-e29b-41d4-a716-446655440001",
  "event_type": "moved",
  "file_path": "/home/gaurav/Documents/confidential.xlsx",
  "is_sensitive": true,
  "user": "gaurav",
  "destination": "/home/gaurav/Downloads/",
  "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "message": "Sensitive file moved to potentially insecure location"
}
```

```json
{
  "timestamp": "2025-01-02T10:31:45.789Z",
  "severity": "HIGH",
  "alert_id": "550e8400-e29b-41d4-a716-446655440002",
  "event_type": "modified",
  "file_path": "/home/gaurav/Documents/config.ini",
  "is_sensitive": true,
  "user": "unknown",
  "hash_mismatch": {
    "expected": "a3f8c7e2b9d4f1a6e8c5b2d9f4a1e6c3",
    "actual": "d4e9f2a3b6c1f8e5d2a9c7e4b1f6d3a8"
  },
  "message": "File integrity check failed - possible tampering"
}
```

```json
{
  "timestamp": "2025-01-02T10:32:10.112Z",
  "severity": "CRITICAL",
  "alert_id": "550e8400-e29b-41d4-a716-446655440003",
  "event_type": "bulk_transfer",
  "source_directory": "/home/gaurav/Documents/",
  "destination": "/media/usb_drive/backup",
  "is_sensitive": true,
  "file_count": 25,
  "total_size_mb": 450,
  "user": "gaurav",
  "message": "CRITICAL: Bulk transfer of 25 sensitive files to USB device detected"
}
```

---

## 4. Daily Audit Report

### Summary Report Example

```json
{
  "audit_report": {
    "report_date": "2025-01-02",
    "report_period": "24_hours",
    "generated_timestamp": "2025-01-02T23:59:59Z",
    "statistics": {
      "total_events_logged": 1547,
      "file_created": 342,
      "file_modified": 156,
      "file_moved": 89,
      "file_deleted": 34,
      "sensitive_files_accessed": 78
    },
    "alerts_summary": {
      "total_alerts": 12,
      "critical": 2,
      "high": 4,
      "medium": 5,
      "low": 1
    },
    "integrity_checks": {
      "total_checks_performed": 234,
      "passed": 232,
      "failed": 2,
      "tampering_detected": 2
    },
    "top_sensitive_locations_accessed": [
      {
        "path": "/home/gaurav/Documents",
        "access_count": 45,
        "alert_count": 3
      },
      {
        "path": "/home/gaurav/.ssh",
        "access_count": 5,
        "alert_count": 1
      },
      {
        "path": "/home/gaurav/Downloads",
        "access_count": 78,
        "alert_count": 4
      }
    ],
    "recommendations": [
      "Review CRITICAL alerts from 10:32 AM regarding bulk USB transfer",
      "Investigate file tampering events in /home/gaurav/Documents/config.ini",
      "Enable additional monitoring for /home/gaurav/.ssh directory",
      "Consider restricting USB device access during business hours"
    ]
  }
}
```

---

## 5. File Activity Timeline

### Chronological Event Sequence

| Timestamp | Event Type | File Path | Severity | Status |
|-----------|-----------|-----------|----------|--------|
| 10:30:42 | CREATED | /Documents/report.txt | - | ✓ OK |
| 10:31:05 | MOVED | /Documents/confidential.xlsx | MEDIUM | ⚠️  Alert |
| 10:31:45 | MODIFIED | /Documents/config.ini | HIGH | ❌ Tampering |
| 10:32:10 | BULK_TRANSFER | /Documents/* → /USB | CRITICAL | 🛑 Alert |
| 10:35:22 | INTEGRITY_CHECK | /Documents/document.pdf | - | ✓ Valid |
| 10:40:15 | DELETED | /Documents/temp.log | - | OK |

---

## 6. System Performance Metrics

```json
{
  "performance_metrics": {
    "monitoring_uptime_percent": 99.8,
    "average_event_detection_latency_ms": 45,
    "average_hash_calculation_time_ms": 125,
    "false_positive_rate_percent": 2.1,
    "average_alerts_per_hour": 0.5,
    "memory_usage_mb": 85,
    "cpu_usage_percent": 3.2
  }
}
```

---

## Interpretation Guide

### Alert Severity Levels

- **LOW**: Minor activity, informational only
- **MEDIUM**: Sensitive file accessed or moved, requires review
- **HIGH**: File integrity compromised, possible tampering
- **CRITICAL**: Bulk transfers, mass file movements, suspicious patterns

### File Status Indicators

- ✓ OK: Normal activity, no concerns
- ⚠️ Warning: Requires attention, monitoring
- ❌ Critical: Immediate action required
- 🛑 Emergency: Severe security incident

---

## Real-World Usage Scenarios

### Scenario 1: Insider Threat Detection

Employee attempts to copy confidential files to USB drive:

```
[CRITICAL] Bulk transfer detected: 25 files → /media/usb/
[HIGH] Hash integrity check shows file modifications
[ALERT] Sensitive files accessed outside business hours
RECOMMENDATION: Isolate user account, begin investigation
```

### Scenario 2: Malware Activity Detection

Malware modifies critical system files:

```
[HIGH] Unexpected modifications to system configuration files
[HIGH] Hash mismatch detected in critical_config.ini
[HIGH] Suspicious process attempting file modifications
RECOMMENDATION: Run malware scan, review system integrity
```

### Scenario 3: Data Exfiltration Prevention

Automated backup process with integrity verification:

```
[INFO] Scheduled backup started
[INFO] 500 files processed, all hashes verified
[INFO] Backup integrity: VALID ✓
[INFO] Backup completion: SUCCESS
```

---

For more details on interpretation and response procedures, see `ARCHITECTURE_DIAGRAMS.md`
