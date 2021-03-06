from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.python import log
import sys

from autobahn.twisted.wamp import ApplicationRunner, ApplicationSession
import jsonpickle


class Component(ApplicationSession):
    """
    An application component calling the different backend procedures.
    """

    @inlineCallbacks
    def onJoin(self, details):
        print("session attached")

        res = yield self.call(u"acs.device.manager.utcnow")
        print("date: {}".format(res))

        res = yield self.call(u"acs.device.manager.name")
        test = jsonpickle.decode(res.decode('utf8'))
        print("nom: {name.nom} & prenom: {name.prenom}".format(name=test))
        self.leave()

    def onDisconnect(self):
        print("disconnected")
        reactor.stop()

if __name__ == '__main__':
    log.startLogging(sys.stdout)

    runner = ApplicationRunner("ws://localhost:9000/ws", "realm1", debug=False)
    runner.run(Component)
