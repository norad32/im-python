import sys
from pathlib import Path
from typing import Final
from dataclasses import dataclass
from importlib.resources import files
from .app_logger.levels import Level


def _detect_app_name(default="app"):
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
    is_log_panel_visible: bool = False


def _handle_log_panel_toggle_key(io, state: State) -> None:
    """Toggle the log panel on LOG_PANEL_TOGGLE_KEY when not typing in an input."""
    if io.want_text_input:
        return
    for codepoint in io.input_queue_characters:
        if codepoint == ord(LOG_PANEL_TOGGLE_KEY):
            state.is_log_panel_visible = not state.is_log_panel_visible
            break


def _render_log_panel(imgui, hello_imgui, state: State) -> None:
    """Render non-movable, height-resizable log panel, that sticks to the viewport bottom."""
    if not state.is_log_panel_visible:
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

        imgui.text("Logs go here.")
        imgui.text(f"Current height: {int(current_size.y)} px")
    imgui.end()


def run(log_level: Level) -> None:
    """Run GUI app."""
    try:
        # Import here to keep imports light for non-GUI contexts (tests, docs, etc.).
        from imgui_bundle import immapp, imgui, hello_imgui  # type: ignore

        hello_imgui.set_assets_folder(str(files("im_python").joinpath("assets")))

    except ImportError as e:  # pragma: no cover - diagnostic path
        raise RuntimeError(
            "imgui-bundle is required to run the GUI app."
            "Install with `pip install imgui-bundle`"
        ) from e

    state = State()

    def gui() -> None:

        io = imgui.get_io()
        _handle_log_panel_toggle_key(io, state)

        imgui.text("Hello I'm Python!")
        imgui.separator()
        imgui.text("- Edit this GUI in src/im_python/gui.py")
        imgui.text("- Add panels, menus, docking, etc.")

        if imgui.button(f"Show Logs ({LOG_PANEL_TOGGLE_KEY})"):
            state.is_log_panel_visible = not state.is_log_panel_visible
        imgui.same_line()

        if imgui.button("Close"):
            hello_imgui.get_runner_params().app_shall_exit = True

        _render_log_panel(imgui, hello_imgui, state)

    immapp.run(
        gui_function=gui,
        window_title="I'm Python",
        window_size=(900, 600),
    )
