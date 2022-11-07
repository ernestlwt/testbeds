import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

print("Realsense product line: " + str(device_product_line) )

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == "RGB Camera":
        found_rgb = True
        break
if not found_rgb:
    print("RGB sensor not found on camea")
    exit(0)

# RGB resolution = 1920 x 1080, but test if 640, 480 is sufficient for demo
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) # color, width, height, format, fps

pipeline.start(config)

try:
    while True:

        # wait for next RGB frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        
        color_image = np.asanyarray(color_frame.get_data())

        cv2.namedWindow("RealSense", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("RealSense", color_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break # exit when press q

finally:
    pipeline.stop()

