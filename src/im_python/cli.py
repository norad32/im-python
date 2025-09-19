import sys
from importlib.metadata import PackageNotFoundError, version as pkg_version
import typer
from . import app_logger
from im_python.app_logger.levels import Level

_logger = app_logger.get(__name__)

app = typer.Typer(
    name="im-python",
    help="Hello I'm Python",
)

LOG_LEVEL_OPT = typer.Option(
    None,
    "--log-level",
    "-l",
    help=(
        "Set log level (name or number): CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET "
        "or 50/40/30/20/10/0. Subcommand value overrides global."
    ),
    metavar="LEVEL",
)


def _print_version() -> None:
    try:
        version = pkg_version("im-python")
    except PackageNotFoundError:
        version = "0.0.0+local"
    _logger.info(f"Version: {version}")
    typer.echo(version)


def _resolve_log_level(ctx: typer.Context, level_text: str | None) -> Level:
    text = level_text or (ctx.obj or {}).get("log_level") or "ERROR"
    try:
        return Level.parse(text)
    except ValueError as e:
        raise typer.BadParameter(str(e))


@app.callback(invoke_without_command=True)
def _root(
    context: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        is_eager=True,
    ),
    log_level: str | None = LOG_LEVEL_OPT,
) -> None:
    context.obj = context.obj or {}
    if log_level is not None:
        context.obj["log_level"] = log_level

    if version and context.invoked_subcommand is None:
        app_logger.setup(_resolve_log_level(context, log_level))
        _print_version()
        raise typer.Exit(0)

    if context.invoked_subcommand is None:
        context.invoke(gui, context, log_level)  # subcommand will configure logging
        raise typer.Exit(0)


@app.command(help="Launch the GUI")
def gui(context: typer.Context, log_level: str | None = LOG_LEVEL_OPT) -> int:
    level = _resolve_log_level(context, log_level)
    app_logger.setup(level)

    from .gui import run

    run(level)
    raise typer.Exit(0)


@app.command(help="Quick self-check and exit")
def check(context: typer.Context, log_level: str | None = LOG_LEVEL_OPT) -> None:
    level = _resolve_log_level(context, log_level)
    app_logger.setup(level)

    _logger.info("I'm Python OK")
    typer.echo("I'm Python OK")


def main() -> int:
    app(prog_name="im-python")
    return 0


if __name__ == "__main__":
    sys.exit(main())
