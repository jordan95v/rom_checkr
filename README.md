<h1>No-Intro ROM Checkr</h1>

`no-intro-rom-checkr` is a CLI utility that validates ROM files against a No-Intro XML DAT.

It scans a folder of ROMs and, for each file:

- Finds a `<game>` entry whose `name` matches the ROM filename without extension.
- Prefers SHA256 validation when SHA256 hashes exist in the DAT.
- Falls back to MD5 validation when SHA256 is not available.
- Reports confidence based on matching dump count.

<h2>Table of Contents</h2>

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How matching works](#how-matching-works)
- [Running tests](#running-tests)
- [License](#license)

## Requirements

- Python 3.13+

## Installation

```bash
# Using uv
you@machine:~$ uv sync --no-dev

# Using pip and venv
you@machine:~$ python -m venv .venv
you@machine:~$ source .venv/bin/activate  # Windows: .venv\Scripts\activate
(venv) you@machine:~$ pip install .
```

For development (tests + tooling):

```bash
# Using uv
you@machine:~$ uv sync

# Using pip and venv
(venv) you@machine:~$ pip install -e .[dev]
```

## Usage

Run the CLI by passing:

- `--path`: directory containing ROM files.
- `--xml`: path to a No-Intro XML DAT file.

```bash
# Using uv
you@machine:~$ uv run python -m core --path /path/to/roms --xml /path/to/no-intro.xml

# Using pip and venv
(venv) you@machine:~$ python -m core --path /path/to/roms --xml /path/to/no-intro.xml
```

### Output Meaning

For each file in the folder:

- `trusted with N dumps` when `N >= 2`
- `questionable with only 1 dump` when `N == 1`
- `invalid` when `N == 0`

Non-file entries in the folder (subdirectories, etc.) are skipped.

## How Matching Works

`NoIntroCheckr.check_rom` compares one ROM against the XML DAT:

1. Uses the ROM stem (filename without extension) to find matching game entries:
   - Example: `Pokemon.gba` matches `<game name="Pokemon">`.
2. If matching entries provide SHA256 values, computes the ROM SHA256 and counts matches.
3. Otherwise, if entries provide MD5 values, computes ROM MD5 and counts matches.
4. If neither hash exists, returns `0`.

The returned integer is the number of matching dumps in the XML and drives the CLI confidence message.

## Running Tests

```bash
# Using uv
you@machine:~$ uv run pytest

# Using pip and venv
(venv) you@machine:~$ pytest
```

The default pytest configuration includes coverage output for the `core` package.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).