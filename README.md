# I'm Python

A Python project template that uses **[imgui-bundle](https://pypi.org/project/imgui-bundle/)** for GUI, with all configuration centralized in a **`pyproject.toml`** (TOML — "tom").
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

### Makefile

Just run

```bash
make
```

to see how to use the project.

## Project layout

```
im-python/
├─ .github/
│  └─ workflows/
│     ├─ build.yaml
│     └─ test.yaml
├─ installer/
│  └─ ImPython.spec

├─ scripts/
│  └─ run_app.py
├─ src/
│  └─ im_python/
│     ├─ assets/
│     │  └─ app_settings/
│     │     └─ icon.png
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ cli.py
│     └─ gui.py
├─ tests/
│  └─ test_basic.py
├─ LICENSE
├─ Makefile
├─ pyproject.toml
└─ README.md
```

## Licene

[MIT](LICENSE)

## Author

[norad32](https://github.com/norad32)
