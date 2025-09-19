from enum import IntEnum
import logging
from typing import Final, Self

_ALIASES: Final[dict[str, str]] = {"WARN": "WARNING", "FATAL": "CRITICAL"}


class Level(IntEnum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    @classmethod
    def parse(cls, value: str | int | Self) -> Self:
        """
        Accepts enum, int (10/20/...), or string ('debug', '20').
        Raises ValueError on unknown.
        """

        if isinstance(value, cls):
            return value

        if isinstance(value, int):
            try:
                return cls(value)
            except ValueError:
                raise ValueError(f"Unknown numeric log level: {value}") from None
        if isinstance(value, str):
            level_string = value.strip()
            if level_string.isdigit():
                return cls(int(level_string))

            name = level_string.upper()
            name = _ALIASES.get(name, name)

            try:
                return cls[name]
            except KeyError:
                valid = ", ".join([e.name for e in cls])
                raise ValueError(f"Invalid log level: {value!r}. Valid: {valid}")
