import socket

class UDPServer:
    UDP_IP = "192.168.1.6"
    UDP_PORT = 5000

    def __init__(self, ip: str = UDP_IP, port: int = UDP_PORT):
        self.udpSocket = socket.socket(
            socket.AF_INET,     # Internet
            socket.SOCK_DGRAM)  # UDP
        self.udpSocket.bind((ip, port))


        print("Serving on", ip, port)

        self.counterPacket = 1

        while True:
            try:
                data, addr = self.udpSocket.recvfrom(1024)  # buffer size is 1024 bytes
                print("Received message:", data, "from", addr)

                self.process(data, addr)

            except KeyboardInterrupt:
                print("\tClosed by an Interrupt")
                break


    def process(self, data: bytes, from_addr):
        print("Processing data:", data)

        print("sending Counter = {}".format(self.counterPacket))
        sending_content = self.counterPacket if data == b"getLast" else int(data) + 500

        self.udpSocket.sendto(
            sending_content.to_bytes(2, byteorder='big'),
            from_addr)
        print("Sending Counter = {0}... to {1}".format(sending_content, from_addr[0]))

        self.counterPacket += 1

UDPServer()