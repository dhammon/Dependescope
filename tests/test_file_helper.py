
import unittest
import sys
sys.path.insert(0, '../src')
from src.file_helper import FileHelper
from io import StringIO
from contextlib import redirect_stdout
from os import path as path_check


class TestFileHelper(unittest.TestCase):

    def test_find_registry_type_sad(self):
        path = path_check.dirname(__file__) + "/test_file_helper.py"
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                FileHelper.find_registry_type(path)
        f.close

    def test_find_registry_type_happy_pypi(self):
        path = path_check.dirname(__file__) + "/files/requirements.txt"
        result = FileHelper.find_registry_type(path)
        assert result == "python"

    def test_find_repository_type_happy_npm(self):
        path = path_check.dirname(__file__) + "/files/package.json"
        result = FileHelper.find_registry_type(path)
        assert result == "npm-package"
    
    def test_get_npm_packages_happy(self):
        expected = ['autoprefixer', 'babel-core', 'webpack-merge', '@types/jest']
        path = path_check.dirname(__file__) + "/files/package.json"
        result = FileHelper.get_npm_packages(path)
        assert result == expected
    
    def test_get_pypi_packages_happy(self):
        expected = ['beautifulsoup4', 'fake_useragent', 'scikit-fuzzy']
        path = path_check.dirname(__file__) + "/files/requirements.txt"
        result = FileHelper.get_pypi_packages(path)
        assert result == expected
    

if __name__ == "__main__":
    unittest.main()