#
#  Synchronized subscriber
#
import time
import zmq

def sync_service(context):
    # Socket to receive signals
    syncservice = context.socket(zmq.REP)
    syncservice.bind('tcp://*:5562')

    # Get synchronization from subscribers
    # wait for synchronization request
    #msg = syncservice.recv()
    # send synchronization reply
    #syncservice.send(b'')
    return syncservice

def sync_client(context):
    # Second, synchronize with publisher
    syncclient = context.socket(zmq.REQ)
    syncclient.connect('tcp://localhost:5562')

    # send a synchronization request
    syncclient.send(b'')

    # wait for synchronization reply
    syncclient.recv()

    time.sleep(1)

def poll(sub, sync):
    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    poller.register(sync, zmq.POLLIN)

    nbr = 0
    while True:
        socks = dict(poller.poll())
        if sync in socks and socks[sync] == zmq.POLLIN:
            msg = sync.recv()
            print ("Receive {0}".format(msg))
            sync.send(b'Pong')
            print ("Send {0}".format(b'Pong'))

        if sub in socks and socks[sub] == zmq.POLLIN:
            msg = sub.recv()
            print ("Receive {0}".format(msg))
            if msg == b'END':
                break
            nbr += 1

    print ('Received %d updates' % nbr)

def main():
    context = zmq.Context()

    # First, connect our subscriber socket
    subscriber = context.socket(zmq.SUB)
    subscriber.connect('tcp://localhost:5561')
    subscriber.setsockopt(zmq.SUBSCRIBE, b'')

    #sync_client(context)
    syncservice = sync_service(context)

    poll(subscriber, syncservice)
    return 

    # Third, get our updates and report how many we got
    nbr = 0
    while True:
        msg = subscriber.recv()
        if msg == b'END':
            break
        nbr += 1

    print ('Received %d updates' % nbr)

if __name__ == '__main__':
    main()
