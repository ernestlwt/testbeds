import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

message = ' '.join(sys.argv[1:] or 'Hello World')

channel.basic_publish(
    exchange='',
    routing_key='hello',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode = 2 # persistent message
    )
)

print('[x] Sent ' + str(message))
connection.close()