
import unittest
import sys
sys.path.insert(0, '../src')
from src.validator import Validator
from io import StringIO
from contextlib import redirect_stdout
from os import path as path_check


class TestValidator(unittest.TestCase):

    def test_validate_community_threshold_happy(self):
        values = [0, 1, 2]
        for value in values:
            result = Validator.validate_community_threshold(value)
            assert result == ""

    def test_validate_community_threshold_sad(self):
        values = [-1, 1.3, 3]
        for value in values:
            f = StringIO()
            with redirect_stdout(f):
                with self.assertRaises(SystemExit):
                    Validator.validate_community_threshold(value)
            f.close

    def test_validate_maintenance_threshold_happy(self):
        values = [0, 1, 2]
        for value in values:
            result = Validator.validate_maintenance_threshold(value)
            assert result == ""

    def test_validate_maintenance_threshold_sad(self):
        values = [-1, 1.3, 3]
        for value in values:
            f = StringIO()
            with redirect_stdout(f):
                with self.assertRaises(SystemExit):
                    Validator.validate_maintenance_threshold(value)
            f.close

    def test_validate_popularity_threshold_happy(self):
        values = [0, 1, 5]
        for value in values:
            result = Validator.validate_popularity_threshold(value)
            assert result == ""

    def test_validate_popularity_threshold_sad(self):
        values = [-1, 3.3, 6]
        for value in values:
            f = StringIO()
            with redirect_stdout(f):
                with self.assertRaises(SystemExit):
                    Validator.validate_popularity_threshold(value)
            f.close

    def test_validate_security_threshold_happy(self):
        values = [0, 1, 2]
        for value in values:
            result = Validator.validate_security_threshold(value)
            assert result == ""

    def test_validate_security_threshold_sad(self):
        values = [-1, 3, 1.1]
        for value in values:
            f = StringIO()
            with redirect_stdout(f):
                with self.assertRaises(SystemExit):
                    Validator.validate_security_threshold(value)
            f.close

    def test_validate_score_threshold_happy(self):
        values = [0, 50, 100]
        for value in values:
            result = Validator.validate_score_threshold(value)
            assert result == ""

    def test_validate_score_threshold_sad(self):
        values = [-1, 101, 50.2]
        for value in values:
            f = StringIO()
            with redirect_stdout(f):
                with self.assertRaises(SystemExit):
                    Validator.validate_score_threshold(value)
            f.close

    def test_validate_output_format_sad(self):
        input = 'lol'
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Validator.validate_output_format(input)
        f.close

    def test_validate_output_format_happy(self):
        input = "JSON"
        result = Validator.validate_output_format(input)
        assert result == ""
    
    def test_validate_inputs_list_sad(self):
        inputs = 'somestring'
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Validator.validate_input_list(inputs)
        f.close

    def test_validate_inputs_list_happy(self):
        inputs = ['some', 'list']
        result = Validator.validate_input_list(inputs)
        assert result == ""

    def test_validate_path_happy(self):
        path = path_check.dirname(__file__) + "/files/requirements.txt"
        result = Validator.validate_path(path)
        assert result == ""

    def test_validate_path_sad_basename(self):
        path = path_check.dirname(__file__) + "/files/lol.txt"
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Validator.validate_path(path)
        f.close

    def test_validate_path_sad_nonexist(self):
        path = "/path/does/not/exist/files/requirements.txt"
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Validator.validate_path(path)
        f.close

if __name__ == "__main__":
    unittest.main()