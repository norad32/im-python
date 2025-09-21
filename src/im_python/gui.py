import sys
from pathlib import Path
from typing import Final, cast
from dataclasses import dataclass
from importlib.resources import files
from configparser import ConfigParser
from .app_logger import app_logger
from .app_logger.levels import Level
from .app_logger.gui_handler import GuiHandler

_logger = app_logger.get(__name__)


def _detect_app_name(default="im-python"):
    if getattr(sys, "frozen", False):
        return Path(sys.executable).stem

    if sys.argv and sys.argv[0]:
        name = Path(sys.argv[0]).stem
        if name and name not in ("-c", "<stdin>"):
            return name

    return (
        Path(globals().get("__file__", default)).stem
        if "__file__" in globals()
        else default
    )


def _get_config_path() -> Path:
    try:
        from platformdirs import user_config_dir

        config_dir = Path(user_config_dir(_detect_app_name()))
    except ImportError:
        config_dir = Path("config")
        _logger.error(f"No user log dir. Defaulting to {config_dir}")

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


WINDOW_TITLE: Final[str] = _detect_app_name("I'm Python")
DEFAULT_WINDOW_SIZE: Final[tuple[int, int]] = (1024, 768)

LOG_PANEL_TOGGLE_KEY: Final[str] = "§"
MIN_LOG_PANEL_HEIGHT: Final[int] = 148


@dataclass
class Config:
    window_title: str = WINDOW_TITLE
    window_size: tuple[int, int] = DEFAULT_WINDOW_SIZE


@dataclass
class State:
    log_handler: GuiHandler
    logs_panel_visible: bool = False
    logs_autoscroll: bool = True
    logs_count: int = 0


def _load_state(ini_path: Path, state: State) -> None:
    if not ini_path.exists():
        _logger.info(f"No config found at {ini_path}. Using defaults")
        return

    config = ConfigParser()

    try:
        config.read(ini_path)
        if config.has_section("State"):
            state.logs_panel_visible = config.getboolean(
                "State", "logs_panel_visible", fallback=state.logs_panel_visible
            )
            state.logs_autoscroll = config.getboolean(
                "State", "logs_autoscroll", fallback=state.logs_autoscroll
            )
    except Exception as e:
        _logger.warning("Could not read State from ini: %s", e)


def _save_state(ini_path: Path, state: State) -> None:
    ini_path.parent.mkdir(parents=True, exist_ok=True)
    cfg = ConfigParser()

    if ini_path.exists():
        try:
            cfg.read(ini_path)
        except Exception:
            cfg = ConfigParser()

    if not cfg.has_section("State"):
        cfg.add_section("State")
    cfg.set("State", "logs_panel_visible", "1" if state.logs_panel_visible else "0")
    cfg.set("State", "logs_autoscroll", "1" if state.logs_autoscroll else "0")

    with ini_path.open("w", encoding="utf-8") as f:
        cfg.write(f)


def _handle_log_panel_toggle_key(io, state: State) -> None:
    """Toggle the log panel on LOG_PANEL_TOGGLE_KEY when not typing in an input."""
    if io.want_text_input:
        return
    for codepoint in io.input_queue_characters:
        if codepoint == ord(LOG_PANEL_TOGGLE_KEY):
            state.logs_panel_visible = not state.logs_panel_visible
            break


