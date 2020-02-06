from log import Log
import udp
from proto import Protocol
from json import dumps


class Client:
    PORT = 3000

    def __init__(self, port: int = PORT):
        self.socket = udp.Socket(port=port)
        self.counterPacket = 0
        self.protocol = Protocol()

    def send(self, address):
        json_string = dumps(
            {
                "type": "move",
                "to": [0, 0],
                "from": [1, 0],
                "ask": True
            }
        )

        Log.variable("json_data", json_string)

        data = self.protocol.for_string(json_string)
        self.socket.send(data, address)

        Log.variable("Sent UDP", list(data), level=1)
        self.counterPacket += 1


c = Client()
c.send(("127.0.0.1", 5000))
