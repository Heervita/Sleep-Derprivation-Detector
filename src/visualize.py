# visualize.py
import cv2
from config import (
    COLOR_TEXT,
    COLOR_ALERT,
    COLOR_WARNING,
    COLOR_OK,
    CONTOUR_THICKNESS,
)
from utils import format_number


def draw_eye_contours(frame, left_eye, right_eye):
    import numpy as np  # local import

    left_hull = cv2.convexHull(left_eye)
    right_hull = cv2.convexHull(right_eye)

    cv2.drawContours(frame, [left_hull], -1, COLOR_OK, CONTOUR_THICKNESS)
    cv2.drawContours(frame, [right_hull], -1, COLOR_OK, CONTOUR_THICKNESS)



def draw_metrics(frame, ear, perclos, sleep_score, label, blink_count):
    cv2.putText(frame, f"EAR: {format_number(ear)}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 2)

    cv2.putText(frame, f"PERCLOS: {format_number(perclos)}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 2)

    cv2.putText(frame, f"SleepScore: {format_number(sleep_score)}", (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 2)

    # Fatigue label with color
    color = COLOR_OK
    if label == "MILD":
        color = COLOR_WARNING
    elif label == "HIGH":
        color = COLOR_ALERT

    cv2.putText(frame, f"Label: {label}", (10, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.putText(frame, f"Blinks: {blink_count}", (10, 135),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXT, 2)



def draw_perclos_bar(frame, perclos):
    height = frame.shape[0]
    bar_x, bar_y = 10, height - 40

    # Background
    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + 200, bar_y + 20), (60, 60, 60), -1)

    # Fill according to PERCLOS
    fill_w = int(perclos * 200)

    color = COLOR_OK
    if perclos >= 0.35:
        color = COLOR_ALERT
    elif perclos >= 0.20:
        color = COLOR_WARNING

    cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + 20), color, -1)

    cv2.putText(frame, "PERCLOS", (bar_x + 210, bar_y + 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_TEXT, 1)



def render_all(frame, ear, perclos, sleep_score, label, blink_count,
               left_eye=None, right_eye=None):
    # Optional: contours
    if left_eye is not None and right_eye is not None:
        draw_eye_contours(frame, left_eye, right_eye)

    # Metrics
    draw_metrics(frame, ear, perclos, sleep_score, label, blink_count)

    # PERCLOS bar
    draw_perclos_bar(frame, perclos)

    return frame