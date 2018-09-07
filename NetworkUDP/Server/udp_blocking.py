import socket
# from time import sleep

from network import Network

class UDPServer:
    UDP_IP = "192.168.1.5"
    UDP_PORT = 5000

    def __init__(self, ip: str = UDP_IP, port: int = UDP_PORT):
        self.udpSocket = socket.socket(
            socket.AF_INET,     # Internet
            socket.SOCK_DGRAM)  # UDP
        self.udpSocket.bind((ip, port))

        Network.DEBUG_PACKET = True

        print("Serving on", ip, port)

        self.counterPacket = 0

        while True:
            try:
                data, addr = self.udpSocket.recvfrom(1024)  # buffer size is 1024 bytes
                Network.log_receiving_integer(data, addr)

                self.process(data, addr)

            except KeyboardInterrupt:
                print("\tClosed by an Interrupt")
                break


    def process(self, data: bytes, from_addr):

        Network.log_variable("Processing data", data)
        Network.log_variable("counterPacket", self.counterPacket)


        if data != b"getLast":
            # TODO save to log
            incoming_number = Network.bytes_to_int(data)

            Network.log_level_1("incoming_number", incoming_number)

            if incoming_number:
                if self.counterPacket == incoming_number:

                    Network.save_packet_id(incoming_number)

                self.counterPacket += 1

        # sleep(0.05)  # 50 ms sleep

        Network.log_sending_integer(self.counterPacket, from_addr[0])

        self.udpSocket.sendto(
            Network.int_to_bytes(self.counterPacket),
            from_addr
        )

        Network.log_request_end()

UDPServer()