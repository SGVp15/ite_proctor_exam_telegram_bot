import logging

from config import SYSTEMLOG

file_log = logging.FileHandler(SYSTEMLOG)
console_out = logging.StreamHandler()


def configure_logging(level=logging.WARNING):
    logging.basicConfig(
        handlers=(file_log, console_out),
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )


configure_logging()
log = logging.getLogger(__name__)
