from collections.abc import Callable
from hashlib import md5, sha256
from pathlib import Path
from typing import Any
from lxml.etree import _ElementTree
from core.config import logger

__all__: list[str] = ["NoIntroCheckr"]


def _hash_file(path: Path, algo: Callable) -> str:
    h: Any = algo()
    with path.open(mode="rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class NoIntroCheckr:
    @staticmethod
    def check_rom(rom: Path, tree: _ElementTree) -> int:
        """Checks the integrity of a ROM file against a No-Intro XML database.

        Args:
            rom: The path to the ROM file to be verified.
            tree: A pre-parsed lxml ElementTree of the No-Intro XML database.

        Raises:
            OSError: If the ROM file cannot be read.

        Returns:
            int: The number of matching dumps found in the XML database for the ROM.
        """

        if hashes := tree.xpath(
            _path=".//game[@name=$name]//file/@sha256", name=rom.stem
        ):  # type: ignore
            logger.debug(msg=f"Checking {rom.name} using sha256 hashes")
            return hashes.count(_hash_file(path=rom, algo=sha256))
        elif hashes := tree.xpath(
            _path=".//game[@name=$name]//file/@md5", name=rom.stem
        ):  # type: ignore
            logger.debug(msg=f"Checking {rom.name} using md5 hashes")
            return hashes.count(_hash_file(path=rom, algo=md5))
        return 0
