from pathlib import Path
from typing import Annotated
from lxml.etree import _ElementTree, parse
from typer import Option, Typer
from core.checkr import NoIntroCheckr
from core.config import logger

app: Typer = Typer()


@app.command()
def check_folder(
    path: Annotated[
        Path,
        Option(
            help="The path to the folder containing the roms to check.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
        ),
    ],
    xml: Annotated[
        Path,
        Option(
            help="The path to the XML file containing the expected checksums.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
):
    tree: _ElementTree = parse(source=xml)
    for rom in sorted(path.iterdir()):
        if not rom.is_file():
            logger.warning(msg=f"{rom.name} is not a file, skipping.")
            continue
        try:
            dump_amount: int = NoIntroCheckr.check_rom(rom=rom, tree=tree)
        except OSError:
            logger.warning(msg=f"{rom.name} could not be read, skipping.")
            continue
        if dump_amount >= 2:
            logger.info(msg=f"{rom.name} is trusted with {dump_amount} dumps.")
        elif dump_amount == 1:
            logger.warning(msg=f"{rom.name} is questionable with only 1 dump.")
        else:
            logger.error(msg=f"{rom.name} is invalid.")


if __name__ == "__main__":  # pragma: no cover
    app()
