import cv2
from datetime import datetime

cap = cv2.VideoCapture("rtsp://localhost:8554/mystream")

prev_time = datetime.now()
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    current_time = datetime.now()
    time_taken = current_time - prev_time
    fps = 1/time_taken.total_seconds()
    prev_time = current_time
    print(fps)


    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
