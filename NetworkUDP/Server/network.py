class NetworkData:

    @classmethod
    def to_bytes(cls, number: int, integer_data, signed=False):
        return integer_data.to_bytes(number, byteorder="little", signed=signed)

    @classmethod
    def to_int(cls, data, signed=False):
        return int.from_bytes(data, byteorder="little", signed=signed)
