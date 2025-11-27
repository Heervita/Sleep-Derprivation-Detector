"""
This source handles the calculation of EAR (Eye Aspect Ratio) for both eyes.
"""

from scipy.spatial.distance import euclidean
import numpy as np
def eye_aspect_ratio(eye):
    #computing the euclidean distance /EAR for a single eye 

    #vertical distances
    A = euclidean(eye[1], eye[5]) # p2 to p6
    B = euclidean(eye[2], eye[4]) # p3 to p5

    #horizontal distances
    C = euclidean(eye[0], eye[3])

    if C == 0:
        return 0.0
    ear = (A+B)/ (2.0 * C)
    return ear

def compute_average_ear(left_eye, right_eye):
    #Compute average EAR from left and right eye landmarks.

    leftear = eye_aspect_ratio(left_eye)
    rightear = eye_aspect_ratio(right_eye)
    avg_ear = (leftear + rightear) / 2.0
    return avg_ear

