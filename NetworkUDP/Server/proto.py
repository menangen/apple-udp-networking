from network import NetworkData


class Protocol:

    def __init__(self, version: int = 1):
        self.VERSION = version

    def get_header(self, data_length: int):
        return bytes([self.VERSION, data_length])

    def for_string(self, text: str):
        header_data = self.get_header(len(text))

        return header_data + text.encode()

    def for_integer(self, var: int, size: int = 1):
        header_data = self.get_header(size)
        return header_data + NetworkData.to_bytes(size, var)
