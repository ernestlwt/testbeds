import pika
import time
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)

channel.queue_bind(exchange='direct_logs', queue=result.method.queue)

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(
        exchange='direct_logs',
        queue=result.method.queue,
        routing_key=severity
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