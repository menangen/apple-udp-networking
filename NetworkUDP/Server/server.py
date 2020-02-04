import udp
from network import NetworkData
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
                    incoming_number = NetworkData.to_int(data)

                    Log.udp_content("incoming_number", incoming_number)

                    if incoming_number:
                        Log.save_packet_id(incoming_number, self.counterPacket + 1 == incoming_number)

                    self.counterPacket += 1
                else:
                    Log.notice("Processing [ getLast ] message")

            except KeyboardInterrupt:
                print("\tClosed by an Interrupt")
                break

            Log.sending_integer(self.counterPacket, from_addr[0])

            data = NetworkData.to_bytes(2, self.counterPacket)
            self.socket.send(data, from_addr)

            Log.request_end()


s = Server()
s.process()