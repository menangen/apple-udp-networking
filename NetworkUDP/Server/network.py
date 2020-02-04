class NetworkData:

    @classmethod
    def to_bytes(cls, data, signed=False):
        return data.to_bytes(2, byteorder="little", signed=signed)

    @classmethod
    def to_int(cls, data, signed=False):
        return int.from_bytes(data, byteorder="little", signed=signed)
