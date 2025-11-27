"""
This sources handle, face detection via dlib and resize and greyscale conversion (for easier results)
"""
import cv2 
import difflib
from config import FRAME_WIDTH
import dlib 

class videosource:
    #webcam initilization and frame fetching
    def __init__(self, source = None, video_path = None):
        if video_path:
            self.cap = cv2.VideoCapture(video_path)
        else:
            cam_index = source if source else 0
            self.cap = cv2.VideoCapture(cam_index)
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps is None or self.fps ==0:
            self.fps = 25.0
    
    def read_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        h,w = frame.shape[:2]
        scale = FRAME_WIDTH/ float(w)
        frame = cv2.resize(frame, (FRAME_WIDTH, int(h*scale)))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame, gray
    
    def release(self):
        self.cap.release()


class facedetector: 
    # frontal face detection using dlib
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()

    def detect_face(self, gray):
        # detects face in grayscale
        rects = self.detector(gray, 0)
        return rects


