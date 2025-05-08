from __future__ import annotations

from pathlib import Path

from platformdirs import user_config_dir
from platformdirs import user_log_dir

from .package_info import PackageInfo


class Paths:
    """
    Manages paths for configuration and logging based on package name.
    """

    def __init__(self, package_info: PackageInfo):
        """
        Initialize the Paths object.

        Args:
            package_info (PackageInfo): An instance containing package metadata.
        """
        self.package_info = package_info
        self.package_name = self.package_info.get_package_name()

    def get_config_dir(self) -> Path:
        """
        Get the platform-specific user configuration directory.

        Returns:
            Path: Configuration directory path.
        """
        return Path(user_config_dir(self.package_name))

    def get_log_dir(self) -> Path:
        """
        Get the platform-specific user log directory.

        Returns:
            Path: Log directory path.
        """
        return Path(user_log_dir(self.package_name))
