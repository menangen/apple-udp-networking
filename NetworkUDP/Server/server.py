from binascii import hexlify as tohex
from json import loads

from log import Log
import udp
import events


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

                if data[0:2] == bytes([1, 0]):
                    Log.variable("Processing data", tohex(data).upper())

                    packet_data = data[3:]
                    packet_type = packet_data[0]

                    Log.variable("Packet type", packet_type)

                    event_id = packet_type & 127

                    Log.variable("Event id", event_id)

                    for e in events.ALL:
                        if event_id == e.id:
                            event_content = e.decode(packet_data)

                            if event_id == 0:
                                Log.notice("Hello event")

                                json_str = event_content.decode('ascii')

                                obj = loads(json_str)
                                Log.notice(obj)

                else:
                    Log.notice("Processing random [ udp ] packet")

            except KeyboardInterrupt:
                print("\tClosed by an Interrupt")
                break

            # Log.sending_integer(self.counterPacket, from_addr[0])

            # data = Protocol.for_integer(self.counterPacket)
            # self.socket.send(data, from_addr)

            Log.request_end()


s = Server()
s.process()