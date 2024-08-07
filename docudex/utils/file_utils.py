from __future__ import annotations

import mimetypes
import os


def check_file_exists(file_path: str) -> bool:
    """Check if a file exists at the given path."""
    return os.path.isfile(file_path)


def get_file_type(file_path: str) -> str | None:
    """Guess the MIME type of a file based on its file path."""
    if not check_file_exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_type, _ = mimetypes.guess_type(file_path)
    return file_type
