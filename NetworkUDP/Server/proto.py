from typing import Tuple
from log import Log
from network import NetworkData
import udp


class Protocol:
    dest: Tuple = (None, None)

    class Header:
        def __init__(self, data: bytes):
            self.data = data

            self.VERSION: int = 1
            self.CHUNK = 0
            self.TOTAL_CHUNKS = 0

            self.chunk_id = NetworkData.get_chunk_id(self.CHUNK, self.TOTAL_CHUNKS)

        def __add__(self, content_bytes: bytes):
            return bytes([self.VERSION, self.chunk_id, len(self.data)]) + content_bytes

    def __init__(self, port: int = 5000):
        self.socket = udp.Socket(port=port)
        self.counterPacket = 0

    def encode(self, var: str or int):

        if isinstance(var, str):
            Log.success("String encoding")
            data = var.encode()

        elif isinstance(var, int):
            Log.success("Int encoding")
            data = NetworkData.to_bytes(1, var)

        else:
            Log.notice("Error at encoding")
            raise ValueError

        header_data = self.Header(data)

        return header_data + data

    def set_destination(self, address_and_port):
        self.dest = address_and_port

    def send_string(self, string_data):
        data = self.encode(string_data)
        self.socket.send(data, self.dest)

        Log.variable("Sent UDP bytes", list(data), level=1)
        self.counterPacket += 1

