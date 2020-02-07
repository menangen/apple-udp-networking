from typing import Tuple
from log import Log
from network import NetworkData
import udp


class Protocol:
    dest: Tuple = (None, None)

    def __init__(self, port: int = 5000, version: int = 1):
        self.socket = udp.Socket(port=port)
        self.counterPacket = 0

        self.VERSION = version - 1
        self.CHUNK = 0
        self.TOTAL_CHUNKS = 0

    @staticmethod
    def compute_chunks(size: int):
        full_chunks = size >> 9
        partial_chunk = size & 511

        return full_chunks, partial_chunk

    @staticmethod
    def get_chunk_id(current: int = 0, total: int = 0):
        return current << 4 | total

    def get_header(self, data_length: int):
        chunk_id = self.get_chunk_id(self.CHUNK, self.TOTAL_CHUNKS)

        return bytes([self.VERSION, chunk_id, data_length])

    def encode(self, var: str or int):

        if isinstance(var, str):
            Log.notice("String encoding")
            data = var.encode()

        elif isinstance(var, int):
            Log.notice("Int encoding")
            data = NetworkData.to_bytes(1, var)

        else:
            raise ValueError

        header_data = self.get_header(len(data))

        return header_data + data

    def set_destination(self, address_and_port):
        self.dest = address_and_port

    def send_string(self, string_data):
        data = self.encode(string_data)
        self.socket.send(data, self.dest)

        Log.variable("Sent UDP bytes", list(data), level=1)
        self.counterPacket += 1

