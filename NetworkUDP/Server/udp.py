import socket
from log import Log

from typing import Tuple


class Socket:
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5000
    BUFFER = 64

    def __init__(self, ip: str = UDP_IP, port: int = UDP_PORT):

        self.udpSocket = socket.socket(
            socket.AF_INET,     # Internet
            socket.SOCK_DGRAM)  # UDP

        self.udpSocket.bind((ip, port))
        Log.notice(f"Binding UDP socket on {port}")

    def read(self):
        data, addr = self.udpSocket.recvfrom(self.BUFFER)  # buffer size is 1024 bytes
        Log.receiving_bytes(data, addr)

        return data, addr

    def send(self, data: bytes, address: Tuple):
        Log.notice(f"Sending {len(data)} bytes to {address[0]}")
        self.udpSocket.sendto(data, address)
