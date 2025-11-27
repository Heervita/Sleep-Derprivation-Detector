# landmarks.py
"""
Facial Landmark Extraction Module
--------------------------------
This module:
- Loads the 68-point facial landmark predictor
- Converts detections into NumPy arrays
- Extracts left-eye and right-eye landmark coordinates

Used for EAR calculation.
"""

import dlib
import numpy as np
from imutils import face_utils
from config import LANDMARK_MODEL_PATH


class LandmarkDetector:
    """
    Wraps dlib's shape predictor for extracting facial landmarks.
    """

    def __init__(self, model_path=LANDMARK_MODEL_PATH):
        self.predictor = dlib.shape_predictor(model_path)

        # Landmark index slices for left/right eye
        (self.l_start, self.l_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.r_start, self.r_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def get_landmarks(self, gray_frame, face_rect):
        """
        Extract all 68 facial landmarks.

        Parameters
        ----------
        gray_frame : numpy array
            Grayscale input image.
        face_rect : dlib rectangle
            Detected face bounding box.

        Returns
        -------
        numpy array of shape (68, 2)
            All landmark points.
        """
        shape = self.predictor(gray_frame, face_rect)
        shape_np = face_utils.shape_to_np(shape)
        return shape_np

    def extract_eye_regions(self, landmarks):
        """
        Extract 6 landmark points for left and right eyes.

        Parameters
        ----------
        landmarks : numpy array (68, 2)

        Returns
        -------
        left_eye : (6, 2) array
        right_eye : (6, 2) array
        """
        left_eye = landmarks[self.l_start:self.l_end]
        right_eye = landmarks[self.r_start:self.r_end]
        return left_eye, right_eye
