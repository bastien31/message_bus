import six
import datetime

from autobahn.twisted.wamp import Application

app = Application("acs.device.manager")

@app.register()
def utcnow():
    print("Someone is asking for the time ;)")
    now = datetime.datetime.utcnow()
    return six.u(now.strftime("%Y-%m-%dT%H:%M:%SZ"))

if __name__ == '__main__':
    app.run("ws://localhost:9000/ws", "realm1", standalone=True)
