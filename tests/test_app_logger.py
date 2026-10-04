from im_python.app_logger import app_logger
from im_python.app_logger.levels import Level


def test_setup_Should_ConfigureLoggerAndWriteToFile(tmp_path, monkeypatch):
    log_path = tmp_path / "application.log"
    monkeypatch.setattr(app_logger, "_get_log_path", lambda: log_path)

    try:
        app_logger.setup(Level.INFO)
        logger = app_logger.get()

        assert logger.level == Level.INFO
        assert logger.propagate is False
        logger.info("test log entry")
    finally:
        app_logger.shutdown()

    assert "test log entry" in log_path.read_text(encoding="utf-8")
