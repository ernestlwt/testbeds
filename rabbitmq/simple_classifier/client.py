import pika
import uuid

routing_keys = {
    'load_model': 'load',
    'unload_model': 'unload',
    'do_inference': 'infer'
}

class ClassifierClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='clkassifier_exchange', exchange_type='direct')

        result_queue = self.channel.queue_declare(queue='inference_result', exclusive=True)
        self.callback_queue = result_queue.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call_load_model(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='classifier_exchange',
            routing_key=routing_keys['load_model'],
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=''
        )
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)

    def call_unload_model(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='classifier_exchange',
            routing_key=routing_keys['unload_model'],
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=''
        )
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)

    def call_inference(self, img_path):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='classifier_exchange',
            routing_key=routing_keys['do_inference'],
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                expiration='20000'
            ),
            body=str(img_path)
        )
        while self.response is None:
            self.connection.process_data_events()
        return str(self.response)


client = ClassifierClient()
print('[x] Sent inference_request')
response = client.call_inference('dog.jpg')
print('[*] Results: ' + response)
print('[x] Sent load_request')
response = client.call_load_model()
print('[*] Results: ' + response)
print('[x] Sent inference_request')
response = client.call_inference('dog.jpg')
print('[*] Results: ' + response)
print('[x] Sent unload_request')
response = client.call_unload_model()
print('[*] Results: ' + response)