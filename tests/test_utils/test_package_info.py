from pathlib import Path

from docudex.utils.package_info import PackageInfo

MOCK_TOML = b"""
[tool.poetry]
name = "mocked-package"
"""


def test_get_package_name_success(tmp_path):
    # Create a mock pyproject.toml
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_bytes(MOCK_TOML)

    pkg_info = PackageInfo(pyproject_path=pyproject_path, default_name="fallback")
    assert pkg_info.get_package_name() == "mocked-package"


def test_get_package_name_file_not_found():
    pkg_info = PackageInfo(pyproject_path=Path("/nonexistent/path.toml"), default_name="fallback")
    assert pkg_info.get_package_name() == "fallback"


def test_get_package_name_invalid_toml(tmp_path):
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text("invalid toml =")  # Bad syntax

    pkg_info = PackageInfo(pyproject_path=pyproject_path, default_name="fallback")
    assert pkg_info.get_package_name() == "fallback"
