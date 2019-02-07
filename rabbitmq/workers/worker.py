import pika
import sys
import logging
from utils import config_logger

log = logging.getLogger(__name__)

def callback(ch, method, properties, body):
    print('Received: {}'.format(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    log.info('Message {} received and processed'.format(body))

def main():
    logging.getLogger('pika').setLevel(logging.ERROR)
    if len(sys.argv) < 2:
        worker_id = 1
    else:
        worker_id = sys.argv[1]
    worker_name = 'Worker_{}'.format(worker_id)
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='tasks')
    log.info('{} started'.format(worker_name))
    print("[*] {}: waiting for messages. To exit press CTRL+C".format(worker_name))

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='tasks')

    channel.start_consuming()
    log.info('{} finished'.format(worker_name))

if __name__ == '__main__':
    config_logger(log_file='logs/worker.log')
    main()