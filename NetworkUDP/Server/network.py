

class Network:
    DEBUG_PACKET = False
    DEBUG_SAVE = False

    @classmethod
    def log(cls, *args):
        if cls.DEBUG_PACKET or cls.DEBUG_SAVE:
            print(*args)
            cls.DEBUG_SAVE = False

    @classmethod
    def int_to_bytes(cls, data, signed=False):
        return data.to_bytes(2, byteorder='little', signed=signed)

    @classmethod
    def bytes_to_int(cls, data, signed=False):
        return int.from_bytes(data, byteorder='little', signed=signed)

    @classmethod
    def log_variable(cls, template: str, object_to_log):
        cls.log(template + " = {}".format(object_to_log))

    @classmethod
    def log_level_1(cls, template: str, object_to_log):
        cls.log("\t({})\t >>\t".format(object_to_log) + template)

    @classmethod
    def log_sending_integer(cls, number: int, ip: str):
        cls.log("Sending Data = {0}... to {1}".format(number, ip))

    @classmethod
    def log_receiving_integer(cls, data: bytearray, addr: tuple):
        cls.log("_________________")
        cls.log("Received message:", data, "from", addr)

    @classmethod
    def log_request_end(cls):
        cls.log(">>>>>>>")

    @classmethod
    def save_packet_id(cls, id):
        cls.DEBUG_SAVE = True
        cls.log("\t..oo00\t[ Saving #{} ]\t00oo..".format(id))
