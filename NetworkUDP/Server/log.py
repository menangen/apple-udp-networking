import coloredlogs
import logging
import verboselogs
import sys
import argparse


class Log:
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='?', type=str)
    parser.add_argument(
        "--debug", help="enable debug messages to file", action="store_true")
    args = parser.parse_args()

    Logger = verboselogs.VerboseLogger(__name__)

    coloredlogs.install(
        level=logging.DEBUG,
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

    log_to_file = logging.FileHandler(filename=args.file or '/Volumes/RAMDisk/udp.log')
    log_to_file.setLevel(logging.DEBUG if args.debug else logging.INFO)
    log_to_file.setFormatter(
        logging.Formatter(
            fmt='%(asctime)s %(levelname)s:    %(message)s',
            datefmt='%H:%M:%S')
    )
    Logger.addHandler(log_to_file)

    @classmethod
    def udp_content(cls, name, content):
        cls.Logger.debug(f"\t({content})\t >>\t{name}")

    @classmethod
    def variable(cls, template: str, object_to_log, level=0):
        if level:
            cls.Logger.info(f"{template} = {object_to_log}")
        else:
            cls.Logger.verbose(f"{template} = {object_to_log}")

    @classmethod
    def sending_integer(cls, number: int, ip: str):
        cls.Logger.debug(f"Sending Data = {number}... to {ip}")

    @classmethod
    def receiving_integer(cls, data: bytearray, addr: tuple):
        # cls.Logger.verbose("_________________")
        cls.Logger.debug(f"Received message: {data}, from {addr}")

    @classmethod
    def request_end(cls):
        cls.Logger.verbose(">>>>>>>\n")

    @classmethod
    def save_packet_id(cls, packet_id, normal=False):
        if normal:
            cls.Logger.success(f"[ Saving #{packet_id} ]")
        else:
            cls.Logger.error(f"[Error Saving #{packet_id} ]")
