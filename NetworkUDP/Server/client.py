from log import Log
from proto import Protocol
from json import dumps

from events import Position, Movement, Hello


class Client:
    PORT = 3000

    def __init__(self, port: int = PORT):
        self.protocol = Protocol(port)

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

        self.protocol.set_destination(address)
        self.protocol.send(Hello(json_string))

        event = Movement(Position(1, 254), Position(1, 255))
        self.protocol.send(event)


c = Client()
c.send(("127.0.0.1", 5000))
