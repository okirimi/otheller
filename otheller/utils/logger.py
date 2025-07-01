import logging
from pathlib import Path


def setup_logger(level: str) -> logging.Logger:
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        msg = f"Invalid log level: {level}"
        raise TypeError(msg)

    file_path = "./logs/otheller.log"

    # Create log folder if not exists
    Path("./logs").mkdir(exist_ok=True)

    file_handler = logging.FileHandler(file_path)

    logging.basicConfig(
        level=numeric_level,
        # [2025-06-26 20:13:26 - <filename>:1024 - DEBUG] <message>
        format="[%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s] %(message)s",
        handlers=[
            file_handler,  # output logs to a log file
        ],
    )

    # logging.getLogger() returns a singleton per name;
    # no need to manage logger instances manually
    return logging.getLogger(__name__)
