# I'm Python

[![Tests, lint & typecheck](https://github.com/norad32/im-python/actions/workflows/test-lint-typecheck.yaml/badge.svg?branch=main)](https://github.com/norad32/im-python/actions/workflows/test-lint-typecheck.yaml)
[![Release build](https://github.com/norad32/im-python/actions/workflows/release.yaml/badge.svg)](https://github.com/norad32/im-python/actions/workflows/release.yaml)

A starter desktop GUI built with [imgui-bundle](https://pypi.org/project/imgui-bundle/). It includes a CLI, persistent GUI preferences, a GUI log panel, tests, and GitHub Actions checks. Requires Python 3.14 or newer.

## Run locally

On Linux, create an environment and install the GUI extra:

```bash
python3.14 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[gui]"
python -m im_python
```

On Windows PowerShell:

```powershell
py -3.14 -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -e ".[gui]"
python -m im_python
```

## Develop and test

Install the development and GUI dependencies, then run the checks used in CI:

```bash
python -m pip install -e ".[dev,gui]"
pytest --cov=im_python --cov-report=term-missing --cov-fail-under=60 -vv
ruff check --ignore BLE001 --output-format=github .
ruff format --check .
mypy src/ tests/
```

`BLE001` is excluded because the logger and config code intentionally catch errors around cleanup and malformed user settings. The other Ruff checks, formatting, type checking, and the 60% coverage minimum are blocking CI checks.

For Make targets, run `make` to see the available commands.

## Release artifacts

Pushing a `v*` tag triggers the release workflow. It builds a Python wheel and a Linux PyInstaller executable, then attaches both to the GitHub release. The executable is Linux-only.

## Project layout

```text
.github/workflows/   CI and tagged-release workflows
installer/           PyInstaller specification
scripts/             Direct app launcher used by packaging
src/im_python/       CLI, GUI, logging, and bundled assets
tests/               Unit tests
pyproject.toml       Package metadata and optional dependencies
Makefile             Local development and packaging commands
```

## Credits

This project uses the following open-source libraries and tools:

| Library | Purpose | License |
|---------|---------|---------|
| **[Dear ImGui](https://github.com/ocornut/imgui)** | Immediate-mode GUI foundation used through imgui-bundle | [MIT](https://github.com/ocornut/imgui/blob/master/LICENSE.txt) |
| **[imgui-bundle](https://github.com/pthom/imgui_bundle)** | Python bindings and GUI application framework | [MIT](https://github.com/pthom/imgui_bundle/blob/main/LICENSE) |
| **[Typer](https://github.com/fastapi/typer)** | Command-line interface | [MIT](https://github.com/fastapi/typer/blob/master/LICENSE) |
| **[platformdirs](https://github.com/tox-dev/platformdirs)** | Platform-specific user configuration and log directories | [MIT](https://github.com/tox-dev/platformdirs/blob/main/LICENSE) |
| **[pytest](https://github.com/pytest-dev/pytest)** | Test framework | [MIT](https://github.com/pytest-dev/pytest/blob/main/LICENSE) |
| **[pytest-cov](https://github.com/pytest-dev/pytest-cov)** | Test coverage reporting | [MIT](https://github.com/pytest-dev/pytest-cov/blob/master/LICENSE) |
| **[Ruff](https://github.com/astral-sh/ruff)** | Linting and formatting | [MIT](https://github.com/astral-sh/ruff/blob/main/LICENSE) |
| **[mypy](https://github.com/python/mypy)** | Static type checking | [MIT](https://github.com/python/mypy/blob/master/LICENSE) |
| **[build](https://github.com/pypa/build)** | Python package building | [MIT](https://github.com/pypa/build/blob/main/LICENSE) |
| **[Hatchling](https://github.com/pypa/hatch)** | PEP 517 package build backend | [MIT](https://github.com/pypa/hatch/blob/master/LICENSE.txt) |
| **[PyInstaller](https://github.com/pyinstaller/pyinstaller)** | Linux executable packaging | [GPL-2.0-or-later with Bootloader Exception](https://github.com/pyinstaller/pyinstaller/blob/develop/COPYING.txt) |
| **[Python standard library](https://docs.python.org/3/library/)** | Configuration parsing, logging, threading, and other built-in functionality | [PSF License](https://docs.python.org/3/license.html) |

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) for details.

## Author

[norad32](https://github.com/norad32)
