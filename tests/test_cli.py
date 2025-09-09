from __future__ import annotations

import sys
import types

import pytest
from typer.testing import CliRunner

from im_python import cli


@pytest.fixture()
def runner() -> CliRunner:
    return CliRunner()


def _install_dummy_gui(monkeyPatch: pytest.MonkeyPatch, *, code: int) -> None:
    package = cli.__package__ or "im_python"
    module_name = f"{package}.gui"

    dummy = types.ModuleType(module_name)

    def run() -> int:
        return code

    dummy.run = run  # type: ignore[attr-defined]
    sys.modules[module_name] = dummy


def test_should_print_version_if_version_flag(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cli, "pkg_version", lambda _: "1.2.3", raising=True)

    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == "1.2.3\n"


def test_should_print_version_if_version_short_flag(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cli, "pkg_version", lambda _: "9.9.9", raising=True)

    result = runner.invoke(cli.app, ["-v"])
    assert result.exit_code == 0
    assert result.stdout == "9.9.9\n"


def test_should_print_local_version_if_package_not_installed(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    def raise_pnf(_: str) -> str:
        raise cli.PackageNotFoundError

    monkeypatch.setattr(cli, "pkg_version", raise_pnf, raising=True)

    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert result.stdout == "0.0.0+local\n"


def test_should_show_help_if_help_flag(runner: CliRunner) -> None:
    result = runner.invoke(cli.app, ["--help"])
    assert result.exit_code == 0
    out = result.stdout
    # App help
    assert "Hello I'm Python" in out
    # Options/help lines
    assert "Show version and exit." in out
    # Commands help lines
    assert "Launch the GUI" in out
    assert "Quick self-check and exit" in out


def test_sould_exit_with_gui_code_if_no_subcommand_provided(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    _install_dummy_gui(monkeypatch, code=42)
    result = runner.invoke(cli.app, [])
    assert result.exit_code == 42
    assert result.stdout == ""


def test_should_exit_with_gui_code__if_gui_subcommand_invoked(
    runner: CliRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    _install_dummy_gui(monkeypatch, code=7)
    result = runner.invoke(cli.app, ["gui"])
    assert result.exit_code == 7
    assert result.stdout == ""


def test_should_echo_ok_if_check_subcommand_invoked(runner: CliRunner) -> None:
    result = runner.invoke(cli.app, ["check"])
    assert result.exit_code == 0
    assert result.stdout == "im-python OK\n"


def main_should_invoke_typer_app_with_prog_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []

    class DummyApp:
        def __call__(self, *args, **kwargs):
            calls.append((args, kwargs))

    dummy = DummyApp()
    monkeypatch.setattr(cli, "app", dummy, raising=True)

    rc = cli.main()

    assert rc == 0
    assert calls, "Typer app was not invoked by main()."
    assert calls[-1][1].get("prog_name") == "im-python"
