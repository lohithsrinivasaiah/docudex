import os
import unittest

from docudex.utils.file_utils import check_file_exists
from docudex.utils.file_utils import get_file_type


class TestFileUtils(unittest.TestCase):
    base_path = os.path.join(os.path.dirname(__file__), "test_assets")
    supported_file_types = [
        "document_test.pdf",         # PDF document
        "spreadsheet_test.xlsx",     # Excel file
        "data_test.csv",             # CSV file
        "table_test.tsv",            # TSV file
        "script_test.py",            # Python script
        "textfile_test.txt",         # Text file
        "style_test.css",            # CSS file
        "index_test.html",           # HTML file
        "script_test.js",            # JavaScript file
        "data_test.json",            # JSON file
        "main_test.cpp",             # C++ source file
        "program_test.java",         # Java source file
        "module_test.rb",            # Ruby script
        "test_test.sh",              # Shell script
    ]

    def test_check_file_exists(self):
        for file_name in self.supported_file_types:
            file_path = os.path.join(self.base_path, file_name)
            self.assertTrue(check_file_exists(file_path))

        non_existent_file_path = os.path.join(self.base_path, "non_existent_file.txt")
        self.assertFalse(check_file_exists(non_existent_file_path))

    def test_get_file_type(self):
        for file_name in self.supported_file_types:
            file_path = os.path.join(self.base_path, file_name)
            file_type = get_file_type(file_path)
            self.assertIsNotNone(file_type)

        non_existent_file_path = os.path.join(self.base_path, "non_existent_file.txt")
        with self.assertRaises(FileNotFoundError):
            get_file_type(non_existent_file_path)


if __name__ == "__main__":
    unittest.main()
