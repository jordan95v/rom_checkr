from click.testing import Result
from pathlib import Path
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from typer.testing import CliRunner
from core.__main__ import app
from core.checkr import NoIntroCheckr


__all__: list[str] = ["TestCommands"]


class TestCommands:
    def test_check_folder(self, mocker: MockerFixture, tmp_path: Path) -> None:
        runner: CliRunner = CliRunner()
        for name in ["rom_a.gba", "rom_b.gba", "rom_c.gba"]:
            (tmp_path / name).write_bytes(data=b"")
        check_rom_mock: MagicMock = mocker.patch.object(
            target=NoIntroCheckr, attribute="check_rom", side_effect=[1, 2, 0]
        )
        runner.invoke(
            app=app,
            args=[
                "--path",
                tmp_path.as_posix(),
                "--xml",
                "tests/samples/fake_dump.xml",
            ],
        )
        assert check_rom_mock.call_count == 3

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

    def test_check_folder_unreadable_rom(
        self, mocker: MockerFixture, tmp_path: Path
    ) -> None:
        runner: CliRunner = CliRunner()
        (tmp_path / "bad.gba").write_bytes(data=b"")
        mocker.patch.object(
            target=NoIntroCheckr, attribute="check_rom", side_effect=OSError
        )
        result: Result = runner.invoke(
            app=app,
            args=[
                "--path",
                tmp_path.as_posix(),
                "--xml",
                "tests/samples/fake_dump.xml",
            ],
        )
        assert result.exit_code == 0
