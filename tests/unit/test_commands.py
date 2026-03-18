from pathlib import Path
from unittest.mock import MagicMock
from core.checkr import NoIntroCheckr
from pytest_mock import MockerFixture
from typer.testing import CliRunner
from core.__main__ import app


class TestCommands:
    def test_check_folder(self, mocker: MockerFixture) -> None:
        runner: CliRunner = CliRunner()
        check_rom_mock: MagicMock = mocker.patch.object(
            target=NoIntroCheckr, attribute="check_rom", side_effect=[1, 2, 0]
        )
        runner.invoke(
            app=app,
            args=[
                "--path",
                "tests/samples",
                "--xml",
                "tests/samples/fake_dump.xml",
            ],
        )
        assert check_rom_mock.call_count == 4

    def test_check_folder_non_file(self, mocker: MockerFixture, tmp_path: Path) -> None:
        runner: CliRunner = CliRunner()
        check_rom_mock: MagicMock = mocker.patch.object(
            target=NoIntroCheckr, attribute="check_rom", return_value=0
        )
        folder: Path = tmp_path / "folder"
        folder.mkdir()
        runner.invoke(
            app=app,
            args=[
                "--path",
                tmp_path.as_posix(),
                "--xml",
                "tests/samples/fake_dump.xml",
            ],
        )
        assert check_rom_mock.call_count == 0
