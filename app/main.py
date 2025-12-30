from ingestion import tail_log
from window import TimeWindow
from analyzer import detect_anomaly, should_alert
from state import AnalyzerState
from alert import send_alert
from config import LOG_FILE_PATH, WINDOW_SIZE_SECONDS, BASELINE_WINDOWS

def main():
    try:
        window = TimeWindow(WINDOW_SIZE_SECONDS)
        state = AnalyzerState(BASELINE_WINDOWS)

        for log_line in tail_log(LOG_FILE_PATH):
            window.add_log(log_line)

            if window.is_expired():
                metrics = window.summary()

                if detect_anomaly(metrics, state) and should_alert(state):
                    send_alert(
                        f"Log anomaly detected: {metrics}",
                        state
                    )

                state.update_baseline(metrics.get("error_count", 0))
                window.reset()
    except KeyboardInterrupt:
        print("Shutting down log analyzer gracefully.")


if __name__ == "__main__":
    main()
