from hashlib import md5, sha256
from pathlib import Path
from lxml.etree import _ElementTree, parse
from core.config import logger

__all__: list[str] = ["NoIntroCheckr"]


class NoIntroCheckr:
    def check_rom(self, rom: Path, xml: Path) -> bool:
        """Checks the integrity of a ROM file against a No-Intro XML database.

        The method searches for the ROM's filename (stem) in the provided XML.
        It prioritizes SHA256 validation if available, falling back to MD5.
        Results and mismatches are recorded via the system logger.

        Args:
            rom: The path to the ROM file to be verified.
            xml: The path to the No-Intro XML database file.

        Raises:
            OSError: If the ROM or XML file cannot be read.
            lxml.etree.XMLSyntaxError: If the XML database is malformed.

        Returns:
            bool: True if the ROM's hash matches an entry in the database, False otherwise.
        """

        root: _ElementTree = parse(source=xml)
        if hashes := root.xpath(_path=f'.//game[@name="{rom.stem}"]//file/@sha256'):
            logger.debug(f"Checking {rom.name} using sha256 hashes")
            sha256_hash: str = sha256(string=rom.read_bytes()).hexdigest()
            total: int = hashes.count(sha256_hash)
            logger.debug(f"Hash {sha256_hash} found {total} times in the database")
        elif hashes := root.xpath(_path=f'.//game[@name="{rom.stem}"]//file/@md5'):
            logger.debug(f"Checking {rom.name} using md5 hashes")
            md5_hash: str = md5(string=rom.read_bytes()).hexdigest()
            total: int = hashes.count(md5_hash)
            logger.debug(f"Hash {md5_hash} found {total} times in the database")
        else:
            logger.error(f"No hashes found for {rom.name} in the database")
            return False
        return True
