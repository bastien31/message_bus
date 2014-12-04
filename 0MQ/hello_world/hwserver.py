#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

i=0
while True:
    #  Wait for next request from client
    #message = socket.recv()
    #print("Received request: %s" % message)

    #  Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    print ("Send message: {0}".format(i))
    socket.send(b"World {0}".format(i))
    
    i+=1
