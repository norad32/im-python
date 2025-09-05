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
	@echo "  test         Run pytest (with coverage)"
	@echo "  lint         Run ruff (lint) + ruff format --check"
	@echo "  typecheck    Run mypy on src/"
	@echo "  wheel        Build wheel and sdist into ./dist"
	@echo "  exe          Build one-file executable via PyInstaller spec"
	@echo "  clean        Remove build artifacts"
	@echo ""

.PHONY: venv
venv: $(VENV_PY)

$(VENV_PY):
	python -m venv .venv
	$(VENV_PY) -m pip install -U pip


.PHONY: install
install: venv
	-$(PIP) install -e ".[dev,gui]" || true
	$(PIP) install -e .

.PHONY: test
test: install
	$(PY) -m pytest --cov=$(PKG) --cov-report=term-missing -vv

.PHONY: lint
lint: install
	$(PY) -m ruff check .
	$(PY) -m ruff format --check

.PHONY: typecheck
typecheck: install
	$(PY) -m mypy src/$(PKG)

.PHONY: wheel
wheel: install
	$(PY) -m build

.PHONY: exe
exe: install
	$(PY) -m PyInstaller $(SPEC)

.PHONY: clean
clean:
	@set -euo pipefail; \
	spec="$(SPEC)"; \
	to_delete=(dist .venv build .mypy_cache .pytest_cache .ruff_cache .coverage I_m_Python.ini); \
	for p in "$${to_delete[@]}"; do \
	  if [[ -n "$$p" && ( -e "$$p" || -L "$$p" ) ]]; then \
	    echo "Removing $$p"; rm -rf -- "$$p"; \
	  else \
	    echo "Skipping $$p (not found)"; \
	  fi; \
	done
