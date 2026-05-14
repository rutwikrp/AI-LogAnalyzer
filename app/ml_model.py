from sklearn.ensemble import IsolationForest
import numpy as np


class MLAnomalyDetector:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.trained = False

    def train(self, data):
        """
        data: list of error counts
        """
        if len(data) < 5:
            return  # not enough data

        X = np.array(data).reshape(-1, 1)
        self.model.fit(X)
        self.trained = True

    def predict(self, value):
        """
        value: current error count
        """
        if not self.trained:
            return 1  # treat as normal

        X = np.array([[value]])
        return self.model.predict(X)[0]  # 1 or -1