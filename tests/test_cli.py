from typer.testing import CliRunner

from im_python import cli
from im_python.app_logger.levels import Level

runner = CliRunner()


def test_check_Should_PrintSuccessMessage(monkeypatch):
    monkeypatch.setattr(cli.app_logger, "setup", lambda _: None)

    result = runner.invoke(cli.app, ["check"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "I'm Python OK"


def test_check_Should_UseRequestedLogLevel_If_OptionIsProvided(monkeypatch):
    configured_levels = []
    monkeypatch.setattr(cli.app_logger, "setup", configured_levels.append)

    result = runner.invoke(cli.app, ["check", "--log-level", "DEBUG"])

    assert result.exit_code == 0
    assert configured_levels == [Level.DEBUG]


def test_check_Should_ReturnUsageError_If_LogLevelIsInvalid():
    result = runner.invoke(cli.app, ["check", "--log-level", "unknown"])

    assert result.exit_code != 0
    assert "Invalid log level" in result.output


def test_version_Should_PrintInstalledVersion_If_Requested(monkeypatch):
    configured_levels = []
    monkeypatch.setattr(cli.app_logger, "setup", configured_levels.append)
    monkeypatch.setattr(cli, "pkg_version", lambda _: "1.2.3")

    result = runner.invoke(cli.app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "1.2.3"
    assert configured_levels == [Level.ERROR]
