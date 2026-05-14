from ingestion import tail_log
from window import TimeWindow
from analyzer import detect_anomaly, should_alert
from state import AnalyzerState
from alert import send_alert
from config import LOG_FILE_PATH, WINDOW_SIZE_SECONDS, BASELINE_WINDOWS
from ml_model import MLAnomalyDetector

def main():
    try:
        print("Log analyzer started", flush=True)
        window = TimeWindow(WINDOW_SIZE_SECONDS)
        state = AnalyzerState(BASELINE_WINDOWS)
        ml_model = MLAnomalyDetector()

        for log_line in tail_log(LOG_FILE_PATH):
            window.add_log(log_line)

            if window.is_expired():
                metrics = window.summary()
                error_count = metrics.get("error_count", 0)

                print(f"Window metrics: {metrics}", flush=True)

                # Train model on historical data
                ml_model.train(list(state.window_history))

                # Predict anomaly
                prediction = ml_model.predict(error_count)

            if prediction == -1:
                print("ML Anomaly detected", flush=True)

            # Existing rule-based logic
            if detect_anomaly(metrics, state) and should_alert(state):
                print("Rule-based anomaly detected", flush=True)
                send_alert(
                    f"Log anomaly detected: {metrics}",
                    state
                )

            state.update_baseline(error_count)
            window.reset()
    except KeyboardInterrupt:
        print("Shutting down log analyzer gracefully.")


if __name__ == "__main__":
    main()
