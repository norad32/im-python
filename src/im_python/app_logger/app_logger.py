from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
import sys
import queue
import atexit
import threading
from .levels import Level


def _detect_app_name(default="app"):
    if getattr(sys, "frozen", False):
        return Path(sys.executable).stem

    if sys.argv and sys.argv[0]:
        name = Path(sys.argv[0]).stem
        if name and name not in ("-c", "<stdin>"):
            return name

    return (
        Path(globals().get("__file__", default)).stem
        if "__file__" in globals()
        else default
    )


APP_NAME = _detect_app_name()
_logger = logging.getLogger(APP_NAME)

_queue: queue.Queue[logging.LogRecord] | None = None
_listener: QueueListener | None = None
_sinks: list[logging.Handler] = []

_lock = threading.RLock()


def _get_log_path() -> Path:
    try:
        from platformdirs import user_log_dir

        log_dir = Path(user_log_dir(APP_NAME))
    except ImportError:
        log_dir = Path("logs")
        _logger.error(f"No user log dir. Defaulting to {log_dir}")

    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / f"{APP_NAME}.log"


def _build_formatter() -> logging.Formatter:
    format_str = (
        "{asctime}.{msecs:03.0f} | {levelname:8s} | {name}:{lineno} | {message}"
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=format_str, datefmt=date_format, style="{")
    return formatter


def _remove_handlers() -> None:
    for handler in list(_logger.handlers):
        _logger.removeHandler(handler)

        try:
            handler.close()
        except Exception as e:
            print(f"[app_logger] handler.close() failed: {e!r}", file=sys.stderr)


def _rebuild_listener(new_handlers: list[logging.Handler]) -> None:
    global _sinks, _listener

    _sinks = new_handlers
    _create_queue()
    assert _queue is not None
    _listener = QueueListener(_queue, *_sinks, respect_handler_level=True)
    _listener.start()


def _stop_listener() -> None:
    global _listener

    if _listener is not None:
        try:
            _listener.stop()
        finally:
            _listener = None


def _create_queue() -> None:
    global _queue

    if _queue is None:
        _queue = queue.Queue(0)  # unbounded


def setup(level=Level.ERROR) -> None:
    """
    Configure the app logger with console + rotating file sinks and a background listener.
    Safe to call multiple times.
    """
    with _lock:
        _logger.setLevel(level)
        _logger.propagate = False

        _stop_listener()
        _remove_handlers()

        formatter = _build_formatter()

        _create_queue()
        assert _queue is not None
        queue_handler = QueueHandler(_queue)
        queue_handler.setLevel(level)
        _logger.addHandler(queue_handler)

        sinks: list[logging.Handler] = []

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        sinks.append(console_handler)

        file_handler = RotatingFileHandler(
            _get_log_path(),
            maxBytes=1_000_000,
            backupCount=3,
            encoding="utf-8",
            delay=True,
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        sinks.append(file_handler)

        for handler in _sinks:
            try:
                handler.setLevel(level)
                handler.setFormatter(formatter)
            except Exception as e:
                print(f"[app_logger] preserving sink failed: {e!r}", file=sys.stderr)
            sinks.append(handler)

        _rebuild_listener(sinks)

        atexit.unregister(shutdown)  # avoid duplicate registrations
        atexit.register(shutdown)


def setup_gui(level=Level.ERROR) -> logging.Handler:
    """Add the ImGui sink and rebuild the listener."""
    if _listener is None:
        raise RuntimeError("Cannot set-up gui logger before logger is set-up")

    with _lock:
        try:
            from .gui_handler import GuiHandler
        except ImportError as e:
            raise RuntimeError("ImGui logging is not available") from e

        gui_handler = next(
            (handler for handler in _sinks if isinstance(handler, GuiHandler)), None
        )

        if gui_handler is None:
            gui_handler = GuiHandler()

        gui_handler.setLevel(level)
        gui_handler.setFormatter(_build_formatter())

        sinks = [handler for handler in _sinks if not isinstance(handler, GuiHandler)]
        sinks.append(gui_handler)
        _stop_listener()
        _rebuild_listener(sinks)

        return gui_handler


def shutdown() -> None:
    """Stop background logging and close log file."""
    with _lock:
        _stop_listener()
        _remove_handlers()


def set_level(level: Level) -> None:
    """Change log level at runtime."""
    with _lock:
        _logger.setLevel(level)

        for handler in _logger.handlers:
            handler.setLevel(level)

        for handler in _sinks:
            handler.setLevel(level)


def get(name: str | None = None) -> logging.Logger:
    """Get app logger or a child logger"""
    if not name:
        return _logger

    return logging.getLogger(f"{APP_NAME}.{name}")
