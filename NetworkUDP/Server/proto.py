from network import NetworkData


class Protocol:
    VERSION = 1

    @classmethod
    def for_string(cls, text: str):
        data = bytes([cls.VERSION])

        return data + text.encode()

    @classmethod
    def for_integer(cls, var: int, size: int = 1):
        return NetworkData.to_bytes(size, var)
