import pika
import time
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange='topic_logs', queue=result.method.queue)

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_keys]...\n" % sys.argv[0])
    sys.exit(1)

for b_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs',
        queue=result.method.queue,
        routing_key=b_key
    )


def callback(ch, method, properties, body):
    print('[x] %r:%r' % (method.routing_key, body))

channel.basic_consume(
    queue=result.method.queue,
    on_message_callback=callback,
    auto_ack=True
)


print('[*] Waiting for logs. To exit press CTRL+C')
channel.start_consuming()