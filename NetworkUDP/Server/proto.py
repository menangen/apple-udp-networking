from typing import Tuple
from log import Log
from network import NetworkData
import udp

import events


class Protocol:
    dest: Tuple = (None, None)

    class Header:
        VERSION: int = 1

        def __init__(self, data: bytes):
            self.data = data

            self.CHUNK = 0
            self.TOTAL_CHUNKS = 0

            self.chunk_id = NetworkData.get_chunk_id(self.CHUNK, self.TOTAL_CHUNKS)

        def __add__(self, content_bytes: bytes):
            return bytes([self.VERSION, self.chunk_id, len(self.data)]) + content_bytes

    def __init__(self, port: int = 5000):
        self.socket = udp.Socket(port=port)
        self.counterPacket = 0

    def encode(self, var: str or int or events.Event):

        if isinstance(var, str):
            Log.success("String encoding")
            data = var.encode()

        elif isinstance(var, int):
            Log.success("Int encoding")
            data = NetworkData.to_bytes(1, var)

        elif isinstance(var, events.Event):
            Log.success("Event encoding")
            data = var.serialize()

        else:
            Log.notice("Error at encoding")
            raise ValueError

        header_data = self.Header(data)

        return header_data + data

    @staticmethod
    def decode(data: bytes):
        Log.success("Decoding UDP packet data:")

        if data[0:1] == bytes([Protocol.Header.VERSION]):
            # Log.variable("Processing data", tohex(data).upper())

            packet_data = data[3:]
            packet_type = packet_data[0]

            Log.variable("Packet type", packet_type)

            event_id = packet_type & 127

            Log.variable("Event id", event_id)

            for e in events.events:
                if event_id == e.id:
                    event = e.decode(packet_data[1:])
                    return event

        else:
            Log.notice("Processing random [ udp ] packet")

    def set_destination(self, address_and_port):
        self.dest = address_and_port

    def send(self, var):
        data = self.encode(var)
        self.socket.send(data, self.dest)

        Log.variable("Sent UDP bytes", list(data), level=1)
        self.counterPacket += 1

