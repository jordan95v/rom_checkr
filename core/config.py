from logging import DEBUG
from core.pylog import Pylog

__all__: list[str] = ["logger"]

logger: Pylog = Pylog(name="rom_checkr", level=DEBUG)
