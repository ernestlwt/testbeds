import tensorflow as tf

from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras import backend

import numpy as np
import pika
import gc

model = None

routing_keys = {
    'load_model': 'load',
    'unload_model': 'unload',
    'do_inference': 'infer'
}

def load_model():
    global model
    # required on some machines when unable to find convolution algorithm
    physical_devices = tf.config.experimental.list_physical_devices('GPU') 
    for physical_device in physical_devices: 
        tf.config.experimental.set_memory_growth(physical_device, True)

    model = ResNet50(weights='imagenet')
    do_inference('dog.jpg') # do initialization once to load model im memory

def do_inference(img_path):
    global model
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    # decode the results into a list of tuples (class, description, probability)
    # (one such list for each sample in the batch)
    return decode_predictions(preds, top=3)[0]

def unload_model():
    global model
    del model
    backend.clear_session()
    gc.collect()
    model = None

def on_request(ch, method, props, body):
    global model
    if method.routing_key == routing_keys['load_model']:
        if model is None:
            load_model()
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id = props.correlation_id),
            body='model loaded'
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif method.routing_key == routing_keys['unload_model']:
        unload_model()
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id = props.correlation_id),
            body='model unloaded'
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif method.routing_key == routing_keys['do_inference']:
        if model is None:
            ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id = props.correlation_id),
                body='model not loaded'
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        results = do_inference(body)
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id = props.correlation_id),
            body=str(results)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='classifier_exchange', exchange_type='direct')
inference_queue = channel.queue_declare(queue='inference_queue')

for routing_key in list(routing_keys.values()):
    channel.queue_bind(
        exchange='classifier_exchange',
        queue=inference_queue.method.queue,
        routing_key=routing_key
    )

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    queue=inference_queue.method.queue,
    on_message_callback=on_request
)

print('[*] Waiting for inference requests. To exit press CTRL+C')
channel.start_consuming()

