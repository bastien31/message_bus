from crochet import setup, run_in_reactor, wait_for
setup()
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import clientFromString
import sys
from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession, ApplicationSessionFactory
from autobahn.wamp import types
from autobahn.wamp.types import ComponentConfig
from autobahn.twisted.websocket import WampWebSocketClientFactory
import time
SESSION = None


class Component(ApplicationSession):
    """
    An application component calling the different backend procedures.
    """

    def onJoin(self, details):
        print("session attached")

    def onDisconnect(self):
        print("disconnected")

def wait_for_session(timeout=5.0):
    begin_time = time.time()
    end_time = begin_time + float(timeout)
    global SESSION
    exec_time = time.time()
    while exec_time < end_time and not SESSION:
        time.sleep(0.5)
        exec_time = time.time()

@run_in_reactor
def start_wamp():
    def create():
        global SESSION

        cfg = ComponentConfig("realm1", dict())
        try:
            SESSION = Component(cfg)
        except Exception:
            log.err()

        return SESSION

    transport_factory = WampWebSocketClientFactory(create, url="ws://localhost:9000/ws",
                                                   debug=False, debug_wamp=False)

    client = clientFromString(reactor, "tcp:{}:{}".format("localhost", 9000))
    client.connect(transport_factory)

@wait_for(timeout=1)
def get_utc():
    global SESSION
    res = None
    if SESSION:
        res = SESSION.call(u"acs.device.manager.utcnow")
    else:
        print("No session :(")

    return res

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    print ("start")
    start_wamp()
    wait_for_session()
    res = get_utc()
    if res:
        print("date: {}".format(res))
    print ("end")
