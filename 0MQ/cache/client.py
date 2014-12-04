#
#  Synchronized publisher
#
import time
import zmq

def sync_client(context):
    # Second, synchronize with publisher
    syncclient = context.socket(zmq.REQ)
    syncclient.connect('tcp://localhost:5562')

    # send a synchronization request
    print ("Send {0}".format(b'Ping'))
    syncclient.send(b'Ping')

    # wait for synchronization reply
    msg = syncclient.recv()
    print ("Receive {0}".format(msg))

    time.sleep(1)

def sync_service(context):
    # Socket to receive signals
    syncservice = context.socket(zmq.REP)
    syncservice.bind('tcp://*:5562')

    # Get synchronization from subscribers
    # wait for synchronization request
    msg = syncservice.recv()
    # send synchronization reply
    syncservice.send(b'')

def main():
    context = zmq.Context()

    # Socket to talk to clients
    publisher = context.socket(zmq.PUB)
    # set SNDHWM, so we don't drop messages for slow subscribers
    publisher.sndhwm = 1100000
    publisher.bind('tcp://*:5561')

    #sync_service(context)
    sync_client(context)

    # Now broadcast exactly 1M updates followed by END
    for i in range(100):
    	print ("Send {0}:{1}".format(b'Rhubarb', i))
        publisher.send("{0}:{1}".format(b'Rhubarb', i))

    publisher.send(b'END')

if __name__ == '__main__':
    main()
