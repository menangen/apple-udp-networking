import coloredlogs
import logging
import verboselogs
import sys
import argparse
import platform


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
        datefmt='%H:%M:%S',
        level_styles={
            'critical': {'color': 'red', 'bold': True}, 'debug': {'color': 'green'},
            'error': {'color': 'red'}, 'info': {}, 'notice': {'color': 'red'},
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

    default_log_file = '/Volumes/RAMDisk/socket.log' if platform.system() == 'Darwin' else "socket.log"
    current_file_log = args.file or default_log_file

    # log_to_file = logging.FileHandler(filename=current_file_log)
    # log_to_file.setLevel(logging.DEBUG if args.debug else logging.INFO)
    # log_to_file.setFormatter(
    #     logging.Formatter(
    #         fmt='%(asctime)s %(levelname)s:    %(message)s',
    #         datefmt='%H:%M:%S')
    # )
    # Logger.addHandler(log_to_file)
    # Logger.verbose(f"Logging to {current_file_log}")

    @classmethod
    def notice(cls, template: str):
        cls.Logger.notice(template)

    @classmethod
    def success(cls, template: str):
        cls.Logger.success(template)

    @classmethod
    def udp_content(cls, name, content):
        cls.Logger.debug(f"\t{name}\t>>\t{content}")

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
    def receiving_bytes(cls, data: bytes, addr: tuple):
        cls.Logger.debug(f"Received UDP data: {list(data)}, from {addr}")

    @classmethod
    def request_end(cls):
        cls.Logger.verbose(">>>>>>>\n")

    @classmethod
    def save_packet_id(cls, packet_id, normal=False):
        if normal:
            cls.Logger.success(f"[ Saving #{packet_id} ]")
        else:
            cls.Logger.error(f"[Error Saving #{packet_id} ]")
