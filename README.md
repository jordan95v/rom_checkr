# No-Intro ROM Checkr

![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

`no-intro-rom-checkr` is a CLI utility that validates ROM files against a [No-Intro](https://no-intro.org/) XML DAT file.

## Features

- Matches ROMs by filename stem against `<game name="...">` entries in the DAT.
- Prefers **SHA256** validation when available; falls back to **MD5**.
- Reports confidence level based on the number of matching dumps found.
- Skips non-file entries (subdirectories, symlinks, etc.) with a warning.

## Table of contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How Matching Works](#how-matching-works)
- [Running Tests](#running-tests)
- [License](#license)

## Requirements

- Python 3.11+

## Installation

```bash
# Using uv
uv sync --no-dev

# Using pip + venv
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install .
```

For development (tests + tooling):

```bash
# Using uv
uv sync

# Using pip + venv
pip install -e .[dev]
```

## Usage

```bash
# Using uv
uv run python -m core --path /path/to/roms --xml /path/to/no-intro.xml

# Using pip + venv
python -m core --path /path/to/roms --xml /path/to/no-intro.xml
```

### Options

| Option | Description |
|--------|-------------|
| `--path` | Directory containing ROM files |
| `--xml`  | Path to the No-Intro XML DAT file |

### Example output

```
INFO     Pokemon Red (USA).gb is trusted with 3 dumps.
WARNING  Homebrew.gb is questionable with only 1 dump.
WARNING  Unknown.gb is invalid.
WARNING  saves/ is not a file, skipping.
```

### Confidence levels

| Result | Condition |
|--------|-----------|
| `trusted with N dumps` | N ≥ 2 matching dumps |
| `questionable with only 1 dump` | exactly 1 matching dump |
| `invalid` | 0 matching dumps |

## How matching works

`NoIntroCheckr.check_rom` compares a ROM against the XML DAT in three steps:

1. **Name lookup** — uses the ROM stem (filename without extension) to find `<game>` entries.
   - `Pokemon Red (USA).gb` → looks for `<game name="Pokemon Red (USA)">`.
2. **SHA256 check** — if any matching entry has SHA256 hashes, computes the ROM's SHA256 and counts exact matches.
3. **MD5 fallback** — if no SHA256 hashes exist, computes MD5 and counts matches instead.
4. Returns `0` if the game name is not found or no hashes match.

The returned count drives the confidence message logged by the CLI.

## Running tests

```bash
# Using uv
uv run pytest

# Using pip + venv
pytest
```

Coverage is reported automatically for the `core` package via the default pytest configuration.

## License

MIT — see [LICENSE](LICENSE).
