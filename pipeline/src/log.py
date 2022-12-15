import os
import sys

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="{time} | {level} | {message} | {extra}",
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
)


def get_logger():
    return logger
