#!/usr/bin/env python
import pika
import socket
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='tldlabacsdev02.tl.intel.com'))

channel = connection.channel()
channel.queue_declare(queue='hello')


i = 0
while True:
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World {0} from {1}!'.format(i, socket.getfqdn()))
    time.sleep(1)
    i += 1

connection.close()
