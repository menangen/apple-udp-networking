import coloredlogs, logging
import sys

class Network:
    DEBUG_PACKET = False
    DEBUG_SAVE = False

    Logger = logging.getLogger(__name__)
    coloredlogs.install(
        level='DEBUG',
        logger=Logger,
        stream=sys.stdout,
        isatty=True,
        datefmt='%H:%M:%S %d %B',
        fmt="[%(levelname)s] %(message)s \t |%(asctime)s",
        field_styles={
            'asctime': {'color': 'yellow'},
            'hostname': {'color': 'magenta'},
            'levelname': {'color': 'black', 'bold': True},
            'name': {'color': 'blue'},
            'programname': {'color': 'cyan'}
        }
    )

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
        cls.Logger.debug("Sending Data = {0}... to {1}".format(number, ip))

    @classmethod
    def log_receiving_integer(cls, data: bytearray, addr: tuple):
        cls.log("_________________")
        cls.Logger.debug(f"Received message: {data}, from {addr}")

    @classmethod
    def log_request_end(cls):
        cls.log(">>>>>>>")

    @classmethod
    def save_packet_id(cls, packet_id, normal = False):
        cls.DEBUG_SAVE = True

        template = "[ Saving #{} ]" if normal else "[ (!!) ErrorSaving #{} ]"

        record = template.format(packet_id)
        tabs_tmpl = "\t\t"
        cls.log(tabs_tmpl + record)
