from log import Log
import udp
from proto import Protocol


class Client:
    PORT = 3000

    def __init__(self, port: int = PORT):
        self.socket = udp.Socket(port=port)
        self.counterPacket = 0
        self.protocol = Protocol()

    def send(self, address):
        data = self.protocol.for_string(r"HI")

        self.socket.send(data, address)

        Log.variable("Sent UDP", list(data))

        self.counterPacket += 1


c = Client()
c.send(("127.0.0.1", 5000))
