# config.py
EAR_THRESHOLD = 0.21  # adjust during calibration

# to count as a blink/eye-closure
CONSEC_FRAMES = 3

# PERCLOS window size (in seconds)
# Percentage of time (in last X seconds) eyes are closed
PERCLOS_WINDOW = 60

# Frame resize width for faster processing
FRAME_WIDTH = 640


# Thickness for drawing contours
CONTOUR_THICKNESS = 1

# Colors (BGR)
COLOR_TEXT = (255, 255, 255)
COLOR_ALERT = (0, 0, 255)
COLOR_WARNING = (0, 255, 255)
COLOR_OK = (0, 255, 0)

# Path to facial landmarks model (relative path recommended)
LANDMARK_MODEL_PATH = "models/shape_predictor_68_face_landmarks.dat"

# Default CSV log file
CSV_LOG_PATH = "data/logs/sleep_log.csv"
