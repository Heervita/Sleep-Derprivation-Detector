# perclos.py

import time
from collections import deque
from config import PERCLOS_WINDOW, EAR_THRESHOLD, CONSEC_FRAMES

class PERCLOSCalculator:

    def __init__(self, window_seconds=PERCLOS_WINDOW, ear_threshold=EAR_THRESHOLD):
        self.window_seconds = window_seconds
        self.ear_threshold = ear_threshold

        # Stores tuples: (timestamp, closed_flag)
        self.history = deque()

        # For blink/closure logic
        self.consec_closed = 0
        self.blink_count = 0

    def update(self, ear_value):
        now_ts = time.time()

        # Determine if eyes are closed in this frame
        closed_flag = 1 if ear_value < self.ear_threshold else 0

        # Blink/closure logic
        if closed_flag:
            self.consec_closed += 1
        else:
            if self.consec_closed >= CONSEC_FRAMES:
                self.blink_count += 1
            self.consec_closed = 0

        # Add current frame to history
        self.history.append((now_ts, closed_flag))

        # Remove entries older than window_seconds
        cutoff = now_ts - self.window_seconds
        while self.history and self.history[0][0] < cutoff:
            self.history.popleft()

        # Compute PERCLOS
        total = len(self.history)
        if total == 0:
            perclos = 0.0
        else:
            closed_total = sum(flag for (_, flag) in self.history)
            perclos = closed_total / total

        # Compute sleep score (0-100%)
        sleep_score = perclos * 100.0

        # Determine fatigue classification
        if perclos < 0.20:
            label = "ALERT"
        elif perclos < 0.35:
            label = "MILD"
        else:
            label = "HIGH"

        return {
            "perclos": perclos,
            "closed_flag": closed_flag,
            "blink_count": self.blink_count,
            "sleep_score": sleep_score,
            "label": label
        }
