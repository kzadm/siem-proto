from django.shortcuts import render
from .detector import load_events_from_file, detect_alerts
import os, json
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "logs.jsonl")

def dashboard(request):
    log_path = os.path.join(os.path.dirname(__file__), 'logs.jsonl')
    raw_events = load_events_from_file(log_path)
    alerts = detect_alerts(raw_events)
    return render(request, "dashboard.html", {"alerts": alerts})


def add_event_view(request):
    success = False
    if request.method == "POST":
        event = {
            "time": request.POST.get("time"),
            "src": request.POST.get("src"),
            "event_type": request.POST.get("event_type"),
            "msg": request.POST.get("msg"),
        }
        try:
            with open(LOG_FILE, "a") as f:
                f.write(json.dumps(event) + "\n")
            success = True
        except Exception as e:
            print(f"[!] Failed to write event: {e}")

    context = {
        "success": success,
        "now": datetime.utcnow().isoformat()
    }
    return render(request, "siem_core/add_event.html", context)