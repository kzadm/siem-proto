import requests

TELEGRAM_TOKEN = "8171062437:AAF0sfGwK2HlyVbMBlRvkoVIMovKh9SfYSE"
CHAT_ID = "201042884"

def send_telegram_alert(alert: dict):
    text = (
        f"[{alert['level'].upper()}] {alert['timestamp']}\n"
        f"Source: {alert['source_ip']}\n"
        f"Type: {alert['event_type']}\n"
        f"Alert: {alert['alert']}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[!] Telegram send error: {e}")