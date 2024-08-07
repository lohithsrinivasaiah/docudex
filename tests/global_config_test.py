import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock
from unittest.mock import patch

from ruamel.yaml import YAML

from docudex.config import ConfigLoader
from docudex.config import ConfigManager
from docudex.config import GlobalConfig


class TestConfigLoader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "config.yaml"
        self.yaml = YAML()
        self.yaml.preserve_quotes = True

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load(self):
        with open(self.config_path, "w") as f:
            f.write("key: value\n")
        config_loader = ConfigLoader(self.config_path)
        config = config_loader.load()
        self.assertEqual(config, {"key": "value"})

    def test_load_empty(self):
        config_loader = ConfigLoader(self.config_path)
        with self.assertRaises(FileNotFoundError):
            config_loader.load()

    def test_load_error(self):
        with patch("ruamel.yaml.YAML.load", side_effect=Exception("Mock error")):
            with open(self.config_path, "w") as f:
                f.write("key: value\n")
            config_loader = ConfigLoader(self.config_path)
            with self.assertRaises(Exception):
                config_loader.load()

    def test_save(self):
        config_loader = ConfigLoader(self.config_path)
        config_loader.save({"key": "value"})
        with open(self.config_path) as f:
            self.assertEqual(f.read(), "key: value\n")

    def test_save_error(self):
        with patch("ruamel.yaml.YAML.dump", side_effect=OSError("Mock error")):
            config_loader = ConfigLoader(self.config_path)
            with self.assertRaises(OSError):
                config_loader.save({"key": "value"})


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.config_path = Path(self.temp_dir.name) / "config.yaml"
        self.default_config_path = Path(self.temp_dir.name) / "default_config.yaml"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_or_create_config(self):
        with open(self.config_path, "w") as f:
            f.write("key: value\n")
        config_manager = ConfigManager(self.config_path, self.default_config_path)
        config = config_manager.load_or_create_config()
        self.assertEqual(config, {"key": "value"})

    def test_load_or_create_config_default(self):
        with open(self.default_config_path, "w") as f:
            f.write("key: value\n")
        config_manager = ConfigManager(self.config_path, self.default_config_path)
        config = config_manager.load_or_create_config()
        self.assertEqual(config, {"key": "value"})

    def test_create_config_from_default(self):
        with open(self.default_config_path, "w") as f:
            f.write("key: value\n")
        config_manager = ConfigManager(self.config_path, self.default_config_path)
        config = config_manager.create_config_from_default()
        self.assertEqual(config, {"key": "value"})

    def test_create_config_from_default_error(self):
        config_manager = ConfigManager(self.config_path, self.default_config_path)
        with self.assertRaises(FileNotFoundError):
            config_manager.create_config_from_default()


class TestGlobalConfig(unittest.TestCase):
    def setUp(self):
        self.config_manager_mock = MagicMock(spec=ConfigManager)
        self.config_manager_mock.load_or_create_config.return_value = {"key": "value"}

    def tearDown(self):
        GlobalConfig._instance = None  # Reset singleton instance for each test

    def test_init(self):
        with patch("docudex.config.ConfigManager", return_value=self.config_manager_mock):
            global_config = GlobalConfig()
            self.assertIn("_initialized", global_config.__dict__)
            self.assertIn("config_manager", global_config.__dict__)
            self.assertEqual(global_config.__dict__["key"], "value")


if __name__ == "__main__":
    unittest.main()
