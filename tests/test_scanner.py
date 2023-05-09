
import unittest
import sys
sys.path.insert(0, '../src')
from src.scanner import Scanner
from io import StringIO
from contextlib import redirect_stdout
from os import path as path_check


class TestScanner(unittest.TestCase):
    
    def test_scan(self):
        registry = "npm-package"
        path = path_check.dirname(__file__) + "/files/package.json"
        scan_results = Scanner.scan(registry, path)
        assert type(scan_results) == list
        assert len(scan_results) == 3

    def test_validate_registry_happy(self):
        expected = ""
        registry = "npm-package"
        result = Scanner.validate_registry(registry)
        assert result == expected

    def test_validate_registry_sad(self):
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Scanner.validate_registry("lol")
        f.close

if __name__ == "__main__":
    unittest.main()