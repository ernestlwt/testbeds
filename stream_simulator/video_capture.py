import cv2
import threading

class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.t = threading.Thread(target=self._reader)
        self.t.daemon  = True
        self.t.start()

    def _reader(self):
        while True:
            ret = self.cap.grab()
            if not ret:
                break
    
    def read(self):
        _, frame = self.cap.retrieve()
        return frame

    def isOpened(self):
        return self.cap.isOpened()