class NetworkData:

    @classmethod
    def to_bytes(cls, number: int, integer_data, signed=False):
        return integer_data.to_bytes(number, byteorder="little", signed=signed)

    @classmethod
    def to_int(cls, data, signed=False):
        return int.from_bytes(data, byteorder="little", signed=signed)

    @classmethod
    def get_chunk_id(cls, current: int = 0, total: int = 0):
        return current << 4 | total

    @classmethod
    def compute_chunks(cls, size: int):
        full_chunks = size >> 9
        partial_chunk = size & 511

        return full_chunks, partial_chunk
