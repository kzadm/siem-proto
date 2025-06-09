# siem_core/detector_runner.py

import time
import os

from siem_core.detector import detect_alerts, load_events_from_file

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs.jsonl")

def follow_logs():

    print(f"[*] Monitoring file: {LOG_FILE}")
    while True:
        try:
            events = load_events_from_file(LOG_FILE)
            alert = detect_alerts(events)
            print(alert)
        except FileNotFoundError:
            print(f"[!] Log file not found: {LOG_FILE}")

        time.sleep(1)

if __name__ == "__main__":
    follow_logs()
