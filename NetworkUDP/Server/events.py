import json
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

    @classmethod
    def decode(cls, coords_packed: bytes):
        x_packed = coords_packed[0:2]
        y_packed = coords_packed[2:4]

        x_unpacked = int.from_bytes(x_packed, byteorder="big", signed=False)
        y_unpacked = int.from_bytes(y_packed, byteorder="big", signed=False)

        return cls(x_unpacked, y_unpacked)

    def __str__(self):
        return f"<Position({self.x}, {self.y})>"


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

    @classmethod
    def decode(cls, data: bytes):

        Log.udp_content("Event data", list(data))

        return data


class Hello(Event):
    def __init__(self, message: str):
        super().__init__()

        self.ask = True
        self.message = message

    def serialize(self):
        packet_type = super().serialize()

        content = self.message.encode()

        Log.udp_content("Packet type", list(packet_type))
        Log.udp_content("Content", list(content))

        data = packet_type + content

        Log.notice(f"Length: {len(data)}")

        return data

    @classmethod
    def decode(cls, data: bytes):
        json_str = data.decode('ascii')

        Log.notice("Hello event decoded")

        try:
            obj = json.loads(json_str)
            Log.notice(obj)
        except AttributeError:
            Log.notice("Error decoding JSON")

        return cls(json_str)


class Movement(Event):
    id = 1

    def __init__(self, from_point: Position, to_point: Position):
        super().__init__(self.id)

        self.ask = True

        self.from_point = from_point
        self.to_point = to_point

    def serialize(self):
        packet_type = super().serialize()

        from_position = self.from_point.serialize()
        to_position = self.to_point.serialize()

        Log.udp_content("Packet type", list(packet_type))
        Log.udp_content("From", list(from_position))
        Log.udp_content("To", list(to_position))

        data = packet_type + from_position + to_position

        return data

    @classmethod
    def decode(cls, data: bytes):
        from_point_bytes = data[0:4]
        to_point_bytes = data[4:8]

        Log.udp_content("From", list(from_point_bytes))
        Log.udp_content("To",   list(to_point_bytes))

        from_position = Position.decode(from_point_bytes)
        to_position = Position.decode(to_point_bytes)

        return cls(from_position, to_position)

    def __str__(self):
        return f"<events.Movement [{self.from_point}] -> [{self.to_point}] >"


events = [Movement, Hello]
