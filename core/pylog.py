import sys
from logging import Formatter, Logger, StreamHandler, LogRecord

__all__: list[str] = ["Pylog"]


class AnsiFormatter(Formatter):
    LEVEL_COLOR: dict[int, str] = {
        10: "\033[92m",  # DEBUG - Green
        20: "\033[94m",  # INFO - Blue
        30: "\033[93m",  # WARNING - Yellow
        40: "\033[91m",  # ERROR - Red
        50: "\033[95m",  # CRITICAL - Magenta
    }
    RESET_COLOR: str = "\033[0m"

    def format(self, record: LogRecord) -> str:
        level_color: str = self.LEVEL_COLOR.get(record.levelno, self.RESET_COLOR)
        record.levelname = f"{level_color}{record.levelname}{self.RESET_COLOR}"
        return super().format(record)


class Pylog(Logger):
    def __init__(self, name: str, level: int) -> None:
        super().__init__(name=name, level=level)
        handler: StreamHandler = StreamHandler(stream=sys.stdout)
        formatter: Formatter = AnsiFormatter(
            fmt="[%(levelname)s][%(asctime)s][%(filename)s] - %(message)s"
        )
        handler.setLevel(level=level)
        handler.setFormatter(fmt=formatter)
        self.addHandler(hdlr=handler)
