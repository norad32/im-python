from __future__ import annotations

from contextlib import contextmanager
from importlib.resources import files, as_file
from os import PathLike
from pathlib import Path, PurePath
from typing import Iterator, TextIO

_ASSETS = files("im_python").joinpath("assets")


def _parts(pathlike: str | PathLike[str]) -> tuple[str, ...]:
    """
    Normalize a path or string into string segments for Traversable.joinpath().
    """
    return tuple(PurePath(pathlike).parts)


def _traversable(pathlike: str | PathLike[str]):
    t = _ASSETS
    for seg in _parts(pathlike):
        t = t.joinpath(seg)
    return t


def resource(pathlike: str | PathLike[str]) -> Path:
    """
    Return a real filesystem Path to a packaged resource.
    """
    t = _traversable(pathlike)
    with as_file(t) as p:
        return Path(p)


@contextmanager
def open_text(
    pathlike: str | PathLike[str], encoding: str = "utf-8"
) -> Iterator[TextIO]:
    """Open a text resource with the given encoding."""
    t = _traversable(pathlike)
    with as_file(t) as p:
        with open(p, "r", encoding=encoding) as f:
            yield f


def exists(pathlike: str | PathLike[str]) -> bool:
    """True if the resource exists inside the package."""
    return _traversable(pathlike).is_file()
