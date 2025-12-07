import cv2
import numpy as np

def init_video(path="flood.mp4"):
    cap = cv2.VideoCapture(path)

    # DEBUG PRINTS
    print("Trying to open:", path)
    print("Video opened?", cap.isOpened())

    return cap

def analyze_video_frame(cap):
    ret, frame = cap.read()

    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
        if not ret:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            return frame, "normal"

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    ratio = np.sum(mask > 0) / mask.size

    label = "normal"
    if ratio > 0.10:
        label = "flood"

    return frame, label
