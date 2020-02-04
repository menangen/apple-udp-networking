import udp
from proto import Protocol


class Client:
    PORT = 3000

    def __init__(self, port: int = PORT):
        self.socket = udp.Socket(port=port)
        self.counterPacket = 0

    def send(self, address):
        data = Protocol.for_string(r"HI")

        self.socket.send(data, address)
        self.counterPacket += 1


c = Client()
c.send(("127.0.0.1", 5000))
