import coloredlogs
import logging
import verboselogs
import sys


class Log:
    DEBUG_PACKET = False
    DEBUG_SAVE = False

    verboselogs.install()
    logging.basicConfig(
        format='%(levelname)s:    %(message)s',
        filename='/Volumes/RAMDisk/udp.log',
        level=logging.DEBUG
    )
    Logger = logging.getLogger(__name__)

    coloredlogs.install(
        level='DEBUG',
        logger=Logger,
        stream=sys.stdout,
        isatty=True,
        datefmt='%H:%M:%S %d %B',
        level_styles={
            'critical': {'color': 'red', 'bold': True}, 'debug': {'color': 'blue'},
            'error': {'color': 'red'}, 'info': {}, 'notice': {'color': 'magenta'},
            'spam': {'color': 'green', 'faint': True}, 'success': {'color': 'green', 'bold': True},
            'verbose': {'color': 'white'}, 'warning': {'color': 'yellow'}},
        fmt="%(asctime)s[%(levelname)s] %(message)s \t",
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
    def udp_content(cls, name, content):
        cls.Logger.success(f"{name}: {content}")

    @classmethod
    def variable(cls, template: str, object_to_log, level=0):
        cls.Logger.verbose(
            f"\t({object_to_log})\t >>\t{template}"
            if level else
            f"{template} = {object_to_log}"
        )

    @classmethod
    def sending_integer(cls, number: int, ip: str):
        cls.Logger.debug(f"Sending Data = {number}... to {ip}")

    @classmethod
    def receiving_integer(cls, data: bytearray, addr: tuple):
        cls.Logger.verbose("_________________")
        cls.Logger.debug(f"Received message: {data}, from {addr}")

    @classmethod
    def request_end(cls):
        cls.Logger.verbose(">>>>>>>\n")

    @classmethod
    def save_packet_id(cls, packet_id, normal=False):
        tabs_tmpl = "\t\t"
        if normal:
            cls.Logger.success(f"{tabs_tmpl}[ Saving #{packet_id} ]")
        else:
            cls.Logger.critical(f"[ (!!) ErrorSaving #{packet_id} ]")
