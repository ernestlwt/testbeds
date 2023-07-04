import cv2
import redis
import json
import numpy as np
from confluent_kafka import Consumer, OFFSET_BEGINNING, OFFSET_END

REDIS_HOST="localhost"
REDIS_PORT="6379"
REDIS_PASSWORD=""

KAFKA_SERVER="localhost:19092"
KAFKA_MONITOR_TOPIC="kafka_monitoring"

kafka_consumer = Consumer({
    "bootstrap.servers": KAFKA_SERVER,
    "group.id": "hi",
    "auto.offset.reset": "latest"
})

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=False)

def process_message(msg, redis_client):
    msg = json.loads(msg.value())
    redis_key = msg['key']
    redis_value = redis_client.get(redis_key)
    if redis_value is None:
        print("ERROR: Redis key not found")
    else:
        frame = np.frombuffer(redis_value, dtype=np.uint8)
        frame = cv2.imdecode(frame, flags=1)
        cv2.imshow("monitor", frame)

def reset_offset(consumer, partitions, reset):
    if reset:
        for p in partitions:
            p.offset = OFFSET_END
        consumer.assign(partitions)

kafka_consumer.subscribe([KAFKA_MONITOR_TOPIC], on_assign=lambda c, p: reset_offset(c, p, True))

while True:
    msg = kafka_consumer.poll(1.0)
    if msg is None:
        print("Waiting...")
    elif msg.error():
        print(f"ERROR: {msg.error()}")
    else:
        print("Consumed event from topic {topic}".format(topic=msg.topic()))
        process_message(msg, redis_client)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
consumer.close()