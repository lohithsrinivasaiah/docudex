from __future__ import annotations

from pathlib import Path

import tomli as tomllib

DEFAULT_PACKAGE_NAME = "docudex"
DEFAULT_PYPROJECT_PATH = Path(__file__).parents[3] / "pyproject.toml"


class PackageInfo:
    """
    Handles reading and caching the package name from pyproject.toml.
    """

    def __init__(
        self,
        pyproject_path: Path = DEFAULT_PYPROJECT_PATH,
        default_name: str = DEFAULT_PACKAGE_NAME,
    ):
        """
        Initialize the PackageInfo object.

        Args:
            pyproject_path (Path): Path to the pyproject.toml file.
            default_name (str): Fallback package name if retrieval fails.
        """
        self.pyproject_path = pyproject_path
        self.default_name = default_name

    def get_package_name(self) -> str:
        """
        Retrieve the package name from pyproject.toml using Poetry's format.

        Returns:
            str: Package name or the default name if an error occurs.
        """
        try:
            with self.pyproject_path.open("rb") as f:
                data = tomllib.load(f)
            return data["tool"]["poetry"]["name"]
        except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError):
            return self.default_name
