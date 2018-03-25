import pika
import time
import sys
from pika.spec import PERSISTENT_DELIVERY_MODE


def producer(exchange, *keys):
    keys = list(keys)

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.17.38.137',
        # credentials=pika.PlainCredentials(username='admin', password='admin123')
    ))
    channel = connection.channel()

    # channel.exchange_declare(exchange='devops', exchange_type='fanout')
    channel.exchange_declare(exchange=exchange, exchange_type='topic')
    channel.queue_declare(queue='log', durable=True)
    channel.queue_bind(queue='log', exchange=exchange, routing_key='#')

    for count in range(0, 100):
        if len(keys) > 1:
            key = keys.pop(0)
            keys.append(key)
        else:
            key = keys[0] if len(keys) > 0 else ''

        result = channel.basic_publish(
            exchange=exchange,
            routing_key=key,
            body='{index} [{key}]'.format(index=count, key=key),
            properties=pika.BasicProperties(
                delivery_mode=PERSISTENT_DELIVERY_MODE
            )
        )
        print(result)

    channel.close()
    connection.close()

def consumer(exchange, *keys):
    keys = list(keys)

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.17.38.137',
        # credentials=pika.PlainCredentials(username='admin', password='admin123')
    ))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    channel.exchange_declare(exchange=exchange, exchange_type='topic')

    temporary_queue_declare_result = channel.queue_declare(exclusive=True)
    temporary_queue_name = temporary_queue_declare_result.method.queue

    for key in keys:
        channel.queue_bind(queue=temporary_queue_name, exchange=exchange, routing_key=key)

    def callback(ch, method, properties, body):

        print(method)
        print(properties)
        print(ch)
        print('{key} : {body}'.format(key=method.routing_key, body=body))
        # print('{counter} {key} : {body}'.format(counter=counter, key=method.routing_key, body=body))
        time.sleep(0.2)
        channel.basic_ack(method.delivery_tag)


    channel.basic_consume(callback, queue=temporary_queue_name, no_ack=False, arguments={'test': 'yo'})
    channel.start_consuming()


if __name__ == '__main__':
    {
        'consumer': consumer,
        'producer': producer,
    }.get(sys.argv[1], lambda *args: print('dumb'))(*sys.argv[2:]) if len(sys.argv) > 2 else print('dumb')


