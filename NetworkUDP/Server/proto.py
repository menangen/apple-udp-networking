from network import NetworkData


class Protocol:

    def __init__(self, version: int = 1):
        self.VERSION = version
        self.CHUNK = 0
        self.CHUNKS_NUMBER = 0

    @staticmethod
    def compute_chunks(size: int):
        full_chunks = size >> 9
        partial_chunk = size & 511

        return full_chunks, partial_chunk

    @staticmethod
    def get_chunk_id(current: int = 0, total: int = 0):
        return current << 4 | total

    def get_header(self, data_length: int):
        chunk_id = self.get_chunk_id(self.CHUNK, self.CHUNKS_NUMBER)

        return bytes([self.VERSION, chunk_id, data_length])

    def encode(self, data: bytes, size: int):
        header_data = self.get_header(size)

        return header_data + data

    def for_string(self, text: str):
        return self.encode(text.encode(), len(text))

    def for_integer(self, var: int, size: int = 1):
        return self.encode(NetworkData.to_bytes(size, var), size)
