import logging
import json
from datetime import datetime
from config import ALERT_LOG_FILE, ALERT_THRESHOLD


class AlertSystem:
    """Generate and manage security alerts for file transfer violations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alerts = []
        self.severity_levels = {
            'LOW': 1,
            'MEDIUM': 2,
            'HIGH': 3,
            'CRITICAL': 4
        }
    
    def generate_alert(self, event_data, severity='MEDIUM'):
        """Generate an alert for a file transfer event.
        
        Args:
            event_data: Dictionary containing event information
            severity: Alert severity level (LOW, MEDIUM, HIGH, CRITICAL)
        """
        alert = {
            'timestamp': datetime.now().isoformat(),
            'severity': severity,
            'event_type': event_data.get('event_type'),
            'file_path': event_data.get('file_path'),
            'is_sensitive': event_data.get('is_sensitive'),
            'user': event_data.get('user'),
            'file_hash': event_data.get('file_hash'),
            'alert_id': self._generate_alert_id()
        }
        
        self.alerts.append(alert)
        self._log_alert(alert)
        self._check_alert_threshold()
    
    def _generate_alert_id(self):
        """Generate unique alert ID."""
        import uuid
        return str(uuid.uuid4())
    
    def _log_alert(self, alert):
        """Log alert to file and console."""
        alert_msg = json.dumps(alert)
        self.logger.warning(f'SECURITY ALERT: {alert_msg}')
        
        # Write to alert log file
        try:
            with open(ALERT_LOG_FILE, 'a') as f:
                f.write(alert_msg + '\\n')
        except Exception as e:
            self.logger.error(f'Failed to write alert to file: {str(e)}')
    
    def _check_alert_threshold(self):
        """Check if alert threshold is exceeded."""
        high_severity_alerts = [a for a in self.alerts if a['severity'] in ['HIGH', 'CRITICAL']]
        
        if len(high_severity_alerts) >= ALERT_THRESHOLD:
            self._escalate_alert()
    
    def _escalate_alert(self):
        """Escalate alerts when threshold is met."""
        self.logger.critical('ALERT THRESHOLD EXCEEDED - Multiple high-severity events detected')
    
    def get_alert_summary(self):
        """Get summary of recent alerts."""
        summary = {
            'total_alerts': len(self.alerts),
            'critical': len([a for a in self.alerts if a['severity'] == 'CRITICAL']),
            'high': len([a for a in self.alerts if a['severity'] == 'HIGH']),
            'medium': len([a for a in self.alerts if a['severity'] == 'MEDIUM']),
            'low': len([a for a in self.alerts if a['severity'] == 'LOW'])
        }
        return summary
    
    def clear_alerts(self):
        """Clear alert history."""
        self.alerts.clear()
        self.logger.info('Alert history cleared')
    
    def get_recent_alerts(self, count=10):
        """Get most recent alerts.
        
        Args:
            count: Number of recent alerts to retrieve
        
        Returns:
            List of recent alerts
        """
        return self.alerts[-count:] if len(self.alerts) > 0 else []