def _render_log_panel(imgui, hello_imgui, state: State) -> None:
    """Render non-movable, height-resizable log panel, that sticks to the viewport bottom."""
    if not state.logs_panel_visible:
        return

    viewport = imgui.get_main_viewport()
    work_pos = viewport.work_pos
    work_size = viewport.work_size

    imgui.set_next_window_viewport(viewport.id_)
    imgui.set_next_window_pos(
        imgui.ImVec2(work_pos.x, work_pos.y + (2.0 / 3.0) * work_size.y),
        imgui.Cond_.first_use_ever,
    )
    imgui.set_next_window_size(
        imgui.ImVec2(work_size.x, work_size.y / 3.0),
        imgui.Cond_.first_use_ever,
    )

    imgui.set_next_window_size_constraints(
        imgui.ImVec2(work_size.x, MIN_LOG_PANEL_HEIGHT),
        imgui.ImVec2(work_size.x, work_size.y),
    )

    flags = imgui.WindowFlags_.no_move | imgui.WindowFlags_.no_docking

    if imgui.begin(f"Logs ({LOG_PANEL_TOGGLE_KEY})", None, flags):
        current_size = imgui.get_window_size()
        desired_width = work_size.x

        if abs(current_size.x - desired_width) > 0.5:
            imgui.set_window_size(imgui.ImVec2(desired_width, current_size.y))
            current_size = imgui.get_window_size()

        # Lock left edge and bottom to viewport
        desired_pos = imgui.ImVec2(
            work_pos.x, work_pos.y + work_size.y - current_size.y
        )
        imgui.set_window_pos(desired_pos)

        _, state.logs_autoscroll = imgui.checkbox("Autoscroll", state.logs_autoscroll)

        imgui.same_line()
        if imgui.button("Clear"):
            state.log_handler.clear()
            state.logs_count = 0

        if imgui.begin_child("##logs"):
            at_bottom_before = imgui.get_scroll_y() >= imgui.get_scroll_max_y() - 1

            logs_count = 0
            records = state.log_handler.snapshot()
            for record in records:
                logs_count += 1
                imgui.text_wrapped(record.message)

            if state.logs_autoscroll and (
                logs_count > state.logs_count or at_bottom_before
            ):
                imgui.set_scroll_here_y(1)

            state.logs_count = logs_count

        imgui.end_child()

    imgui.end()


def run(log_level: Level) -> None:
    """Run GUI app."""
    log_handler = cast(GuiHandler, app_logger.setup_gui(log_level))
    state = State(log_handler)

    try:
        # Import here to keep imports light for non-GUI contexts (tests, docs, etc.).
        from imgui_bundle import immapp, imgui, hello_imgui  # type: ignore

        hello_imgui.set_assets_folder(str(files("im_python").joinpath("assets")))

    except ImportError as e:  # pragma: no cover - diagnostic path
        _logger.error("imgui-bundle not installed")
        raise RuntimeError(
            "imgui-bundle is required to run the GUI app."
            "Install with `pip install imgui-bundle`"
        ) from e

    ini_path = _get_config_path() / "imgui.ini"
    _load_state(ini_path, state)

    _logger.info("GUI started")

    def gui() -> None:
        io = imgui.get_io()
        _handle_log_panel_toggle_key(io, state)

        imgui.text("Hello I'm Python!")
        imgui.separator()
        imgui.text("- Edit this GUI in src/im_python/gui.py")
        imgui.text("- Add panels, menus, docking, etc.")

        if imgui.button(f"Show Logs ({LOG_PANEL_TOGGLE_KEY})"):
            state.logs_panel_visible = not state.logs_panel_visible
        imgui.same_line()

        if imgui.button("Generate test logs"):
            _logger.debug("Debug log")
            _logger.info("Info log")
            _logger.warning("Warning log")
            _logger.error("Error log")
            _logger.critical("Critical log")

        if imgui.button("Close"):
            hello_imgui.get_runner_params().app_shall_exit = True

        _render_log_panel(imgui, hello_imgui, state)

    runner_parameters = hello_imgui.RunnerParams()
    runner_parameters.callbacks.show_gui = gui
    runner_parameters.app_window_params.window_title = WINDOW_TITLE
    runner_parameters.ini_folder_type = hello_imgui.IniFolderType.absolute_path
    runner_parameters.ini_filename = str(ini_path)
    runner_parameters.ini_filename_use_app_window_title = False

    immapp.run(runner_parameters)

    _save_state(ini_path, state)
