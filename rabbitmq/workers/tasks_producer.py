import pika
import sys
import logging
from utils import config_logger

log = logging.getLogger(__name__)

def send_tasks(channel, queue_name, count):
    for i in range(count):
        msg = 'Task {}'.format(i)
        channel.basic_publish(exchange='',
                            routing_key=queue_name,
                            body=msg,
                            properties=pika.BasicProperties(
                                delivery_mode=2
                            ))
        log.info('{} published'.format(msg))

def main(queue_name='tasks', tasks_count=5):
    logging.getLogger('pika').setLevel(logging.ERROR)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    # channel.queue_declare(queue=queue_name, durable=True)
    send_tasks(channel, queue_name, tasks_count)
    connection.close()

if __name__ == '__main__':
    config_logger(log_file='logs/tasks_producer.log')
    main()