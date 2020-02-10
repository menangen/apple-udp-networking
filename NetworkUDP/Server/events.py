from log import Log


class Position:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def serialize(self):
        # to 32-bit bin data (16-bit per coord)
        # FFF for x, FFF for y
        data = self.x << 16 | self.y

        return data.to_bytes(4, byteorder="big", signed=False)


class Event:
    id = 0
    ask = False

    def __init__(self, identificator: int = 0):
        self.id = identificator

    def serialize(self):
        # 8-bit packet type
        _flag = self.ask << 7
        packet_id = _flag | self.id

        return packet_id.to_bytes(1, byteorder="big", signed=False)

    @staticmethod
    def decode(data: bytes):
        packet_type = data[0]
        packet_data = data[1:]

        Log.udp_content("Event data", packet_data)

        return packet_data


class Hello(Event):
    def __init__(self, message: str):
        super().__init__()

        self.ask = True
        self.content = message.encode()

    def serialize(self):
        packet_type = super().serialize()

        Log.udp_content("Packet type", list(packet_type))
        Log.udp_content("Content", list(self.content))

        data = packet_type + self.content

        Log.notice(f"Length: {len(data)}")

        return data


class Movement(Event):
    id = 1

    def __init__(self, from_point: Position, to_point: Position):
        super().__init__(self.id)

        self.ask = True

        self.from_position = from_point.serialize()
        self.to_position = to_point.serialize()

    def serialize(self):
        packet_type = super().serialize()

        Log.udp_content("Packet type", list(packet_type))

        Log.udp_content("From", list(self.from_position))
        Log.udp_content("To", list(self.to_position))

        data = packet_type + self.from_position + self.to_position

        return data


ALL = [Movement, Hello]
