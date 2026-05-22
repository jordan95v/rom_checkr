from pathlib import Path
import pytest
from lxml.etree import _ElementTree, parse
from core.checkr import NoIntroCheckr

__all__: list[str] = ["TestNoIntroCheckr"]


class TestNoIntroCheckr:
    XML: _ElementTree = parse(source=Path("tests/samples/fake_dump.xml"))

    @pytest.mark.parametrize(
        argnames="rom,expected",
        argvalues=[
            (Path("tests/samples/fake_game_md5.gba"), 1),
            (Path("tests/samples/fake_game_sha256.gba"), 2),
            (Path("tests/samples/fake_game_not_found.gba"), 0),
        ],
    )
    def test_check_rom(self, rom: Path, expected: int) -> None:
        result: int = NoIntroCheckr.check_rom(rom=rom, tree=self.XML)
        assert result == expected
