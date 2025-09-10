from __future__ import annotations

import sys
from importlib.metadata import PackageNotFoundError, version as pkg_version
import typer

app = typer.Typer(
    name="im-python",
    help="Hello I'm Python",
)


def _print_version() -> None:
    try:
        version = pkg_version("im-python")
    except PackageNotFoundError:
        version = "0.0.0+local"
    typer.echo(version)


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
) -> None:
    if version:
        _print_version()
        raise typer.Exit(0)

    if context.invoked_subcommand is None:
        gui()
        raise typer.Exit(0)


@app.command(help="Launch the GUI demo")
def gui() -> int:
    from .gui import run

    run()
    raise typer.Exit(0)


@app.command(help="Quick self-check and exit")
def check() -> None:
    typer.echo("im-python OK")


def main() -> int:
    app(prog_name="im-python")
    return 0


if __name__ == "__main__":
    sys.exit(main())
