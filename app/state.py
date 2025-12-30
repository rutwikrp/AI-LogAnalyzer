from collections import deque

class AnalyzerState:
    def __init__(self, baseline_size):
        self.error_history = deque(maxlen=baseline_size)
        self.last_alert_time = 0

    def update_baseline(self, error_count):
        self.error_history.append(error_count)

    def baseline_average(self):
        if not self.error_history:
            return 0
        return sum(self.error_history) / len(self.error_history)
