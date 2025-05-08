from __future__ import annotations

import logging
from collections import deque
from pathlib import Path
from threading import Lock
from typing import ClassVar
from typing import Deque

from docudex.utils.package_info import PackageInfo
from docudex.utils.paths import Paths
from rich.logging import RichHandler


class Logger:
    """Thread-safe singleton logger with line-based truncation and optional console output."""

    DEFAULT_LOG_FILE: ClassVar[str] = "docudex.log"
    _instance: ClassVar[Logger | None] = None
    _lock: ClassVar[Lock] = Lock()

    def __new__(cls, *args: object, **kwargs: object) -> Logger:
        """Create a singleton instance of the Logger class."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, verbose: bool = True, max_lines: int = 5, log_file: Path | str | None = None
    ) -> None:
        """
        Initialize the Logger instance.

        Args:
            verbose (bool): Whether to log messages to the console.
            max_lines (int): Maximum number of lines allowed in the log file.
            log_file (Path | str | None): Path to the log file. Defaults to 'docudex.log'.
        """
        if getattr(self, "_initialized", False):
            return

        package_info = PackageInfo()
        paths = Paths(package_info)

        self.verbose: bool = verbose
        self.max_lines: int = max_lines
        self.log_file: Path = (
            Path(log_file) if log_file else paths.get_log_dir() / self.DEFAULT_LOG_FILE
        )
        self.logger: logging.Logger = logging.getLogger("DocudexLogger")
        self._initialized: bool = True
        self._setup_logger()

    def _setup_logger(self) -> None:
        """Set up file and console handlers for the logger."""
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)-8s - %(message)s", "%d-%m-%Y %H:%M:%S"
        )

        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        if self.verbose:
            console_handler = RichHandler(
                markup=True,
                rich_tracebacks=True,
                show_time=False,
                show_path=False,
                show_level=False,
            )
            console_formatter = logging.Formatter(
                "%(asctime)s - %(levelname)-8s - %(message)s", "%d-%m-%Y %H:%M:%S"
            )
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)

    def _truncate_log_file(self) -> None:
        """Ensure the log file contains no more than `max_lines` by removing oldest lines."""
        lines: Deque[str]
        with self.log_file.open("r", encoding="utf-8") as f:
            lines = deque(f, maxlen=self.max_lines)

        with self.log_file.open("w", encoding="utf-8") as f:
            f.writelines(lines)

    def _log(self, level: str, message: str) -> None:
        """Log a message at the specified level and truncate the log file if needed."""
        getattr(self.logger, level)(message)
        self._truncate_log_file()

    def info(self, message: str) -> None:
        """Log a message with level INFO."""
        self._log("info", message)

    def debug(self, message: str) -> None:
        """Log a message with level DEBUG."""
        self._log("debug", message)

    def warning(self, message: str) -> None:
        """Log a message with level WARNING."""
        self._log("warning", message)

    def error(self, message: str) -> None:
        """Log a message with level ERROR."""
        self._log("error", message)

    def critical(self, message: str) -> None:
        """Log a message with level CRITICAL."""
        self._log("critical", message)
