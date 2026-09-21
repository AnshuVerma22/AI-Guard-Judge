import logging
import os
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "api.log")


os.makedirs(LOG_DIR, exist_ok=True)


logger = logging.getLogger("ai_guard_judge")
logger.setLevel(logging.INFO)


if not logger.handlers:

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()


    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )


    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)


    logger.addHandler(file_handler)
    logger.addHandler(console_handler)