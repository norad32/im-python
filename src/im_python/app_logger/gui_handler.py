import logging
import threading
from collections import deque
from typing import Deque, NamedTuple


class GuiRecord(NamedTuple):
    levelno: int
    levelname: str
    created: float
    name: str
    message: str


class GuiHandler(logging.Handler):
    def __init__(self, capacity: int = 1024):
        super().__init__()
        self.capacity = capacity
        self._records: Deque[GuiRecord] = deque(maxlen=capacity)
        self._lock = threading.Lock()

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        item = GuiRecord(
            record.levelno, record.levelname, record.created, record.name, message
        )
        with self._lock:
            self._records.append(item)

    def clear(self) -> None:
        with self._lock:
            self._records.clear()

    def snapshot(self) -> list[GuiRecord]:
        with self._lock:
            return list(self._records)
