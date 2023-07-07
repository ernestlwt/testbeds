import cv2
import json
import math
import numpy as np
import redis
from datetime import datetime

from VideoManager import VideoManager
from confluent_kafka import Producer, Consumer
from confluent_kafka.admin import AdminClient, NewTopic, KafkaError

CAMERAS = [
    { "camera_name": "cam1", "camera_url": "rtsp://localhost:8554/mystream1" },
    { "camera_name": "cam2", "camera_url": "rtsp://localhost:8554/mystream2" },
    { "camera_name": "cam3", "camera_url": "rtsp://localhost:8554/mystream3" },
    { "camera_name": "cam4", "camera_url": "rtsp://localhost:8554/mystream4" },
    { "camera_name": "cam5", "camera_url": "rtsp://localhost:8554/mystream5" }
]

FRAMES = [None] * len(CAMERAS)

KAFKA_SERVER="localhost:19092"
KAFKA_MONITOR_TOPIC="kafka_monitoring"
DATETIME_FORMAT="%Y/%m/%d,%H:%M:%S:%f"
REDIS_HOST="localhost"
REDIS_PORT="6379"
REDIS_PASSWORD=""

VIEW_ON_KAFKA=False

def setup_kafka_redis():
    producer = Producer({
        "bootstrap.servers": KAFKA_SERVER
    })

    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


    admin_client = AdminClient({
        "bootstrap.servers": KAFKA_SERVER
    })

    topic_list = [KAFKA_MONITOR_TOPIC]

    kafka_topic_list = []
    for topic in topic_list:
        new_topic = NewTopic(topic, 1, 1)
        kafka_topic_list.append(new_topic)
    fs = admin_client.create_topics(kafka_topic_list)

    for topic, f in fs.items():
        try:
            f.result()  # The result itself is None
            print("Topic {} created".format(topic))
        except Exception as e:
            if e.args[0].code() == KafkaError.TOPIC_ALREADY_EXISTS:
                print("Topic {} already created".format(topic))
            else:
                print("Failed to create topic {}: {}".format(topic, e))

    return producer, redis_client

def draw_text(
        img, text,
        font=cv2.FONT_HERSHEY_PLAIN,
        pos=(0, 0),
        font_scale=1,
        font_thickness=1,
        text_color=(0, 255, 0),
        text_color_bg=(0, 0, 0)
    ):

    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, -1)
    cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)

    return text_size

def stack_frames(frames, num_horizontal, frame_size=(120,90)):
    total_frames = len(frames)
    num_rows = math.ceil(total_frames / num_horizontal)
    num_odd = num_horizontal * num_rows - total_frames

    count = 0

    big_frame = None

    frame_counter = 0
    for row in range(num_rows):
        row_frame = None
        while frame_counter < total_frames and frame_counter < ((row + 1) * num_horizontal):
            if frames[frame_counter] is None or len(frames[frame_counter]) == 0:
                frame = np.zeros((frame_size[1], frame_size[0], 3), dtype = "uint8")
            else:
                frame = cv2.resize(frames[frame_counter], frame_size)
            draw_text(frame, CAMERAS[frame_counter]["camera_name"], pos=(10,10))

            if row_frame is None:
                row_frame = frame
            else:
                row_frame = np.hstack((row_frame, frame))
            frame_counter += 1

        if row == num_rows - 1 and num_odd:
            for i in range(num_odd):
                frame = np.zeros((frame_size[1], frame_size[0], 3), dtype = "uint8")
                row_frame = np.hstack((row_frame, frame))
        
        if big_frame is None:
            big_frame = row_frame
        else:
            big_frame = np.vstack((big_frame, row_frame))
    
    return big_frame

def store_frame_in_redis(frame, redis_client):
    key = datetime.now().strftime(DATETIME_FORMAT)

    redis_client.set(key, frame)
    # set the expiration time for the key to 1 minute
    redis_client.expire(key, 10)
    return key

video_cap_list = []

vid_manager = VideoManager(CAMERAS, videoFile=False)
vid_manager.start()

while True:
    status, frames = vid_manager.read()
    for i, f in enumerate(frames):
        if len(f) != 0:
            FRAMES[i] = f
    big_frame = stack_frames(FRAMES, 3, frame_size=(480, 360))

    cv2.imshow("monitor", big_frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

    # producer, redis_client = setup_kafka_redis()
    # _, buffer = cv2.imencode('.jpg', big_frame)

    # key = store_frame_in_redis(buffer.tobytes(), redis_client)
    # msg = {
    #     "key": key
    # }
    # msg_str = json.dumps(msg)
    # producer.produce(KAFKA_MONITOR_TOPIC, msg_str)
