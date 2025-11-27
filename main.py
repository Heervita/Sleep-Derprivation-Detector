#!/usr/bin/env python3

import argparse
import time
from datetime import datetime

import cv2

from config import CSV_LOG_PATH, LANDMARK_MODEL_PATH, FRAME_WIDTH
from src.detector import videosource, facedetector
from src.landmark import LandmarkDetector
from src.ear_calc import compute_average_ear
from src.perclos import PERCLOSCalculator
from src.visualize import render_all
from utils import append_to_csv, ensure_directory, get_timestamp


def parse_args():
    ap = argparse.ArgumentParser(description="Sleep-Deprivation Detector (EAR + PERCLOS)")
    ap.add_argument("--video", type=str, default=None, help="Path to video file (optional)")
    ap.add_argument("--source", type=int, default=None, help="Camera source index (optional)")
    ap.add_argument("--log", type=str, default=CSV_LOG_PATH, help="CSV log file path")
    ap.add_argument("--no-display", action="store_true", help="Run without displaying the video window")
    return ap.parse_args()


def main():
    args = parse_args()

    # Prepare logging
    log_path = args.log
    ensure_directory("/".join(log_path.split("/")[:-1]) or "./")
    header = ["timestamp", "frame_index", "ear", "closed_flag", "perclos", "sleep_score", "blink_count"]

    # Initialize modules
    src = VideoSource(source=args.source, video_path=args.video)
    face_detector = FaceDetector()
    landmark_detector = LandmarkDetector(model_path=LANDMARK_MODEL_PATH)
    perclos_calc = PERCLOSCalculator()

    frame_idx = 0
    print("[INFO] Starting detection. Press 'q' to quit.")

    while True:
        frame, gray = src.read_frame()
        if frame is None:
            print("[INFO] No more frames or cannot read frame. Exiting.")
            break

        frame_idx += 1

        # Detect faces
        rects = face_detector.detect_faces(gray)

        ear_avg = 0.0
        left_eye = None
        right_eye = None

        # process first face only (for simplicity)
        if len(rects) > 0:
            rect = rects[0]
            landmarks = landmark_detector.get_landmarks(gray, rect)
            left_eye, right_eye = landmark_detector.extract_eye_regions(landmarks)

            ear_avg = compute_average_ear(left_eye, right_eye)

        # Update PERCLOS calculator
        results = perclos_calc.update(ear_avg)

        # Render overlays
        display_frame = frame.copy()
        display_frame = render_all(display_frame, ear_avg, results["perclos"], results["sleep_score"],
                                   results["label"], results["blink_count"],
                                   left_eye=left_eye, right_eye=right_eye)

        # Show window unless disabled
        if not args.no_display:
            cv2.imshow("Sleep Deprivation (EAR + PERCLOS)", display_frame)

        # Log to CSV
        try:
            append_to_csv(log_path, [datetime.now().isoformat(), frame_idx, f"{ear_avg:.4f}",
                                     results["closed_flag"], f"{results['perclos']:.4f}",
                                     f"{results['sleep_score']:.2f}", results["blink_count"]], header=header)
        except Exception as e:
            # don't crash if logging fails
            print(f"[WARN] Failed to write log: {e}")

        # Keyboard control
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    src.release()
    cv2.destroyAllWindows()
    print("[INFO] Finished. Log saved to:", log_path)


if __name__ == '__main__':
    main()
