"""
backupcfg.py
Configuration file for backup.py

Defines backup jobs and logging settings
"""

# SMTP config
SMTP_SERVER = "mail.smtp2go.com"
SMTP_PORT = 587
SMTP_USERNAME = "temp-tafe-project"
SMTP_PASSWORD = "00oVvb3MyWrBF26j"

EMAIL_FROM = "alert@burgesss.com.au"
EMAIL_TO = "harvy@burgesss.com.au"


# Path to the log file
LOG_FILE = "backup.log"

BACKUP_JOBS = {
    "job1": {
        "source": "test",
        "destination": "backup"
    },
    "job2": {
        "source": "test",
        "destination": "testdir2"
    },
    "job3": {
        "source": "null",
        "destination": "backup"
    }
}
