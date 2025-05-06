from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

from docudex.utils.package_info import PackageInfo
from docudex.utils.paths import Paths


def test_get_config_dir_returns_user_config_dir():
    mock_pkg_info = MagicMock(spec=PackageInfo)
    mock_pkg_info.get_package_name.return_value = "my-package"

    with patch("docudex.utils.paths.user_config_dir") as mock_user_config_dir:
        mock_user_config_dir.return_value = "/mock/config"
        paths = Paths(mock_pkg_info)

        assert paths.get_config_dir() == Path("/mock/config")
        mock_user_config_dir.assert_called_once_with("my-package")


def test_get_log_dir_returns_user_log_dir():
    mock_pkg_info = MagicMock(spec=PackageInfo)
    mock_pkg_info.get_package_name.return_value = "my-package"

    with patch("docudex.utils.paths.user_log_dir") as mock_user_log_dir:
        mock_user_log_dir.return_value = "/mock/log"
        paths = Paths(mock_pkg_info)

        assert paths.get_log_dir() == Path("/mock/log")
        mock_user_log_dir.assert_called_once_with("my-package")
