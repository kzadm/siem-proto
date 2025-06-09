import json
import os
import hashlib
from datetime import datetime, timedelta

from .telegram_notify import send_telegram_alert

FAILED_LOGINS = {}
ALERT_CACHE_FILE = os.path.join(os.path.dirname(__file__), ".alert_cache")
SENT_ALERT_HASHES = set()

def get_alert_hash(alert: dict) -> str:
    payload = f"{alert['timestamp']}-{alert['source_ip']}-{alert['event_type']}-{alert['alert']}"
    return hashlib.sha256(payload.encode()).hexdigest()

def load_alert_cache():
    if not os.path.exists(ALERT_CACHE_FILE):
        return set()
    with open(ALERT_CACHE_FILE, "r") as f:
        return set(line.strip() for line in f if line.strip())

def save_alert_hash(alert_hash: str):
    with open(ALERT_CACHE_FILE, "a") as f:
        f.write(alert_hash + "\n")

def load_events_from_file(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

def detect_alerts(events):
    global SENT_ALERT_HASHES
    SENT_ALERT_HASHES = load_alert_cache()

    alerts = []

    for event in events:
        try:
            timestamp = datetime.fromisoformat(event.get("time"))
        except Exception:
            continue

        source_ip = event.get("src")
        msg = event.get("msg", "").lower()
        event_type = event.get("event_type", "")
        alert_level = "info"
        alert_message = ""

        if "root login" in msg:
            alert_level = "critical"
            alert_message = "Root login detected"

        elif event_type == "failed_login":
            now = timestamp
            FAILED_LOGINS.setdefault(source_ip, []).append(now)
            recent = [t for t in FAILED_LOGINS[source_ip] if now - t <= timedelta(minutes=1)]
            FAILED_LOGINS[source_ip] = recent

            if len(recent) > 5:
                alert_level = "warning"
                alert_message = f"Brute-force attack suspected from {source_ip}"

        elif any(keyword in msg for keyword in ("attack", "scan", "exploit", "malware")):
            alert_level = "notice"
            alert_message = "Suspicious keyword in message"

        if alert_message:
            alert = {
                "timestamp": timestamp.isoformat(),
                "source_ip": source_ip,
                "event_type": event_type,
                "message": msg,
                "level": alert_level,
                "alert": alert_message
            }

            alert_hash = get_alert_hash(alert)
            if alert_hash not in SENT_ALERT_HASHES:
                send_telegram_alert(alert)
                save_alert_hash(alert_hash)
                SENT_ALERT_HASHES.add(alert_hash)
                print(f"[+] Alert sent: {alert['alert']}")
            else:
                print(f"[-] Skipping duplicate alert: {alert['alert']}")

            alerts.append(alert)

    return alerts
