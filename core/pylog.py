import sys
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    Formatter,
    Logger,
    LogRecord,
    StreamHandler,
    makeLogRecord,
)

__all__: list[str] = ["Pylog"]


class AnsiFormatter(Formatter):
    LEVEL_COLOR: dict[int, str] = {  # noqa: RUF012
        DEBUG: "\033[92m",
        INFO: "\033[94m",
        WARNING: "\033[93m",
        ERROR: "\033[91m",
        CRITICAL: "\033[95m",
    }
    RESET_COLOR: str = "\033[0m"

    def format(self, record: LogRecord) -> str:
        record = makeLogRecord(record.__dict__)
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
