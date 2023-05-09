
import unittest
import sys
sys.path.insert(0, '../src')
from src.analyzer import Analyzer
from io import StringIO
from contextlib import redirect_stdout
from os import path as path_check


class TestAnalyzer(unittest.TestCase):

    def test_exit_client_sad(self):
        results = [
            ['PASS', 'score', 'autoprefixer', '94', '80'], 
            ['PASS', 'security', 'autoprefixer', 'No known security issues', 'security issues found'], 
            ['FAIL', 'popularity', 'autoprefixer', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'autoprefixer', 'Healthy', 'inactive']
        ]
        with self.assertRaises(SystemExit) as raised:
            Analyzer.exit_client(results)
        self.assertEqual(raised.exception.code, 1)

    def test_exit_client_happy(self):
        results = [
            ['PASS', 'score', 'autoprefixer', '94', '80'], 
            ['PASS', 'security', 'autoprefixer', 'No known security issues', 'security issues found'], 
            ['PASS', 'popularity', 'autoprefixer', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'autoprefixer', 'Healthy', 'inactive']
        ]
        with self.assertRaises(SystemExit) as raised:
            Analyzer.exit_client(results)
        self.assertEqual(raised.exception.code, 0)


    def test_validate_scan_results_happy(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Key ecosystem project', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            ['npm-package', 'babel-core', '82', 'Security review needed', 'Key ecosystem project', 'Sustainable', 'Active', 'https://snyk.io/advisor/npm-package/babel-core'], 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        result = Analyzer.validate_scan_results(scan_results)
        assert result == ""

    def test_validate_scan_results_value_int(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Key ecosystem project', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            ['npm-package', 'babel-core', 82, 'Security review needed', 'Key ecosystem project', 'Sustainable', 'Active', 'https://snyk.io/advisor/npm-package/babel-core'], 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Analyzer.validate_scan_results(scan_results)
        f.close            


    def test_validate_scan_results_missing_values(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Key ecosystem project', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            ['Active', 'https://snyk.io/advisor/npm-package/babel-core'], 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Analyzer.validate_scan_results(scan_results)
        f.close            

    def test_validate_scan_results_entry_list(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Key ecosystem project', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            "", 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Analyzer.validate_scan_results(scan_results)
        f.close            

    def test_validate_scan_results_parent_list(self):
        scan_results = ""
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Analyzer.validate_scan_results(scan_results)
        f.close                

    def test_analyze_sad(self):
        scan_results = "breakme"
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Analyzer.analyze(scan_results)
        f.close        

    def test_analyze_baseline(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Key ecosystem project', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            ['npm-package', 'babel-core', '82', 'Security review needed', 'Key ecosystem project', 'Sustainable', 'Active', 'https://snyk.io/advisor/npm-package/babel-core'], 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        expected = [
            ['PASS', 'score', 'autoprefixer', '94', '80'], 
            ['PASS', 'security', 'autoprefixer', 'No known security issues', 'security issues found'], 
            ['PASS', 'popularity', 'autoprefixer', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'autoprefixer', 'Healthy', 'inactive'], 
            ['PASS', 'community', 'autoprefixer', 'Active', 'limited'], 
            ['PASS', 'score', 'babel-core', '82', '80'], 
            ['PASS', 'security', 'babel-core', 'Security review needed', 'security issues found'], 
            ['PASS', 'popularity', 'babel-core', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'babel-core', 'Sustainable', 'inactive'], 
            ['PASS', 'community', 'babel-core', 'Active', 'limited'], 
            ['FAIL', 'score', 'webpack-merge', '76', '80'], 
            ['PASS', 'security', 'webpack-merge', 'No known security issues', 'security issues found'], 
            ['PASS', 'popularity', 'webpack-merge', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'webpack-merge', 'Inactive', 'inactive'], 
            ['PASS', 'community', 'webpack-merge', 'Sustainable', 'limited']
        ]
        result = Analyzer.analyze(scan_results)
        assert result == expected

    def test_analyze_set_score(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Key ecosystem project', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            ['npm-package', 'babel-core', '82', 'Security review needed', 'Key ecosystem project', 'Sustainable', 'Active', 'https://snyk.io/advisor/npm-package/babel-core'], 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        expected = [
            ['PASS', 'score', 'autoprefixer', '94', '70'], 
            ['PASS', 'security', 'autoprefixer', 'No known security issues', 'security issues found'], 
            ['PASS', 'popularity', 'autoprefixer', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'autoprefixer', 'Healthy', 'inactive'], 
            ['PASS', 'community', 'autoprefixer', 'Active', 'limited'], 
            ['PASS', 'score', 'babel-core', '82', '70'], 
            ['PASS', 'security', 'babel-core', 'Security review needed', 'security issues found'], 
            ['PASS', 'popularity', 'babel-core', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'babel-core', 'Sustainable', 'inactive'], 
            ['PASS', 'community', 'babel-core', 'Active', 'limited'], 
            ['PASS', 'score', 'webpack-merge', '76', '70'], 
            ['PASS', 'security', 'webpack-merge', 'No known security issues', 'security issues found'], 
            ['PASS', 'popularity', 'webpack-merge', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'webpack-merge', 'Inactive', 'inactive'], 
            ['PASS', 'community', 'webpack-merge', 'Sustainable', 'limited']
        ]
        result = Analyzer.analyze(scan_results, 70)
        assert result == expected

    def test_analyze_set_security(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Key ecosystem project', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            ['npm-package', 'babel-core', '82', 'Security review needed', 'Key ecosystem project', 'Sustainable', 'Active', 'https://snyk.io/advisor/npm-package/babel-core'], 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        expected = [
            ['PASS', 'score', 'autoprefixer', '94', '70'], 
            ['PASS', 'security', 'autoprefixer', 'No known security issues', 'no known security issues'], 
            ['PASS', 'popularity', 'autoprefixer', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'autoprefixer', 'Healthy', 'inactive'], 
            ['PASS', 'community', 'autoprefixer', 'Active', 'limited'], 
            ['PASS', 'score', 'babel-core', '82', '70'], 
            ['FAIL', 'security', 'babel-core', 'Security review needed', 'no known security issues'], 
            ['PASS', 'popularity', 'babel-core', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'babel-core', 'Sustainable', 'inactive'], 
            ['PASS', 'community', 'babel-core', 'Active', 'limited'], 
            ['PASS', 'score', 'webpack-merge', '76', '70'], 
            ['PASS', 'security', 'webpack-merge', 'No known security issues', 'no known security issues'], 
            ['PASS', 'popularity', 'webpack-merge', 'Key ecosystem project', 'limited'], 
            ['PASS', 'maintenance', 'webpack-merge', 'Inactive', 'inactive'], 
            ['PASS', 'community', 'webpack-merge', 'Sustainable', 'limited']
        ]
        result = Analyzer.analyze(scan_results, 70, 2, 0, 0, 0)
        assert result == expected

    def test_analyze_set_popularity(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Popular', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            ['npm-package', 'babel-core', '82', 'Security review needed', 'Key ecosystem project', 'Sustainable', 'Active', 'https://snyk.io/advisor/npm-package/babel-core'], 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        expected = [
            ['PASS', 'score', 'autoprefixer', '94', '70'], 
            ['PASS', 'security', 'autoprefixer', 'No known security issues', 'no known security issues'], 
            ['FAIL', 'popularity', 'autoprefixer', 'Popular', 'key ecosystem project'], 
            ['PASS', 'maintenance', 'autoprefixer', 'Healthy', 'inactive'], 
            ['PASS', 'community', 'autoprefixer', 'Active', 'limited'], 
            ['PASS', 'score', 'babel-core', '82', '70'], 
            ['FAIL', 'security', 'babel-core', 'Security review needed', 'no known security issues'], 
            ['PASS', 'popularity', 'babel-core', 'Key ecosystem project', 'key ecosystem project'], 
            ['PASS', 'maintenance', 'babel-core', 'Sustainable', 'inactive'], 
            ['PASS', 'community', 'babel-core', 'Active', 'limited'], 
            ['PASS', 'score', 'webpack-merge', '76', '70'], 
            ['PASS', 'security', 'webpack-merge', 'No known security issues', 'no known security issues'], 
            ['PASS', 'popularity', 'webpack-merge', 'Key ecosystem project', 'key ecosystem project'], 
            ['PASS', 'maintenance', 'webpack-merge', 'Inactive', 'inactive'], 
            ['PASS', 'community', 'webpack-merge', 'Sustainable', 'limited']
        ]
        result = Analyzer.analyze(scan_results, 70, 2, 5, 0, 0)
        assert result == expected

    def test_analyze_set_maintenance(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Popular', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            ['npm-package', 'babel-core', '82', 'Security review needed', 'Key ecosystem project', 'Sustainable', 'Active', 'https://snyk.io/advisor/npm-package/babel-core'], 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        expected = [
            ['PASS', 'score', 'autoprefixer', '94', '70'], 
            ['PASS', 'security', 'autoprefixer', 'No known security issues', 'no known security issues'], 
            ['FAIL', 'popularity', 'autoprefixer', 'Popular', 'key ecosystem project'], 
            ['PASS', 'maintenance', 'autoprefixer', 'Healthy', 'healthy'], 
            ['PASS', 'community', 'autoprefixer', 'Active', 'limited'], 
            ['PASS', 'score', 'babel-core', '82', '70'], 
            ['FAIL', 'security', 'babel-core', 'Security review needed', 'no known security issues'], 
            ['PASS', 'popularity', 'babel-core', 'Key ecosystem project', 'key ecosystem project'], 
            ['FAIL', 'maintenance', 'babel-core', 'Sustainable', 'healthy'], 
            ['PASS', 'community', 'babel-core', 'Active', 'limited'], 
            ['PASS', 'score', 'webpack-merge', '76', '70'], 
            ['PASS', 'security', 'webpack-merge', 'No known security issues', 'no known security issues'], 
            ['PASS', 'popularity', 'webpack-merge', 'Key ecosystem project', 'key ecosystem project'], 
            ['FAIL', 'maintenance', 'webpack-merge', 'Inactive', 'healthy'], 
            ['PASS', 'community', 'webpack-merge', 'Sustainable', 'limited']
        ]
        result = Analyzer.analyze(scan_results, 70, 2, 5, 2, 0)
        assert result == expected

    def test_analyze_set_community(self):
        scan_results = [
            ['npm-package', 'autoprefixer', '94', 'No known security issues', 'Popular', 'Healthy', 'Active', 'https://snyk.io/advisor/npm-package/autoprefixer'], 
            ['npm-package', 'babel-core', '82', 'Security review needed', 'Key ecosystem project', 'Sustainable', 'Active', 'https://snyk.io/advisor/npm-package/babel-core'], 
            ['npm-package', 'webpack-merge', '76', 'No known security issues', 'Key ecosystem project', 'Inactive', 'Sustainable', 'https://snyk.io/advisor/npm-package/webpack-merge']
        ]
        expected = [
            ['PASS', 'score', 'autoprefixer', '94', '70'], 
            ['PASS', 'security', 'autoprefixer', 'No known security issues', 'no known security issues'], 
            ['FAIL', 'popularity', 'autoprefixer', 'Popular', 'key ecosystem project'], 
            ['PASS', 'maintenance', 'autoprefixer', 'Healthy', 'healthy'], 
            ['PASS', 'community', 'autoprefixer', 'Active', 'active'], 
            ['PASS', 'score', 'babel-core', '82', '70'], 
            ['FAIL', 'security', 'babel-core', 'Security review needed', 'no known security issues'], 
            ['PASS', 'popularity', 'babel-core', 'Key ecosystem project', 'key ecosystem project'], 
            ['FAIL', 'maintenance', 'babel-core', 'Sustainable', 'healthy'], 
            ['PASS', 'community', 'babel-core', 'Active', 'active'], 
            ['PASS', 'score', 'webpack-merge', '76', '70'], 
            ['PASS', 'security', 'webpack-merge', 'No known security issues', 'no known security issues'], 
            ['PASS', 'popularity', 'webpack-merge', 'Key ecosystem project', 'key ecosystem project'], 
            ['FAIL', 'maintenance', 'webpack-merge', 'Inactive', 'healthy'], 
            ['FAIL', 'community', 'webpack-merge', 'Sustainable', 'active']
        ]
        result = Analyzer.analyze(scan_results, 70, 2, 5, 2, 2)
        assert result == expected

if __name__ == "__main__":
    unittest.main()