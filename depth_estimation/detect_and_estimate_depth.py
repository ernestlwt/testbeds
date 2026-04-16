#!/usr/bin/env python3
"""Run YOLO object detection on a video and estimate target distance with DA3."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
import torch
from depth_anything_3.api import DepthAnything3
from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Ultralytics object detection on a video and estimate the "
            "distance of detected targets using Depth Anything 3."
        )
    )
    parser.add_argument(
        "--video",
        required=True,
        help="Path to the input video file or a folder of images.",
    )
    parser.add_argument(
        "--detector-model",
        default="yolo11n.pt",
        help="Ultralytics detector checkpoint or model name.",
    )
    parser.add_argument(
        "--depth-model",
        default="depth-anything/da3metric-large",
        help=(
            "Depth Anything 3 checkpoint or Hugging Face repo. "
            "Defaults to the nested metric model whose output is already in meters."
        ),
    )
    parser.add_argument(
        "--classes",
        nargs="+",
        default=None,
        help=(
            "Optional class filter. Accepts class names, ids, or a mix of both. "
            "Example: --classes person car 2"
        ),
    )
    parser.add_argument(
        "--device",
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Torch device to use for both models.",
    )
    parser.add_argument(
        "--conf-threshold",
        type=float,
        default=0.25,
        help="Minimum detector confidence.",
    )
    parser.add_argument(
        "--iou-threshold",
        type=float,
        default=0.45,
        help="NMS IoU threshold for detector inference.",
    )
    parser.add_argument(
        "--process-res",
        type=int,
        default=504,
        help="Base inference resolution passed to Depth Anything 3.",
    )
    parser.add_argument(
        "--process-res-method",
        default="upper_bound_resize",
        choices=["upper_bound_resize", "lower_bound_resize"],
        help="Resize mode passed to Depth Anything 3.",
    )
    parser.add_argument(
        "--box-inner-ratio",
        type=float,
        default=0.6,
        help=(
            "Fraction of each detection box used for robust depth pooling. "
            "Smaller values focus more on the object center."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory for annotated video and CSV outputs.",
    )
    parser.add_argument(
        "--output-stem",
        default=None,
        help="Optional basename for output files. Defaults to the input video stem.",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Optional limit for debugging on only the first N frames.",
    )
    return parser.parse_args()


def resolve_class_filter(raw_classes: Iterable[str] | None, names: dict[int, str]) -> list[int] | None:
    if not raw_classes:
        return None

    normalized_names = {str(idx): idx for idx in names}
    normalized_names.update({name.lower(): idx for idx, name in names.items()})
    resolved: list[int] = []

    for raw_value in raw_classes:
        key = raw_value.lower()
        if key in normalized_names:
            resolved.append(normalized_names[key])
            continue

        if raw_value.isdigit():
            class_id = int(raw_value)
            if class_id in names:
                resolved.append(class_id)
                continue

        available = ", ".join(f"{idx}:{name}" for idx, name in names.items())
        raise ValueError(f"Unknown class filter '{raw_value}'. Available classes: {available}")

    return sorted(set(resolved))


def center_crop_bounds(x1: int, y1: int, x2: int, y2: int, ratio: float) -> tuple[int, int, int, int]:
    ratio = max(0.05, min(ratio, 1.0))
    width = max(1, x2 - x1)
    height = max(1, y2 - y1)
    inner_w = max(1, int(round(width * ratio)))
    inner_h = max(1, int(round(height * ratio)))
    cx = x1 + width // 2
    cy = y1 + height // 2
    inner_x1 = max(x1, cx - inner_w // 2)
    inner_y1 = max(y1, cy - inner_h // 2)
    inner_x2 = min(x2, inner_x1 + inner_w)
    inner_y2 = min(y2, inner_y1 + inner_h)
    return inner_x1, inner_y1, inner_x2, inner_y2


def estimate_distance_m(depth_map: np.ndarray, bbox: np.ndarray, frame_shape: tuple[int, int], inner_ratio: float) -> float:
    frame_h, frame_w = frame_shape
    depth_h, depth_w = depth_map.shape

    scale_x = depth_w / frame_w
    scale_y = depth_h / frame_h

    x1, y1, x2, y2 = bbox.astype(float)
    dx1 = int(np.clip(np.floor(x1 * scale_x), 0, depth_w - 1))
    dy1 = int(np.clip(np.floor(y1 * scale_y), 0, depth_h - 1))
    dx2 = int(np.clip(np.ceil(x2 * scale_x), dx1 + 1, depth_w))
    dy2 = int(np.clip(np.ceil(y2 * scale_y), dy1 + 1, depth_h))

    ix1, iy1, ix2, iy2 = center_crop_bounds(dx1, dy1, dx2, dy2, inner_ratio)
    roi = depth_map[iy1:iy2, ix1:ix2]
    valid = roi[np.isfinite(roi) & (roi > 0)]

    if valid.size == 0:
        return float("nan")

    return float(np.median(valid))


def draw_detection(frame: np.ndarray, bbox: np.ndarray, class_name: str, conf: float, distance_m: float, annotation_color: tuple[int, int, int] = (0, 0, 139)) -> None:
    x1, y1, x2, y2 = bbox.astype(int)
    cv2.rectangle(frame, (x1, y1), (x2, y2), annotation_color, 2)

    distance_text = "distance=n/a"
    if np.isfinite(distance_m):
        distance_text = f"distance={distance_m:.2f}m"

    label = f"{class_name} {conf:.2f} {distance_text}"
    text_origin = (x1, max(24, y1 - 10))
    cv2.putText(
        frame,
        label,
        text_origin,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        annotation_color,
        2,
        cv2.LINE_AA,
    )


def main() -> None:
    args = parse_args()
    input_path = Path(args.video).expanduser().resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input path not found: {input_path}")

    is_dir = input_path.is_dir()
    image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    image_files = sorted([p for p in input_path.iterdir() if p.suffix.lower() in image_exts]) if is_dir else []

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_stem = args.output_stem or input_path.stem
    annotated_video_path = output_dir / f"{output_stem}_annotated.mp4"
    csv_path = output_dir / f"{output_stem}_detections.csv"
    annotated_images_dir = output_dir / f"{output_stem}_annotated_images"

    detector = YOLO(args.detector_model)
    class_filter = resolve_class_filter(args.classes, detector.names)

    device = torch.device(args.device)
    depth_model = DepthAnything3.from_pretrained(args.depth_model).to(device=device)
    depth_model.eval()

    cap = None
    writer = None
    fps = 30.0
    frame_count = 0

    if not is_dir:
        cap = cv2.VideoCapture(str(input_path))
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {input_path}")

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        writer = cv2.VideoWriter(
            str(annotated_video_path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (frame_width, frame_height),
        )
        if not writer.isOpened():
            raise RuntimeError(f"Failed to create output video: {annotated_video_path}")
    else:
        frame_count = len(image_files)
        annotated_images_dir.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        fieldnames = [
            "frame_index",
            "timestamp_sec",
            "filename",
            "class_id",
            "class_name",
            "confidence",
            "distance_m",
            "x1",
            "y1",
            "x2",
            "y2",
        ]
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        frame_index = 0
        while True:
            if not is_dir:
                ok, frame_bgr = cap.read()
                if not ok:
                    break
                filename = ""
                timestamp = frame_index / fps
            else:
                if frame_index >= len(image_files):
                    break
                img_path = image_files[frame_index]
                frame_bgr = cv2.imread(str(img_path))
                if frame_bgr is None:
                    frame_index += 1
                    continue
                filename = img_path.name
                timestamp = float(frame_index)

            if args.max_frames is not None and frame_index >= args.max_frames:
                break

            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

            with torch.inference_mode():
                depth_prediction = depth_model.inference(
                    image=[frame_rgb],
                    process_res=args.process_res,
                    process_res_method=args.process_res_method,
                )
            depth_map = np.asarray(depth_prediction.depth[0], dtype=np.float32)

            detector_result = detector.predict(
                source=frame_bgr,
                conf=args.conf_threshold,
                iou=args.iou_threshold,
                classes=class_filter,
                verbose=False,
                device=str(device),
            )[0]

            if detector_result.boxes is not None and len(detector_result.boxes) > 0:
                boxes_xyxy = detector_result.boxes.xyxy.detach().cpu().numpy()
                classes = detector_result.boxes.cls.detach().cpu().numpy().astype(int)
                confidences = detector_result.boxes.conf.detach().cpu().numpy()

                for bbox, class_id, confidence in zip(boxes_xyxy, classes, confidences):
                    distance_m = estimate_distance_m(
                        depth_map=depth_map,
                        bbox=bbox,
                        frame_shape=frame_bgr.shape[:2],
                        inner_ratio=args.box_inner_ratio,
                    )
                    class_name = detector.names[int(class_id)]
                    draw_detection(frame_bgr, bbox, class_name, float(confidence), distance_m)
                    csv_writer.writerow(
                        {
                            "frame_index": frame_index,
                            "timestamp_sec": timestamp,
                            "filename": filename,
                            "class_id": int(class_id),
                            "class_name": class_name,
                            "confidence": float(confidence),
                            "distance_m": "" if not np.isfinite(distance_m) else distance_m,
                            "x1": float(bbox[0]),
                            "y1": float(bbox[1]),
                            "x2": float(bbox[2]),
                            "y2": float(bbox[3]),
                        }
                    )

            if writer is not None:
                writer.write(frame_bgr)
            else:
                out_path = annotated_images_dir / filename
                cv2.imwrite(str(out_path), frame_bgr)

            frame_index += 1

            if frame_index % 10 == 0:
                total = frame_count if frame_count > 0 else "?"
                print(f"Processed {frame_index}/{total} frames", flush=True)

    if cap:
        cap.release()
    if writer:
        writer.release()

    if not is_dir:
        print(f"Annotated video written to: {annotated_video_path}")
    else:
        print(f"Annotated images written to: {annotated_images_dir}")
    print(f"Detection CSV written to: {csv_path}")


if __name__ == "__main__":
    main()

# python3 detect_and_estimate_depth.py \
#   --video data/uav0000268_05773_v/ \
#   --detector-model yolo11n.pt \
#   --classes person car \
#   --output-dir output/
