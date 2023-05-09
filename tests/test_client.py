
import unittest
from io import StringIO
from contextlib import redirect_stdout
from os import path as path_check
from src.client import run
from src.client import handle_args
from src.client import validate_inputs


class TestClient(unittest.TestCase):

    def test_run_happy_equals(self):
        path = path_check.dirname(__file__) + "/files/requirements.txt"
        inputs = ['--package-file-path='+str(path),'--no-banner', '--output-format=JSON']
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit) as raised:
                run(inputs)
            self.assertEqual(raised.exception.code, 1)
        assert "[{" in f.getvalue()
        f.close
        
    def test_validate_inputs_happy(self):
        path = path_check.dirname(__file__) + "/files/requirements.txt"
        inputs = ['--package-file-path='+path,'--no-banner', '--output-format=JSON']
        validate_inputs(inputs)

    def test_handle_args_happy_default(self):
        input = ['--package-file-path=/some/path/packages.json']
        result = handle_args(input)
        self.assertEqual('/some/path/packages.json', result.package_file_path)
        self.assertEqual('STDOUT', result.output_format)
        self.assertEqual(False, result.no_banner)
        
    def test_handle_args_happy_custom(self):
        input = ['--package-file-path=/some/path/packages.json','--no-banner', '--output-format=JSON']
        result = handle_args(input)
        self.assertEqual('/some/path/packages.json', result.package_file_path)
        self.assertEqual('JSON', result.output_format)
        self.assertEqual(True, result.no_banner)


if __name__ == "__main__":
    unittest.main()