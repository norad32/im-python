from __future__ import annotations


def run() -> None:
    """Run a minimal imgui-bundle demo using the immapp helper.

    Importing `imgui_bundle` happens inside this function so that unit tests can
    import this module without requiring GUI dependencies.
    """
    try:
        # Import here to keep imports light for non-GUI contexts (tests, docs, etc.).
        from imgui_bundle import immapp, imgui, hello_imgui  # type: ignore
    except Exception as exc:  # pragma: no cover - diagnostic path
        raise RuntimeError(
            "imgui-bundle is required to run the GUI demo. "
            "Install with `pip install imgui-bundle` inside your virtual environment."
        ) from exc

    # Configure a simple Hello ImGui application
    def gui() -> None:
        imgui.text("Hello from imgui-bundle template!")
        imgui.separator()
        imgui.text("• Edit this GUI in src/tom_imgui_template/app.py")
        imgui.text("• Add panels, menus, docking, etc.")
        if imgui.button("Close"):
            hello_imgui.get_runner_params().app_shall_exit = True

    immapp.run(
        gui_function=gui,
        window_title="ImGui-Bundle Template",
        window_size=(900, 600),
    )
