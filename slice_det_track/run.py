import cv2
import numpy as np
import torch

from sahi_processor.sahi_processor import SAHIProcessor
from ultralytics import YOLO
from boxmot import BYTETracker

sahi = SAHIProcessor(sahi_slice_width=640, sahi_slice_height=640, sahi_postprocess_class_agnostic=False)
model = YOLO('yolov8n.pt')
tracker = BYTETracker()

cap = cv2.VideoCapture("data/people_walking.mp4")

while True:
    ret, frame = cap.read()

    # check that there are still frames
    if not ret:
        print("No more video")
        break

    # slice image
    batched_images = sahi.get_slice_batches([frame], model_batchsize=16)
    # run inference
    bbox_results = []
    for b in batched_images:
        tensors = [torch.from_numpy(frame).permute(2, 0, 1).float() for frame in b]
        tensor_batch = torch.stack(tensors)
        tensor_batch /= 255.0 # optional
        results = model.predict(tensor_batch, classes=[0]) # only for people

        # add results to list
        for r in results:
            bboxes = r.boxes.xyxy.tolist()
            confs = r.boxes.conf.tolist()
            labels = r.boxes.cls.tolist()

            r_bboxes = []
            for bbox, conf, label in zip(bboxes, confs, labels):
                x1, y1, x2, y2 = bbox
                r_bboxes.append([x1, y1, x2, y2, conf, int(label)])
            bbox_results.append(r_bboxes)

    # merge inference
    merged_results = sahi.run_sahi_algo([frame], bbox_results)

    tracks = tracker.update(np.array(merged_results[0]), frame)

    # draw box
    tracker.plot_results(frame, show_trajectories=True)
    cv2.imshow('frame', frame)

    # exit
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()