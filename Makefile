# Default goal
.DEFAULT_GOAL := help

# Detect platform specifics
ifeq ($(OS),Windows_NT)
  VENV_BIN := .venv/Scripts
  VENV_PY  := $(VENV_BIN)/python.exe
  EXE      := dist/ImPython.exe
else
  VENV_BIN := .venv/bin
  VENV_PY  := $(VENV_BIN)/python
  EXE      := dist/ImPython
endif

PY  := $(VENV_PY)
PIP := $(PY) -m pip

PKG  := im_python
SPEC := installer/ImPython.spec

# ----- Helpers -----
.PHONY: help
help:
	@echo ""
	@echo "Targets:"
	@echo "  venv         Create local virtualenv (.venv)"
	@echo "  install      Install project in dev mode (+ dev tools)"
	@echo "  tools        Ensure build/test tools are installed"
	@echo "  test         Run pytest (with coverage)"
	@echo "  lint         Run ruff (lint) + ruff format --check"
	@echo "  typecheck    Run mypy on src/"
	@echo "  wheel        Build wheel and sdist into ./dist"
	@echo "  exe          Build one-file executable via PyInstaller spec"
	@echo "  run          Run CLI help to sanity-check"
	@echo "  clean        Remove build artifacts"
	@echo "  distclean    Also remove .venv"
	@echo ""

# ----- Environment -----
.PHONY: venv
venv: $(VENV_PY)

$(VENV_PY):
	python -m venv .venv
	$(VENV_PY) -m pip install -U pip

# Ensure dev tools exist (separate from editable install)
.PHONY: tools
tools: venv
	$(PIP) install -U build pyinstaller pytest pytest-cov ruff mypy

.PHONY: install
install: venv
	-$(PIP) install -e ".[dev,gui]" || true
	$(PIP) install -e .

# ----- Quality / Tests -----
.PHONY: test
test: tools
	$(PY) -m pytest --cov=$(PKG) --cov-report=term-missing -vv

.PHONY: lint
lint: tools
	$(PY) -m ruff check .
	$(PY) -m ruff format --check

.PHONY: typecheck
typecheck: tools
	$(PY) -m mypy src/$(PKG)

# ----- Build artifacts -----
.PHONY: wheel
wheel: tools
	$(PY) -m build

.PHONY: exe
exe: tools
	$(PY) -m PyInstaller $(SPEC)

# ----- Run / Debug -----
.PHONY: run
run: venv
	$(PY) -m $(PKG) --help || true
	@echo "Executable (if built): $(EXE)"

# ----- Cleanups -----
.PHONY: clean
clean:
	- python - <<-'PY'
	import glob, os, shutil, pathlib
	for p in ['build','dist','.pytest_cache','.mypy_cache']:
		shutil.rmtree(p, ignore_errors=True)
	for f in glob.glob('*.spec'):
		# keep only if it's literally in CWD and named ImPython.spec
		if pathlib.Path(f).name != 'ImPython.spec':
			try: os.remove(f)
			except FileNotFoundError: pass
	for p in pathlib.Path('.').rglob('__pycache__'):
		shutil.rmtree(p, ignore_errors=True)
	PY

.PHONY: distclean
distclean: clean
	- python - <<'PY'
	import shutil
	shutil.rmtree('.venv', ignore_errors=True)
	PY
