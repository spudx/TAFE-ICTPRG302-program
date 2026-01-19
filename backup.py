#!/usr/bin/env python3
"""
backup.py
Harvy Burgess
v1.0

Performs full backups of files or directories based on a
backup job defined in backupcfg.py.

E.g.
    python backup.py <job_name>
"""

import sys
import os
import shutil
import datetime
import traceback

import backupcfg

#log successfull backup
def log_message(message):

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(backupcfg.LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} - {message}\n")

import smtplib
from email.message import EmailMessage


# send smtp email alert function
def send_alert(job_name, error_message):

#define email content
    try:
        msg = EmailMessage()
        msg["From"] = backupcfg.EMAIL_FROM
        msg["To"] = backupcfg.EMAIL_TO
        msg["Subject"] = f"BACKUP FAILED: {job_name}"

        msg.set_content(
            f"Backup job failed\n\n"
            f"Job name: {job_name}\n"
            f"Time: {datetime.datetime.now()}\n"
            f"Error: {error_message}"
        )
# send email
        with smtplib.SMTP(backupcfg.SMTP_SERVER, backupcfg.SMTP_PORT) as server:
            server.starttls()
            server.login(
                backupcfg.SMTP_USERNAME,
                backupcfg.SMTP_PASSWORD
            )
            server.send_message(msg)

    except Exception as exc:
        # log if email fails
        log_message(f"FAIL - Email alert failed: {exc}")

# perform backup function definition
def perform_backup(job_name, source, destination):
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"{os.path.basename(source)}-{timestamp}"
    backup_path = os.path.join(destination, backup_name)

    if os.path.isfile(source):
        shutil.copy2(source, backup_path)
    elif os.path.isdir(source):
        shutil.copytree(source, backup_path)
    else:
        raise FileNotFoundError("Source path is not a file or directory")


def main():

   # Main function to execute the backup job

    if len(sys.argv) != 2:
        error_msg = "No backup job name provided"
        log_message(f"FAIL - {error_msg}")
        send_alert("UNKNOWN", error_msg)
        return 1

    job_name = sys.argv[1]
# check for job name
    if job_name not in backupcfg.BACKUP_JOBS:
        error_msg = f"Backup job '{job_name}' not found in configuration"
        log_message(f"FAIL - {error_msg}")
        send_alert(job_name, error_msg)
        return 1

    job = backupcfg.BACKUP_JOBS[job_name]
    source = job.get("source")
    destination = job.get("destination")
# confirm sourece and destination exist
    try:
        if not os.path.exists(source):
            raise FileNotFoundError("Source path does not exist")

        if not os.path.exists(destination):
            raise FileNotFoundError("Destination path does not exist")
# perform backup
        perform_backup(job_name, source, destination)

        log_message(f"SUCCESS - Backup job '{job_name}' completed successfully")
        return 0

    except Exception as exc:
        error_details = f"{exc}"
        log_message(f"FAIL - Backup job '{job_name}' failed: {error_details}")
        send_alert(job_name, error_details)
        return 1


if __name__ == "__main__":
    sys.exit(main())
