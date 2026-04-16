# Depth Estimator

Testing Depth-Anything-3 with an object detector

## Video and Image distance estimation

`detect_and_estimate_depth.py` runs an Ultralytics detector on each frame of a video or a directory of images, optionally filters detections to only the classes you care about, then estimates the distance of each target with Depth Anything 3.

Outputs:

- Annotated MP4 with boxes and estimated distance labels
- Annotated images directory (for image folder input)
- CSV file with one row per detection

Example:

```bash
python detect_and_estimate_depth.py \
  --video /workspace/input/example.mp4 \
  --detector-model yolo11n.pt \
  --classes person car \
  --output-dir /workspace/output
```

Notes:

- The default depth checkpoint is `depth-anything/DA3NESTED-GIANT-LARGE-1.1`, which the official docs describe as already producing metric depth in meters.
- Distance for each detection is computed as the median depth inside the center region of the bounding box, which is usually more stable than using the full box.
- The first run will download model weights if they are not already cached.
