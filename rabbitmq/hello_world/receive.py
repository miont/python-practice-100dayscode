import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print('[*] Received {}'.format(body))

    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=True)

    print("[*] Waiting for messages")
    channel.start_consuming()
    connection.close()

if __name__ == '__main__':
    main()