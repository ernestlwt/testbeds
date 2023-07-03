import threading
import cv2
import time
from datetime import datetime, timedelta

class VideoCapture:
    def __init__(self, url, error_message_callback, file_fps=10, reconnect_retry_interval=1, reconnect_max_retry_time=10):
        self.url = url
        self.file_fps = file_fps
        self.cap = cv2.VideoCapture(self.url)
        self.reconnect_retry_interval = reconnect_retry_interval
        self.reconnect_max_retry_time = reconnect_max_retry_time
        self.send_error_message = error_message_callback

        self.url_is_video = url[0] == "/"


    def start(self):
        self.stopped = False

        self.t = threading.Thread(target=self._grabber)
        self.t.daemon  = True
        self.t.start()

    def _grabber(self):
        while not self.stopped:
            ret = self.cap.grab()
            if not ret:
                print("Unable to grab frames. Attempting reconnect")
                self.reconnect_start()
                break
            else:
                if self.url_is_video:
                    time.sleep(1/self.file_fps)
    
    def reconnect_start(self):
        s = threading.Thread(target=self.reconnect, args=())
        s.start()

    def reconnect(self):
        if self.cap:
            print("Releasing previous stream")
            self.cap.release()
        start_reconnect_time = datetime.now()
        while not self.cap.isOpened():
            if datetime.now() - start_reconnect_time > timedelta(seconds=self.reconnect_max_retry_time):
                print("Reconnect Failed")
                self.send_error_message(self.url, datetime.now())
                return
            print("Attempting reconnect...")
            self.cap = cv2.VideoCapture(self.url)
            time.sleep(self.reconnect_retry_interval)
        
        self.start()

    def read(self):
        return self.cap.retrieve()

    def stop(self):
        self.stopped = True