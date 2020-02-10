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

    def __init__(self, identificator: int):
        self.id = identificator

    def serialize(self):
        # 8-bit packet type
        _flag = self.ask << 7
        packet_id = _flag | self.id

        return packet_id.to_bytes(1, byteorder="big", signed=False)


class Movement(Event):
    id = 1

    def __init__(self, from_point: Position, to_point: Position):
        super().__init__(self.id)

        self.ask = True

        self._from = from_point
        self._to = to_point

    def serialize(self):
        packet_type = super().serialize()

        print("Packet type:", list(packet_type))

        from_position = self._from.serialize()
        to_position = self._to.serialize()

        print("From:", list(from_position))
        print("To:", list(to_position))

        return packet_type + from_position + to_position
