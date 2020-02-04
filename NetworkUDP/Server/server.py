import udp
from proto import Protocol
from log import Log
from binascii import hexlify as tohex


class Server:
    PORT = 5000

    def __init__(self, port: int = PORT):
        self.socket = udp.Socket(port=port)
        self.counterPacket = 0

    def process(self):
        while True:
            try:
                data, from_addr = self.socket.read()

                Log.variable("counterPacket", self.counterPacket, level=1)

                if data != b"getLast":
                    Log.variable("Processing data", tohex(data).upper())

                else:
                    Log.notice("Processing [ getLast ] message")

            except KeyboardInterrupt:
                print("\tClosed by an Interrupt")
                break

            Log.sending_integer(self.counterPacket, from_addr[0])

            data = Protocol.for_integer(self.counterPacket)
            self.socket.send(data, from_addr)

            Log.request_end()


s = Server()
s.process()