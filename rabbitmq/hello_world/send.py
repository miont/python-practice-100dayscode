import pika

def send_msg(channel, msg):
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body=msg)
    print(f"[*] Sent '{msg}'")


def send_batch(channel, count):
    for i in range(count):
        send_msg(channel, f'msg {i+1}')

def main(queue_name='msgs'):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    send_batch(channel, 5)
    connection.close()

if __name__ == '__main__':
    main()