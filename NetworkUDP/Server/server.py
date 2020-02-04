import socket
from network import NetworkData
from log import Log
from binascii import hexlify as tohex


class UDPServer:
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5000
    BUFFER = 16

    def __init__(self, ip: str = UDP_IP, port: int = UDP_PORT):

        self.udpSocket = socket.socket(
            socket.AF_INET,     # Internet
            socket.SOCK_DGRAM)  # UDP

        self.udpSocket.bind((ip, port))
        print("Serving on", ip, port)

        self.counterPacket = 0

        while True:
            try:
                data, addr = self.udpSocket.recvfrom(self.BUFFER)  # buffer size is 1024 bytes
                Log.receiving_bytes(data, addr)

                self.process(data, addr)

            except KeyboardInterrupt:
                print("\tClosed by an Interrupt")
                break

    def process(self, data: bytes, from_addr):

        Log.variable("counterPacket", self.counterPacket, level=1)

        if data != b"getLast":
            Log.variable("Processing data", tohex(data).upper())
            incoming_number = NetworkData.to_int(data)

            Log.udp_content("incoming_number", incoming_number)

            if incoming_number:

                Log.save_packet_id(incoming_number, self.counterPacket + 1 == incoming_number)

            self.counterPacket += 1
        else:
            Log.notice("Processing [ getLast ] message")

        Log.sending_integer(self.counterPacket, from_addr[0])

        self.udpSocket.sendto(
            NetworkData.to_bytes(self.counterPacket),
            from_addr
        )

        Log.request_end()