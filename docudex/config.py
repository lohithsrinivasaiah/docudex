import logging
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

CONFIG_PATH = Path("~/.config/docudex/config.yaml").expanduser()
DEFAULT_CONFIG_PATH = Path("config.yaml")


class ConfigLoader:
    """
    Handles loading and saving of YAML configuration files.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self.yaml = YAML()
        self.yaml.preserve_quotes = True

    def load(self) -> Any:
        """
        Loads the configuration from the YAML file.
        """
        try:
            with self.path.open() as file:
                return self.yaml.load(file) or {}
        except (Exception, FileNotFoundError) as e:
            logging.error(f"Error loading YAML file at {self.path}: {e}")
            raise

    def save(self, config: Any) -> None:
        """
        Saves the given configuration to the YAML file.
        """
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self.path.open("w") as file:
                self.yaml.dump(config, file)
        except OSError as e:
            logging.error(f"Error saving configuration file at {self.path}: {e}")
            raise


class ConfigManager:
    """
    Manages loading and creating configurations.
    """

    def __init__(
        self,
        config_path: Path = CONFIG_PATH,
        default_config_path: Path = DEFAULT_CONFIG_PATH,
    ) -> None:
        self.config_path = config_path
        self.default_config_path = default_config_path
        self.config_loader = ConfigLoader(config_path)

    def load_or_create_config(self) -> Any:
        """
        Loads the configuration if it exists.
        Otherwise, creates it from the default configuration.
        """
        if self.config_path.exists():
            return self.config_loader.load()
        return self.create_config_from_default()

    def create_config_from_default(self) -> Any:
        """
        Creates a configuration from the default file and saves it as the main configuration.
        """
        if not self.default_config_path.exists():
            raise FileNotFoundError(
                f"Default config file '{self.default_config_path}' does not exist.",
            )

        default_config_loader = ConfigLoader(self.default_config_path)
        config = default_config_loader.load()
        self.config_loader.save(config)
        return config


class GlobalConfig:
    """
    Singleton class for managing global configuration.
    """

    _instance: "GlobalConfig | None" = None

    def __new__(cls: type["GlobalConfig"], *args: Any, **kwargs: Any) -> "GlobalConfig":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        config_path: Path = CONFIG_PATH,
        default_config_path: Path = DEFAULT_CONFIG_PATH,
    ) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.config_manager = ConfigManager(config_path, default_config_path)
            self.__dict__.update(self.config_manager.load_or_create_config())


if __name__ == "__main__":
    GlobalConfig()
