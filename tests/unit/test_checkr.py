from pathlib import Path
import pytest
from core.checkr import NoIntroCheckr

__all__: list[str] = ["TestNoIntroCheckr"]


class TestNoIntroCheckr:
    @pytest.mark.parametrize(
        argnames="rom,expected",
        argvalues=[
            (Path("tests/samples/fake_game_md5.gba"), True),
            (Path("tests/samples/fake_game_sha256.gba"), True),
            (Path("tests/samples/fake_game_not_found.gba"), False),
        ],
    )
    def test_ckeck_rom(self, rom: Path, expected: bool) -> None:
        checkr: NoIntroCheckr = NoIntroCheckr()
        result: bool = checkr.check_rom(
            rom=Path(rom), xml=Path("tests/samples/fake_dump.xml")
        )
        assert result is expected
