from log import Log
import udp
import proto


class Server:
    PORT = 5000

    def __init__(self, port: int = PORT):
        self.socket = udp.Socket(port=port)
        self.counterPacket = 0

    def process(self):
        while True:
            try:
                data, from_addr = self.socket.read()

                # Log.variable("counterPacket", self.counterPacket, level=1)
                event = proto.Protocol.decode(data)
                Log.notice(event)

            except KeyboardInterrupt:
                print("\tClosed by an Interrupt")
                break

            # Log.sending_integer(self.counterPacket, from_addr[0])

            # data = Protocol.for_integer(self.counterPacket)
            # self.socket.send(data, from_addr)

            Log.request_end()


s = Server()
s.process()