import time
from config import ERROR_SPIKE_MULTIPLIER, ALERT_COOLDOWN_SECONDS

def detect_anomaly(metrics, state):
    current_errors = metrics.get("error_count", 0)
    baseline = state.baseline_average()

    if baseline == 0:
        return False

    return current_errors > baseline * ERROR_SPIKE_MULTIPLIER


def should_alert(state):
    now = time.time()
    return now - state.last_alert_time > ALERT_COOLDOWN_SECONDS
