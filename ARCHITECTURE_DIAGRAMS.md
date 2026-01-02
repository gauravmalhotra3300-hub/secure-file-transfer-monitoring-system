# Architecture Diagrams & Flowcharts

## 1. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│              SECURE FILE TRANSFER MONITORING SYSTEM               │
└─────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                     FILE SYSTEM LAYER                            │
│  (User Files, Documents, Downloads, System Directories, USB)    │
└────────────────┬───────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────┐
│            FILE_MONITOR.PY (Watchdog Observer)                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ FileTransferHandler                                     │  │
│  │  - on_created()      ─────┐                            │  │
│  │  - on_modified()     ─────┼──> process_file()          │  │
│  │  - on_moved()        ─────┤     ├─ event detection     │  │
│  │  - on_deleted()      ─────┘     └─ classification       │  │
│  └─────────────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────────────────────┘
                 │
        ┌────────┴────────┬────────────┐
        ▼                 ▼            ▼
┌─────────────────┐ ┌───────────────┐ ┌──────────────┐
│  CONFIG.PY      │ │INTEGRITY_     │ │ ALERT_SYSTEM │
│                 │ │CHECKER.PY     │ │    .PY       │
│  Sensitive      │ │               │ │              │
│  Paths List     │ │ - SHA256 Hash │ │  - Alert     │
│  Thresholds     │ │ - MD5 Hash    │ │    Generation│
│  Exclusions     │ │ - Integrity   │ │  - Logging   │
│  Monitoring     │ │   Verification│ │  - Severity  │
│  Settings       │ │ - Caching     │ │    Levels    │
└─────────────────┘ └───────────────┘ └──────────────┘
        │                 │                  │
        └────────┬────────┴──────────┬───────┘
                 ▼
┌────────────────────────────────────────────────────────────────┐
│                    LOGGING & STORAGE                            │
│  ┌──────────────────┐    ┌──────────────────┐                │
│  │  LOG FILES       │    │  ALERT LOGS      │                │
│  │  - file_monitor  │    │  - alerts.log    │                │
│  │  .log            │    │  - JSON format   │                │
│  │  - Timestamp     │    │  - Alert IDs     │                │
│  │  - Events        │    │  - Severity      │                │
│  └──────────────────┘    └──────────────────┘                │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                │
│  │  AUDIT REPORTS   │    │  JSON REPORTS    │                │
│  │  - Daily Summary │    │  - Machine       │                │
│  │  - Statistics    │    │    Readable      │                │
│  │  - Alerts        │    │  - Parseable     │                │
│  └──────────────────┘    └──────────────────┘                │
└────────────────────────────────────────────────────────────────┘
```

---

## 2. Module Dependencies

```
TOP LEVEL
    │
    ├── file_monitor.py
    │   ├── imports: watchdog, config, integrity_checker, alert_system
    │   └── provides: FileMonitor class, FileTransferHandler
    │
    ├── test_demo.py
    │   ├── imports: all modules above
    │   └── provides: Demo scenarios with outputs
    │
CORE MODULES
    │
    ├── config.py
    │   ├── provides: Configuration settings, paths, thresholds
    │   └── used by: all other modules
    │
    ├── integrity_checker.py
    │   ├── imports: hashlib, os, logging
    │   ├── provides: IntegrityChecker class
    │   └── used by: file_monitor.py
    │
    └── alert_system.py
        ├── imports: logging, json, uuid
        ├── provides: AlertSystem class
        └── used by: file_monitor.py

DEPENDENCIES
    │
    └── requirements.txt
        ├── watchdog==3.0.0 (main module)
        ├── psutil==5.9.6 (process tracking)
        └── python-json-logger==2.0.7 (JSON logging)
