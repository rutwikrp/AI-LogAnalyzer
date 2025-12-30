import requests
import time
from config import ALERT_WEBHOOK_URL

def send_alert(message, state):
    if not ALERT_WEBHOOK_URL:
        return

    payload = {"text": message}
    requests.post(ALERT_WEBHOOK_URL, json=payload)

    state.last_alert_time = time.time()
