from __future__ import annotations
from importlib.resources import files


def run() -> None:
    """Run a GUI app."""
    try:
        # Import here to keep imports light for non-GUI contexts (tests, docs, etc.).
        from imgui_bundle import immapp, imgui, hello_imgui  # type: ignore

        hello_imgui.set_assets_folder(str(files("im_python").joinpath("assets")))

    except Exception as exc:  # pragma: no cover - diagnostic path
        raise RuntimeError(
            "imgui-bundle is required to run the GUI app."
            "Install with `pip install imgui-bundle` inside your virtual environment."
        ) from exc

    def gui() -> None:
        imgui.text("Hello I'm Python!")
        imgui.separator()
        imgui.text("• Edit this GUI in src/im_python/gui.py")
        imgui.text("• Add panels, menus, docking, etc.")
        if imgui.button("Close"):
            hello_imgui.get_runner_params().app_shall_exit = True

    immapp.run(
        gui_function=gui,
        window_title="I'm Python",
        window_size=(900, 600),
    )
