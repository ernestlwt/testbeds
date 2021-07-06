import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

def callback(ch, method, properties, body):
    print('[x] Received '+ str(body))
    time.sleep(body.count(b'.'))
    print('[x] Job done')
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
# default round robin is not good enough
# (e.g when you have 2 workers but every ODD-th job is more time consuming, ODD-th jobs will then always introduce delay)
# this line will then dispatch jobs only to available workers

channel.basic_consume(
    queue='hello',
    on_message_callback=callback
)


print('[*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()