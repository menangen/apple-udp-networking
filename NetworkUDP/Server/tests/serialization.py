from events import Movement, Position

FROM = Position(1, 65534)
TO = Position(1, 65535)

e = Movement(FROM, TO)
data = e.serialize()

print(f"data ({len(data)}): {list(data)}")
