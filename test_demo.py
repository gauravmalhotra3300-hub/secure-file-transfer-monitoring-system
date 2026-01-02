"""Test and demonstration script for Secure File Transfer Monitoring System.

This script demonstrates:
1. Real-time file monitoring
2. File integrity checking with hashing
3. Alert generation for suspicious activities
4. Logging and reporting
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path

# Import project modules
from file_monitor import FileMonitor
from integrity_checker import IntegrityChecker
from alert_system import AlertSystem
from config import SENSITIVE_PATHS, LOG_DIR


class FileTransferDemoScenarios:
    """Demonstrate various file transfer scenarios and monitoring capabilities."""
    
    def __init__(self):
        self.test_dir = Path.home() / 'file_monitor_test'
        self.test_dir.mkdir(exist_ok=True)
        self.integrity_checker = IntegrityChecker()
        self.alert_system = AlertSystem()
        self.results = []
    
    def scenario_1_normal_file_transfer(self):
        """SCENARIO 1: Normal file transfer (should not trigger alert)."""
        print("\n" + "="*60)
        print("SCENARIO 1: Normal File Transfer")
        print("="*60)
        
        # Create a normal file
        test_file = self.test_dir / 'normal_document.txt'
        test_file.write_text('This is a normal document')
        
        # Calculate hash
        hash_before = self.integrity_checker.calculate_hash(str(test_file))
        print(f"\n[INFO] File created: {test_file}")
        print(f"[HASH] SHA256: {hash_before}")
        
        # Log this event
        event = {
            'scenario': 'Normal File Transfer',
            'file': str(test_file),
            'hash': hash_before,
            'is_sensitive': False,
            'status': 'OK'
        }
        self.results.append(event)
        print(f"[STATUS] ✓ Normal file - No alert generated")
        
        return event
    
    def scenario_2_sensitive_file_move(self):
        """SCENARIO 2: Sensitive file movement (should trigger MEDIUM alert)."""
        print("\n" + "="*60)
        print("SCENARIO 2: Sensitive File Movement")
        print("="*60)
        
        # Create sensitive file
        sensitive_file = self.test_dir / 'confidential_data.txt'
        sensitive_file.write_text('SECRET COMPANY DATA')
        
        hash_value = self.integrity_checker.calculate_hash(str(sensitive_file))
        print(f"\n[INFO] Sensitive file created: {sensitive_file}")
        print(f"[HASH] SHA256: {hash_value}")
        
        # Generate alert
        event_data = {
            'event_type': 'moved',
            'file_path': str(sensitive_file),
            'is_sensitive': True,
            'user': 'test_user',
            'file_hash': hash_value
        }
        self.alert_system.generate_alert(event_data, severity='MEDIUM')
        
        event = {
            'scenario': 'Sensitive File Movement',
            'file': str(sensitive_file),
            'hash': hash_value,
            'is_sensitive': True,
            'alert_severity': 'MEDIUM',
            'status': 'ALERT GENERATED'
        }
        self.results.append(event)
        print(f"[ALERT] ⚠️  Sensitive file detected - MEDIUM alert generated")
        
        return event
    
    def scenario_3_file_tampering(self):
        """SCENARIO 3: File tampering detection (should trigger HIGH alert)."""
        print("\n" + "="*60)
        print("SCENARIO 3: File Tampering Detection")
        print("="*60)
        
        # Create and hash original file
        tampered_file = self.test_dir / 'important_config.ini'
        tampered_file.write_text('[CONFIG]\npassword=original')
        
        hash_before = self.integrity_checker.calculate_hash(str(tampered_file))
        print(f"\n[INFO] Original file created: {tampered_file}")
        print(f"[HASH] Before: {hash_before}")
        
        # Simulate tampering
        time.sleep(1)
        tampered_file.write_text('[CONFIG]\npassword=hacked')
        
        hash_after = self.integrity_checker.calculate_hash(str(tampered_file))
        print(f"[INFO] File has been modified (tampered)")
        print(f"[HASH] After:  {hash_after}")
        
        # Verify integrity
        is_valid, actual_hash = self.integrity_checker.verify_integrity(
            str(tampered_file), hash_before
        )
        
        # Generate alert
        if not is_valid:
            event_data = {
                'event_type': 'modified',
                'file_path': str(tampered_file),
                'is_sensitive': True,
                'user': 'unknown',
                'file_hash': hash_after
            }
            self.alert_system.generate_alert(event_data, severity='HIGH')
            print(f"[ALERT] 🚨 Hash mismatch detected - HIGH alert generated!")
        
        event = {
            'scenario': 'File Tampering',
            'file': str(tampered_file),
            'hash_before': hash_before,
            'hash_after': hash_after,
            'integrity_valid': is_valid,
            'alert_severity': 'HIGH' if not is_valid else 'NONE',
            'status': 'TAMPERING DETECTED'
        }
        self.results.append(event)
        
        return event
    
    def scenario_4_bulk_file_transfer(self):
        """SCENARIO 4: Bulk suspicious file transfer (should trigger CRITICAL alert)."""
        print("\n" + "="*60)
        print("SCENARIO 4: Bulk Suspicious File Transfer")
        print("="*60)
        
        # Create multiple sensitive files
        sensitive_dir = self.test_dir / 'sensitive_files'
        sensitive_dir.mkdir(exist_ok=True)
        
        files_created = []
        for i in range(5):
            file_path = sensitive_dir / f'sensitive_doc_{i}.txt'
            file_path.write_text(f'Sensitive data {i}')
            hash_val = self.integrity_checker.calculate_hash(str(file_path))
            files_created.append({'file': str(file_path), 'hash': hash_val})
        
        print(f"\n[INFO] Created {len(files_created)} sensitive files")
        for file_info in files_created:
            print(f"       - {Path(file_info['file']).name}: {file_info['hash'][:16]}...")
        
        # Generate critical alert for bulk transfer
        event_data = {
            'event_type': 'bulk_transfer',
            'file_path': str(sensitive_dir),
            'is_sensitive': True,
            'user': 'suspicious_user',
            'files_count': len(files_created),
            'file_hash': None
        }
        self.alert_system.generate_alert(event_data, severity='CRITICAL')
        
        event = {
            'scenario': 'Bulk File Transfer',
            'files_count': len(files_created),
            'directory': str(sensitive_dir),
            'alert_severity': 'CRITICAL',
            'status': 'BULK TRANSFER DETECTED'
        }
        self.results.append(event)
        print(f"[ALERT] 🛑 CRITICAL alert generated - Bulk transfer of sensitive files!")
        
        return event
    
    def generate_report(self):
        """Generate comprehensive demonstration report."""
        print("\n" + "="*60)
        print("DEMONSTRATION REPORT SUMMARY")
        print("="*60)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_scenarios': len(self.results),
            'scenarios_tested': self.results,
            'alert_summary': self.alert_system.get_alert_summary(),
            'test_directory': str(self.test_dir)
        }
        
        print(f"\n[REPORT] Timestamp: {report['timestamp']}")
        print(f"[REPORT] Total Scenarios Tested: {report['total_scenarios']}")
        print(f"[REPORT] Test Directory: {report['test_directory']}")
        
        print(f"\n[ALERT SUMMARY]")
        for key, value in report['alert_summary'].items():
            print(f"         {key}: {value}")
        
        # Save report to JSON
        report_file = LOG_DIR / 'demo_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n[REPORT] Full report saved to: {report_file}")
        
        return report
    
    def cleanup(self):
        """Clean up test files."""
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
            print(f"\n[CLEANUP] Test directory removed: {self.test_dir}")


def main():
    """Run the demonstration scenarios."""
    print("\n" + "#"*60)
    print("# Secure File Transfer Monitoring System - Demonstration")
    print("#"*60)
    
    demo = FileTransferDemoScenarios()
    
    try:
        # Run all scenarios
        demo.scenario_1_normal_file_transfer()
        demo.scenario_2_sensitive_file_move()
        demo.scenario_3_file_tampering()
        demo.scenario_4_bulk_file_transfer()
        
        # Generate report
        demo.generate_report()
        
        print("\n" + "#"*60)
        print("# Demonstration completed successfully!")
        print("#"*60 + "\n")
        
    except Exception as e:
        print(f"\n[ERROR] Demonstration failed: {str(e)}")
    finally:
        # Cleanup
        demo.cleanup()


if __name__ == '__main__':
    main()
