# Simple rpc client based on this tutorial:
# https://www.rabbitmq.com/tutorials/tutorial-six-python.html

import pika
import uuid

class SimpleRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
    
        self.requests = {}
        self.responses = {}

    def on_response(self, ch, method, props, body):
        print('[*] Response for correclation id {} received'.format(props.correlation_id))
        self.responses[props.correlation_id] = int(body)
    
    def send_task(self, n):
        corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=corr_id
                                       ),
                                   body=str(n))
        self.requests[corr_id] = n
        print('[*] Task {} published'.format(corr_id))
    
    def wait_all_responses(self):
        print('[*] Waiting for responses')
        while len(self.responses) < len(self.requests):
            self.connection.process_data_events()
        print('[*] All responses collected')

    def print_results(self):
        print('[*] Results(req -> res):')
        for k in self.requests.keys():
            req = self.requests.get(k)
            res = self.responses.get(k)
            if res is None:
                print('ERROR: no response for id {}'.format(k))
                continue
            print('{} -> {}'.format(req, res))

if __name__ == '__main__':
    # init client
    client = SimpleRpcClient()
    # send tasks
    print('[*] Sending tasks')
    for n in [1, 5, 12, 27, 44, 77]:
        client.send_task(n)
    # collect all responses
    client.wait_all_responses()
    client.print_results()