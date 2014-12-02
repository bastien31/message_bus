from twisted.internet.defer import inlineCallbacks
import datetime
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
import json
from Name import Name, json_dumps
import six


class ServerCross(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):

        def name():
            # print("Someone is asking for my name ;)")
            data = json_dumps(Name())
            #print("Returning: {}".format(data))
            return data

        def utcnow():
            # print("Someone is asking for the time ;)")
            now = datetime.datetime.utcnow()
            return six.u(now.strftime("%Y-%m-%dT%H:%M:%SZ"))

        yield self.register(name, u"acs.device.manager.name")
        yield self.register(utcnow, u"acs.device.manager.utcnow")
