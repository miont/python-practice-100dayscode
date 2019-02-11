# Simple rpc server based on this tutorial:
# https://www.rabbitmq.com/tutorials/tutorial-six-python.html

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def work1(n):
    return 2*n

def on_request(ch, method, props, body):
    n = int(body)

    print("[*] received: {}".format(n))

    response = work1(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id= \
                                                     props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print('[*] send: {}'.format(response))

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='rpc_queue')

print('[*] Awaiting RPC requests')
channel.start_consuming()
