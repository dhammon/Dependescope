
import unittest
import sys
sys.path.insert(0, '../src')
from src.scraper import Scraper
from io import StringIO
from contextlib import redirect_stdout


class TestScraper(unittest.TestCase):
    
    def test_check_snyk_advisor_happy(self):
        result = Scraper.check_snyk_advisor("npm-package", "lol")
        assert result == ["npm-package", 'lol', '42', 'No known security issues', 'Limited', 'Inactive', 'Limited', 'https://snyk.io/advisor/npm-package/lol']
    
    def test_check_snyk_advisor_sad(self):
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Scraper.check_snyk_advisor("npm-package", "doesnotexistandshouldresultinexitcode")
        f.close

    def test_validate_snyk_results_happy(self):
        results = ["npm-package", 'lol', '42', 'No known security issues', 'Limited', 'Inactive', 'Limited', 'https://snyk.io/advisor/npm-package/lol']
        result = Scraper.validate_snyk_results(results)
        assert result == ""
    
    def test_validate_snyk_results_sad_registry(self):
        results = ["doesnotexist", 'lol', '42', 'No known security issues', 'Limited', 'Inactive', 'Limited', 'https://snyk.io/advisor/npm-package/lol']
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Scraper.validate_snyk_results(results)
        f.close

    def test_validate_snyk_results_sad_package(self):
        results = ["npm-package", 'lol!invalidchar', '42', 'No known security issues', 'Limited', 'Inactive', 'Limited', 'https://snyk.io/advisor/npm-package/lol']
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Scraper.validate_snyk_results(results)
        f.close

    def test_validate_snyk_results_sad_score(self):
        results = ["npm-package", 'lol', 'abc', 'No known security issues', 'Limited', 'Inactive', 'Limited', 'https://snyk.io/advisor/npm-package/lol']
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Scraper.validate_snyk_results(results)
        f.close

    def test_validate_snyk_results_sad_security(self):
        results = ["npm-package", 'lol', '44', 'doesnotexist', 'Limited', 'Inactive', 'Limited', 'https://snyk.io/advisor/npm-package/lol']
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Scraper.validate_snyk_results(results)
        f.close

    def test_validate_snyk_results_sad_popularity(self):
        results = ["npm-package", 'lol', '44', 'No known security issues', 'noexist', 'Inactive', 'Limited', 'https://snyk.io/advisor/npm-package/lol']
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Scraper.validate_snyk_results(results)
        f.close

    def test_validate_snyk_results_sad_maintenance(self):
        results = ["npm-package", 'lol', '44', 'No known security issues', 'Inactive', 'noexist', 'Limited', 'https://snyk.io/advisor/npm-package/lol']
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Scraper.validate_snyk_results(results)
        f.close

    def test_validate_snyk_results_sad_community(self):
        results = ["npm-package", 'lol', '44', 'No known security issues', 'Inactive', 'Inactive', 'noexist', 'https://snyk.io/advisor/npm-package/lol']
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Scraper.validate_snyk_results(results)
        f.close

    def test_validate_snyk_results_sad_url(self):
        results = ["npm-package", 'lol', '44', 'No known security issues', 'Inactive', 'Inactive', 'Limited', 'notaurl']
        f = StringIO()
        with redirect_stdout(f):        
            with self.assertRaises(SystemExit):
                Scraper.validate_snyk_results(results)
        f.close

if __name__ == "__main__":
    unittest.main()