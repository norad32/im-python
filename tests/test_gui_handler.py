import logging

from im_python.app_logger.gui_handler import GuiHandler


def test_emit_Should_StoreFormattedRecord():
    handler = GuiHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s:%(message)s"))

    handler.emit(
        logging.LogRecord(
            "test", logging.WARNING, "test.py", 10, "hello %s", ("GUI",), None, None
        )
    )

    record = handler.snapshot()[0]
    assert record.levelno == logging.WARNING
    assert record.levelname == "WARNING"
    assert record.name == "test"
    assert record.message == "WARNING:hello GUI"


def test_snapshot_Should_KeepNewestRecords_If_CapacityIsExceeded():
    handler = GuiHandler(capacity=2)
    logger = logging.getLogger("test_gui_handler")
    logger.handlers = [handler]
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    for message in ("first", "second", "third"):
        logger.info(message)

    assert [record.message for record in handler.snapshot()] == ["second", "third"]


def test_clear_Should_RemoveAllRecords():
    handler = GuiHandler()
    handler.emit(
        logging.LogRecord("test", logging.INFO, "test.py", 1, "entry", (), None, None)
    )

    handler.clear()

    assert handler.snapshot() == []
