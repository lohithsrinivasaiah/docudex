import logging
from pathlib import Path
from unittest.mock import patch

import pytest
from docudex.logger import Logger


@pytest.fixture(autouse=True)
def reset_logger_singleton():
    Logger._instance = None


@pytest.fixture
def temp_log_path(tmp_path: Path) -> Path:
    return tmp_path / "test.log"


def test_init_early_return(temp_log_path: Path):
    logger = Logger(verbose=False, log_file=temp_log_path)
    logger._initialized = True
    logger.__init__(
        verbose=False, log_file=temp_log_path
    )  # should early-return without reinitializing
    assert logger._initialized is True


def test_log_file_fallback_path():
    with patch("docudex.logger.Paths.get_log_dir", return_value=Path("/tmp")):
        logger = Logger(verbose=False, log_file=None)
        assert logger.log_file.name == Logger.DEFAULT_LOG_FILE


def test_logger_sets_up_logger(temp_log_path: Path):
    logger = Logger(verbose=False, log_file=temp_log_path)
    assert isinstance(logger.logger, logging.Logger)


def test_log_file_parent_created(tmp_path: Path):
    custom_path = tmp_path / "logs" / "my.log"
    Logger(verbose=False, log_file=custom_path)
    assert custom_path.parent.exists()


def test_debug_logging(temp_log_path: Path, caplog):
    caplog.set_level(logging.DEBUG)
    logger = Logger(verbose=True, log_file=temp_log_path)
    logger.debug("Debug message")
    assert any("Debug message" in r.message for r in caplog.records)


def test_info_logging(temp_log_path: Path, caplog):
    caplog.set_level(logging.INFO)
    logger = Logger(verbose=True, log_file=temp_log_path)
    logger.info("Info message")
    assert any("Info message" in r.message for r in caplog.records)


def test_warning_logging(temp_log_path: Path, caplog):
    caplog.set_level(logging.WARNING)
    logger = Logger(verbose=True, log_file=temp_log_path)
    logger.warning("Warning message")
    assert any("Warning message" in r.message for r in caplog.records)


def test_error_logging(temp_log_path: Path, caplog):
    caplog.set_level(logging.ERROR)
    logger = Logger(verbose=True, log_file=temp_log_path)
    logger.error("Error message")
    assert any("Error message" in r.message for r in caplog.records)


def test_critical_logging(temp_log_path: Path, caplog):
    caplog.set_level(logging.CRITICAL)
    logger = Logger(verbose=True, log_file=temp_log_path)
    logger.critical("Critical error")
    assert any("Critical error" in r.message for r in caplog.records)


def test_truncate_log_file_limits_lines(temp_log_path: Path):
    lines = [f"line {i}\n" for i in range(10)]
    with temp_log_path.open("w") as f:
        f.writelines(lines)

    logger = Logger(verbose=False, max_lines=5, log_file=temp_log_path)
    logger._truncate_log_file()

    with temp_log_path.open("r") as f:
        new_lines = f.readlines()

    assert new_lines == lines[-5:]
