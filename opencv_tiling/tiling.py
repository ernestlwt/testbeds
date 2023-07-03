import cv2
from datetime import datetime

from videocapture import VideoCapture

CAMERA_URLS = [
    "rtsp://localhost:8554/mystream"
]

def print_error_message(url, timestamp):
    error_msg = timestamp + ": Unable to connect to Camera " + url
    print(error_msg)

def get_frame_from_cam_list(list_of_cap):
    

video_cap_list = []

for url in CAMERA_URLS:
    cap = VideoCapture(url, print_error_message)
    cap.start()

    video_cap_list.append(cap)


