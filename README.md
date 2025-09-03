# I'm Python

A Python project template that uses **[imgui-bundle](https://pypi.org/project/imgui-bundle/)** for GUI,
with all configuration centralized in a **`pyproject.toml`** (TOML — "tom").  
It’s set up for Linux, Windows, and CI via GitHub Actions.

---

## Quickstart

### System prerequisites

**Linux (Arch)** – make sure you have graphics drivers and common X11/Wayland/OpenGL runtime libs installed. On Arch, you likely already do, otherwise for typical desktop installs:
```bash
sudo pacman -S --needed base-devel python python-pip git
# (most systems already have the GL/X11 runtime libs required by imgui-bundle wheels)
```
> If you run Wayland-only, `imgui-bundle` still works thanks to its backends. The provided demo uses the `immapp` helper which handles windowing for you.

**Windows**
- Python 3.10–3.12 (64-bit) from python.org or the Store
- `git` if you’ll clone the repo

### Create and activate a virtual environment
```bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install (dev mode)
```bash
pip install --upgrade pip
pip install -e ."[dev]"
```

### Run the GUI demo
```bash
im-python
# or
python -m im_python
```

You should see a basic ImGui window.

### Run tests
```bash
pytest -vv
```

### Buil an executable

```bash
# Linux
pyinstaller scripts/run_app.py --onefile --name ImPython
# result: dist/ImPython

# Windows
pyinstaller scripts/run_app.py --onefile --windowed --name ImPython
# result: dist/ImPython
```
---

## Project layout
```
im-python/
├─ .github/
│  └─ workflows/
│     ├─ build-executable.yaml
│     └─ run-tests.yaml
├─ assets/
│  └─ app_settings/
│     └─ icon.png
├─ scripts/
│  └─ run_app.py 
├─ src/
│  └─ im_python/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ app.py
│     └─ cli.py
├─ tests/
│  └─ test_basic.py
├─ README.md
└─ pyproject.toml
```

---

## Author
[norad32](https://github.com/norad32)

---

## License
MIT
