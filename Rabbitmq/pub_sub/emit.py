#!/usr/bin/env python
import pika
import socket
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='tldlabacsdev02.tl.intel.com'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

i = 0
while True:
    channel.basic_publish(exchange='logs',
                          routing_key='',
                          body='info: Hello World {0} from {1}!'.format(i, socket.getfqdn()))
    i += 1
                      
print " [x] Sent %r" % (message,)
connection.close()
