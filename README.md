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

## License

[MIT](LICENSE)

## Author

[norad32](https://github.com/norad32)
