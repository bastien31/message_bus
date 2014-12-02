import six
import datetime
import json
from autobahn.twisted.wamp import Application
from Name import Name, json_dumps

app = Application("acs.device.manager")

@app.register()
def name():
    #print("Someone is asking for my name ;)")
    data = json_dumps(Name())
    #print("Returning: {}".format(data))
    return data

@app.register()
def utcnow():
    #print("Someone is asking for the time ;)")
    now = datetime.datetime.utcnow()
    return six.u(now.strftime("%Y-%m-%dT%H:%M:%SZ"))


if __name__ == '__main__':
    app.run("ws://127.0.0.1:8080/ws", "realm1", standalone=True)
