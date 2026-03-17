<h1>No-Intro ROM Checkr</h1>

This is a CLI tool to check ROMs against the No-Intro database. 

<h2>Table of contents</h2>

- [Installation](#installation)
- [Usage](#usage)
  - [Running the tests](#running-the-tests)
- [License](#license)

## Installation

Run the following commands to install the project:

```bash
you@machine:~$ python -m venv venv
you@machine:~$ source venv/bin/activate # venv\Scripts\activate on Windows
(venv) you@machine:~$ pip install . # -e .[dev] for development
```

And you are ready to go!

## Usage

### Running the tests

Run the following command to run the tests:

```bash
(venv) you@machine:~$ pytest
```

The tests will run and show the results in the terminal, including the coverage.

The default configuration is to run the tests with coverage. You can change this by modifying the `pyproject.toml` file in the `[tool.pytest.ini_options]` section.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.