from pathlib import Path
from types import SimpleNamespace

from im_python.app_logger.gui_handler import GuiHandler
from im_python.gui import State, _handle_log_panel_toggle_key, _load_state, _save_state


def test_save_state_Should_RoundTripPanelPreferences(tmp_path):
    source = State(GuiHandler(), logs_panel_visible=True, logs_autoscroll=False)
    destination = State(GuiHandler())
    ini_path = Path(tmp_path) / "state.ini"

    _save_state(ini_path, source)
    _load_state(ini_path, destination)

    assert destination.logs_panel_visible is True
    assert destination.logs_autoscroll is False


def test_load_state_Should_KeepDefaults_If_FileDoesNotExist(tmp_path):
    state = State(GuiHandler())

    _load_state(tmp_path / "missing.ini", state)

    assert state.logs_panel_visible is False
    assert state.logs_autoscroll is True


def test_handle_log_panel_toggle_key_Should_ToggleVisibility_If_ShortcutPressed():
    input_state = SimpleNamespace(
        want_text_input=False, input_queue_characters=[ord("§")]
    )
    state = State(GuiHandler())

    _handle_log_panel_toggle_key(input_state, state)

    assert state.logs_panel_visible is True


def test_handle_log_panel_toggle_key_Should_NotToggleVisibility_If_TextInputIsActive():
    input_state = SimpleNamespace(
        want_text_input=True, input_queue_characters=[ord("§")]
    )
    state = State(GuiHandler())

    _handle_log_panel_toggle_key(input_state, state)

    assert state.logs_panel_visible is False
