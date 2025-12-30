import time
from collections import defaultdict

class TimeWindow:
    def __init__(self, duration_seconds):
        self.duration = duration_seconds
        self.start_time = time.time()
        self.logs = []

    def add_log(self, log):
        self.logs.append(log)

    def is_expired(self):
        return time.time() - self.start_time >= self.duration

    def reset(self):
        self.start_time = time.time()
        self.logs = []

    def summary(self):
        """
        Extract metrics for this window
        """
        metrics = defaultdict(int)

        for log in self.logs:
            if "ERROR" in log:
                metrics["error_count"] += 1
            metrics["total_logs"] += 1

        return metrics