```

---

## 3. Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      FILE SYSTEM EVENT                           │
│    (File Created, Modified, Moved, Deleted, etc.)              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│           WATCHDOG OBSERVER DETECTS EVENT                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ FileTransferHandler::on_created/modified/moved/deleted    │ │
│  └────────────────────────┬─────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────────┐
│              CLASSIFY EVENT                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Check Against SENSITIVE_PATHS in config.py              │ │
│  │ - Is it a sensitive file?                               │ │
│  │ - YES → Proceed  │  NO → Log & Exit                     │ │
│  └────────┬─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────────┐
│            INTEGRITY HASHING (IntegrityChecker)                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Calculate SHA256 hash of file                            │ │
│  │ Compare with baseline (if exists)                        │ │
│  │ - Hash Match? → Continue                                 │ │
│  │ - Hash Mismatch? → TAMPERING DETECTED                    │ │
│  └────────┬─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────────┐
│         AUTHORIZATION CHECK                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Is this action allowed?                                  │ │
│  │ - Normal operation? → Continue                           │ │
│  │ - Suspicious pattern? → Generate Alert                   │ │
│  └────────┬─────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
           │
       ┌───┴───┐
       │       │
       ▼       ▼
    YES         NO
    │           │
    ▼           ▼
┌────────┐  ┌──────────────────────────────────┐
│LOG OK  │  │  ALERT GENERATION                │
└────────┘  │  (AlertSystem)                   │
            │  ┌──────────────────────────────┐│
            │  │ Determine Severity Level     ││
            │  │ - LOW / MEDIUM / HIGH /      ││
            │  │   CRITICAL                   ││
            │  └────────┬─────────────────────┘│
            │           ▼                       │
            │  ┌──────────────────────────────┐│
            │  │ Generate Unique Alert ID     ││
            │  │ Create JSON alert record     ││
            │  │ Log to alerts.log            ││
            │  │ Check against threshold      ││
            │  │ Escalate if needed           ││
            │  └──────────────────────────────┘│
            └──────────────────────────────────┘
                         │
                         ▼
            ┌─────────────────────────────┐
            │  LOGGING & REPORTING        │
            │  - Event logged             │
            │  - Alert stored             │
            │  - Report generated         │
            │  - User notified (optional) │
            └─────────────────────────────┘
```

---

## 4. Alert Generation Workflow

```
╔═══════════════════════════════════════════════════════════════╗
║             ALERT GENERATION WORKFLOW                          ║
╚═══════════════════════════════════════════════════════════════╝

      Event Detected
            │
            ▼
      ┌──────────────┐
      │ Sensitive?   │ ────NO──→ Log Only
      └──────┬───────┘
             │ YES
             ▼
      ┌──────────────┐
      │ Integrity OK?│ ────YES──→ MEDIUM Alert
      └──────┬───────┘
             │ NO
             ▼
      ┌──────────────┐
      │ Bulk Move?   │ ────YES──→ CRITICAL Alert
      └──────┬───────┘
             │ NO
             ▼
      ┌──────────────┐
      │ File Tampered│────YES──→ HIGH Alert
      └──────┬───────┘
             │ NO
             ▼
      Store Alert + Check Threshold
            │
      ┌─────┴─────┐
      ▼           ▼
  Threshold   Threshold
    Not Met      Met (>=5)
      │           │
      ▼           ▼
   Continue    ESCALATE
               ALERT
```

---

## 5. System Components Interaction

```
┌──────────────┐          ┌──────────────────┐
│ File System  │ EVENT    │   Watchdog       │
│  Events      ├─────────→│   Observer       │
└──────────────┘          └────────┬─────────┘
                                   │
                                   ▼
                          ┌─────────────────┐
                          │ File Monitor    │
                          │ (Handler)       │
                          └────────┬────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  ▼                ▼                ▼
             ┌────────┐      ┌──────────┐     ┌────────┐
             │ Config │      │Integrity │     │ Alert  │
             │ Checker│      │ Checker  │     │ System │
             └────────┘      └──────────┘     └────────┘
                  │                │                │
                  └────────────────┼────────────────┘
                                   ▼
                          ┌──────────────────┐
                          │  Logging Module  │
                          │  - JSON logs     │
                          │  - Alert logs    │
                          │  - Reports       │
                          └──────────────────┘
```

---

## 6. Response Workflow

```
CRITICAL ALERT Detected
      │
      ├─→ Immediate Logging
      │
      ├─→ Email Notification (if configured)
      │
      ├─→ Dashboard Update
      │
      ├─→ SIEM Integration (if available)
      │
      └─→ Operator Review
              │
              ├─→ False Positive?
              │   ├─→ Whitelist Entry
              │   └─→ Update Policy
              │
              └─→ Real Threat?
                  ├─→ Isolate System
                  ├─→ Quarantine Files
                  ├─→ Gather Evidence
                  └─→ Begin Investigation
```

---

For implementation details and API documentation, see the source code comments in each module.
