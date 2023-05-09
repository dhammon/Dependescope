
import unittest
import sys
sys.path.insert(0, '../src')
from src.reporter import Reporter
from io import StringIO
from contextlib import redirect_stdout
from os import path as path_check
import base64

class TestAnalyzer(unittest.TestCase):

    def test_output_results_happy_stdout(self):
        results = [
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
        output_format = "STDOUT"
        expected = "Ky0tLS0tLS0tKy0tLS0tLS0tLS0tLS0rLS0tLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKwp8IFJlc3VsdCB8ICAgQ2F0ZWdvcnkgIHwgICAgUGFja2FnZSAgICB8ICAgICAgICAgTWVhc3VyZSAgICAgICAgICB8ICAgICAgICBUaHJlc2hvbGQgICAgICAgICB8CistLS0tLS0tLSstLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLSstLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSstLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSsKfCAgG1swOzMyOzQwbVBBU1MbWzBtICB8ICAgIHNjb3JlICAgIHwgIGF1dG9wcmVmaXhlciB8ICAgICAgICAgICAgOTQgICAgICAgICAgICB8ICAgICAgICAgICAgNzAgICAgICAgICAgICB8CnwgIBtbMDszMjs0MG1QQVNTG1swbSAgfCAgIHNlY3VyaXR5ICB8ICBhdXRvcHJlZml4ZXIgfCBObyBrbm93biBzZWN1cml0eSBpc3N1ZXMgfCBubyBrbm93biBzZWN1cml0eSBpc3N1ZXMgfAp8ICAbWzA7MzE7NDBtRkFJTBtbMG0gIHwgIHBvcHVsYXJpdHkgfCAgYXV0b3ByZWZpeGVyIHwgICAgICAgICBQb3B1bGFyICAgICAgICAgIHwgIGtleSBlY29zeXN0ZW0gcHJvamVjdCAgIHwKfCAgG1swOzMyOzQwbVBBU1MbWzBtICB8IG1haW50ZW5hbmNlIHwgIGF1dG9wcmVmaXhlciB8ICAgICAgICAgSGVhbHRoeSAgICAgICAgICB8ICAgICAgICAgaGVhbHRoeSAgICAgICAgICB8CnwgIBtbMDszMjs0MG1QQVNTG1swbSAgfCAgY29tbXVuaXR5ICB8ICBhdXRvcHJlZml4ZXIgfCAgICAgICAgICBBY3RpdmUgICAgICAgICAgfCAgICAgICAgICBhY3RpdmUgICAgICAgICAgfAp8ICAbWzA7MzI7NDBtUEFTUxtbMG0gIHwgICAgc2NvcmUgICAgfCAgIGJhYmVsLWNvcmUgIHwgICAgICAgICAgICA4MiAgICAgICAgICAgIHwgICAgICAgICAgICA3MCAgICAgICAgICAgIHwKfCAgG1swOzMxOzQwbUZBSUwbWzBtICB8ICAgc2VjdXJpdHkgIHwgICBiYWJlbC1jb3JlICB8ICBTZWN1cml0eSByZXZpZXcgbmVlZGVkICB8IG5vIGtub3duIHNlY3VyaXR5IGlzc3VlcyB8CnwgIBtbMDszMjs0MG1QQVNTG1swbSAgfCAgcG9wdWxhcml0eSB8ICAgYmFiZWwtY29yZSAgfCAgS2V5IGVjb3N5c3RlbSBwcm9qZWN0ICAgfCAga2V5IGVjb3N5c3RlbSBwcm9qZWN0ICAgfAp8ICAbWzA7MzE7NDBtRkFJTBtbMG0gIHwgbWFpbnRlbmFuY2UgfCAgIGJhYmVsLWNvcmUgIHwgICAgICAgU3VzdGFpbmFibGUgICAgICAgIHwgICAgICAgICBoZWFsdGh5ICAgICAgICAgIHwKfCAgG1swOzMyOzQwbVBBU1MbWzBtICB8ICBjb21tdW5pdHkgIHwgICBiYWJlbC1jb3JlICB8ICAgICAgICAgIEFjdGl2ZSAgICAgICAgICB8ICAgICAgICAgIGFjdGl2ZSAgICAgICAgICB8CnwgIBtbMDszMjs0MG1QQVNTG1swbSAgfCAgICBzY29yZSAgICB8IHdlYnBhY2stbWVyZ2UgfCAgICAgICAgICAgIDc2ICAgICAgICAgICAgfCAgICAgICAgICAgIDcwICAgICAgICAgICAgfAp8ICAbWzA7MzI7NDBtUEFTUxtbMG0gIHwgICBzZWN1cml0eSAgfCB3ZWJwYWNrLW1lcmdlIHwgTm8ga25vd24gc2VjdXJpdHkgaXNzdWVzIHwgbm8ga25vd24gc2VjdXJpdHkgaXNzdWVzIHwKfCAgG1swOzMyOzQwbVBBU1MbWzBtICB8ICBwb3B1bGFyaXR5IHwgd2VicGFjay1tZXJnZSB8ICBLZXkgZWNvc3lzdGVtIHByb2plY3QgICB8ICBrZXkgZWNvc3lzdGVtIHByb2plY3QgICB8CnwgIBtbMDszMTs0MG1GQUlMG1swbSAgfCBtYWludGVuYW5jZSB8IHdlYnBhY2stbWVyZ2UgfCAgICAgICAgIEluYWN0aXZlICAgICAgICAgfCAgICAgICAgIGhlYWx0aHkgICAgICAgICAgfAp8ICAbWzA7MzE7NDBtRkFJTBtbMG0gIHwgIGNvbW11bml0eSAgfCB3ZWJwYWNrLW1lcmdlIHwgICAgICAgU3VzdGFpbmFibGUgICAgICAgIHwgICAgICAgICAgYWN0aXZlICAgICAgICAgIHwKKy0tLS0tLS0tKy0tLS0tLS0tLS0tLS0rLS0tLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKwo="
        f = StringIO()
        with redirect_stdout(f):
            Reporter.output_results(results, output_format)
        string_bytes = f.getvalue().encode("ascii")
        base64_string = base64.b64encode(string_bytes)
        assert base64_string.decode("ascii") == expected
        f.close  

    def test_output_results_sad(self):
        results = "breakme"
        output_format = "breakme"
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Reporter.output_results(results, output_format)
        f.close

    def test_output_results_happy_json(self):
        results = [
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
        output_format = "JSON"
        expected = 'W3siUmVzdWx0IjogIlBBU1MiLCAiQ2F0ZWdvcnkiOiAic2NvcmUiLCAiUGFja2FnZSI6ICJhdXRvcHJlZml4ZXIiLCAiTWVhc3VyZSI6ICI5NCIsICJUaHJlYXNob2xkIjogIjcwIn0sIHsiUmVzdWx0IjogIlBBU1MiLCAiQ2F0ZWdvcnkiOiAic2VjdXJpdHkiLCAiUGFja2FnZSI6ICJhdXRvcHJlZml4ZXIiLCAiTWVhc3VyZSI6ICJObyBrbm93biBzZWN1cml0eSBpc3N1ZXMiLCAiVGhyZWFzaG9sZCI6ICJubyBrbm93biBzZWN1cml0eSBpc3N1ZXMifSwgeyJSZXN1bHQiOiAiRkFJTCIsICJDYXRlZ29yeSI6ICJwb3B1bGFyaXR5IiwgIlBhY2thZ2UiOiAiYXV0b3ByZWZpeGVyIiwgIk1lYXN1cmUiOiAiUG9wdWxhciIsICJUaHJlYXNob2xkIjogImtleSBlY29zeXN0ZW0gcHJvamVjdCJ9LCB7IlJlc3VsdCI6ICJQQVNTIiwgIkNhdGVnb3J5IjogIm1haW50ZW5hbmNlIiwgIlBhY2thZ2UiOiAiYXV0b3ByZWZpeGVyIiwgIk1lYXN1cmUiOiAiSGVhbHRoeSIsICJUaHJlYXNob2xkIjogImhlYWx0aHkifSwgeyJSZXN1bHQiOiAiUEFTUyIsICJDYXRlZ29yeSI6ICJjb21tdW5pdHkiLCAiUGFja2FnZSI6ICJhdXRvcHJlZml4ZXIiLCAiTWVhc3VyZSI6ICJBY3RpdmUiLCAiVGhyZWFzaG9sZCI6ICJhY3RpdmUifSwgeyJSZXN1bHQiOiAiUEFTUyIsICJDYXRlZ29yeSI6ICJzY29yZSIsICJQYWNrYWdlIjogImJhYmVsLWNvcmUiLCAiTWVhc3VyZSI6ICI4MiIsICJUaHJlYXNob2xkIjogIjcwIn0sIHsiUmVzdWx0IjogIkZBSUwiLCAiQ2F0ZWdvcnkiOiAic2VjdXJpdHkiLCAiUGFja2FnZSI6ICJiYWJlbC1jb3JlIiwgIk1lYXN1cmUiOiAiU2VjdXJpdHkgcmV2aWV3IG5lZWRlZCIsICJUaHJlYXNob2xkIjogIm5vIGtub3duIHNlY3VyaXR5IGlzc3VlcyJ9LCB7IlJlc3VsdCI6ICJQQVNTIiwgIkNhdGVnb3J5IjogInBvcHVsYXJpdHkiLCAiUGFja2FnZSI6ICJiYWJlbC1jb3JlIiwgIk1lYXN1cmUiOiAiS2V5IGVjb3N5c3RlbSBwcm9qZWN0IiwgIlRocmVhc2hvbGQiOiAia2V5IGVjb3N5c3RlbSBwcm9qZWN0In0sIHsiUmVzdWx0IjogIkZBSUwiLCAiQ2F0ZWdvcnkiOiAibWFpbnRlbmFuY2UiLCAiUGFja2FnZSI6ICJiYWJlbC1jb3JlIiwgIk1lYXN1cmUiOiAiU3VzdGFpbmFibGUiLCAiVGhyZWFzaG9sZCI6ICJoZWFsdGh5In0sIHsiUmVzdWx0IjogIlBBU1MiLCAiQ2F0ZWdvcnkiOiAiY29tbXVuaXR5IiwgIlBhY2thZ2UiOiAiYmFiZWwtY29yZSIsICJNZWFzdXJlIjogIkFjdGl2ZSIsICJUaHJlYXNob2xkIjogImFjdGl2ZSJ9LCB7IlJlc3VsdCI6ICJQQVNTIiwgIkNhdGVnb3J5IjogInNjb3JlIiwgIlBhY2thZ2UiOiAid2VicGFjay1tZXJnZSIsICJNZWFzdXJlIjogIjc2IiwgIlRocmVhc2hvbGQiOiAiNzAifSwgeyJSZXN1bHQiOiAiUEFTUyIsICJDYXRlZ29yeSI6ICJzZWN1cml0eSIsICJQYWNrYWdlIjogIndlYnBhY2stbWVyZ2UiLCAiTWVhc3VyZSI6ICJObyBrbm93biBzZWN1cml0eSBpc3N1ZXMiLCAiVGhyZWFzaG9sZCI6ICJubyBrbm93biBzZWN1cml0eSBpc3N1ZXMifSwgeyJSZXN1bHQiOiAiUEFTUyIsICJDYXRlZ29yeSI6ICJwb3B1bGFyaXR5IiwgIlBhY2thZ2UiOiAid2VicGFjay1tZXJnZSIsICJNZWFzdXJlIjogIktleSBlY29zeXN0ZW0gcHJvamVjdCIsICJUaHJlYXNob2xkIjogImtleSBlY29zeXN0ZW0gcHJvamVjdCJ9LCB7IlJlc3VsdCI6ICJGQUlMIiwgIkNhdGVnb3J5IjogIm1haW50ZW5hbmNlIiwgIlBhY2thZ2UiOiAid2VicGFjay1tZXJnZSIsICJNZWFzdXJlIjogIkluYWN0aXZlIiwgIlRocmVhc2hvbGQiOiAiaGVhbHRoeSJ9LCB7IlJlc3VsdCI6ICJGQUlMIiwgIkNhdGVnb3J5IjogImNvbW11bml0eSIsICJQYWNrYWdlIjogIndlYnBhY2stbWVyZ2UiLCAiTWVhc3VyZSI6ICJTdXN0YWluYWJsZSIsICJUaHJlYXNob2xkIjogImFjdGl2ZSJ9XQo='
        f = StringIO()
        with redirect_stdout(f):
            Reporter.output_results(results, output_format)
        string_bytes = f.getvalue().encode("ascii")
        base64_string = base64.b64encode(string_bytes)
        assert base64_string.decode("ascii") == expected
        f.close        

    def test_json_output_sad(self):
        results = "breakme"
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Reporter.json_output(results)
        f.close

    def test_json_output_happy(self):
        results = [
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
        #expected = '[{"Result": "PASS", "Category": "score", "Package": "autoprefixer", "Measure": "94", "Threashold": "70"}, {"Result": "PASS", "Category": "security", "Package": "autoprefixer", "Measure": "No known security issues", "Threashold": "no known security issues"}, {"Result": "FAIL", "Category": "popularity", "Package": "autoprefixer", "Measure": "Popular", "Threashold": "key ecosystem project"}, {"Result": "PASS", "Category": "maintenance", "Package": "autoprefixer", "Measure": "Healthy", "Threashold": "healthy"}, {"Result": "PASS", "Category": "community", "Package": "autoprefixer", "Measure": "Active", "Threashold": "active"}, {"Result": "PASS", "Category": "score", "Package": "babel-core", "Measure": "82", "Threashold": "70"}, {"Result": "FAIL", "Category": "security", "Package": "babel-core", "Measure": "Security review needed", "Threashold": "no known security issues"}, {"Result": "PASS", "Category": "popularity", "Package": "babel-core", "Measure": "Key ecosystem project", "Threashold": "key ecosystem project"}, {"Result": "FAIL", "Category": "maintenance", "Package": "babel-core", "Measure": "Sustainable", "Threashold": "healthy"}, {"Result": "PASS", "Category": "community", "Package": "babel-core", "Measure": "Active", "Threashold": "active"}, {"Result": "PASS", "Category": "score", "Package": "webpack-merge", "Measure": "76", "Threashold": "70"}, {"Result": "PASS", "Category": "security", "Package": "webpack-merge", "Measure": "No known security issues", "Threashold": "no known security issues"}, {"Result": "PASS", "Category": "popularity", "Package": "webpack-merge", "Measure": "Key ecosystem project", "Threashold": "key ecosystem project"}, {"Result": "FAIL", "Category": "maintenance", "Package": "webpack-merge", "Measure": "Inactive", "Threashold": "healthy"}, {"Result": "FAIL", "Category": "community", "Package": "webpack-merge", "Measure": "Sustainable", "Threashold": "active"}]'
        expected = 'W3siUmVzdWx0IjogIlBBU1MiLCAiQ2F0ZWdvcnkiOiAic2NvcmUiLCAiUGFja2FnZSI6ICJhdXRvcHJlZml4ZXIiLCAiTWVhc3VyZSI6ICI5NCIsICJUaHJlYXNob2xkIjogIjcwIn0sIHsiUmVzdWx0IjogIlBBU1MiLCAiQ2F0ZWdvcnkiOiAic2VjdXJpdHkiLCAiUGFja2FnZSI6ICJhdXRvcHJlZml4ZXIiLCAiTWVhc3VyZSI6ICJObyBrbm93biBzZWN1cml0eSBpc3N1ZXMiLCAiVGhyZWFzaG9sZCI6ICJubyBrbm93biBzZWN1cml0eSBpc3N1ZXMifSwgeyJSZXN1bHQiOiAiRkFJTCIsICJDYXRlZ29yeSI6ICJwb3B1bGFyaXR5IiwgIlBhY2thZ2UiOiAiYXV0b3ByZWZpeGVyIiwgIk1lYXN1cmUiOiAiUG9wdWxhciIsICJUaHJlYXNob2xkIjogImtleSBlY29zeXN0ZW0gcHJvamVjdCJ9LCB7IlJlc3VsdCI6ICJQQVNTIiwgIkNhdGVnb3J5IjogIm1haW50ZW5hbmNlIiwgIlBhY2thZ2UiOiAiYXV0b3ByZWZpeGVyIiwgIk1lYXN1cmUiOiAiSGVhbHRoeSIsICJUaHJlYXNob2xkIjogImhlYWx0aHkifSwgeyJSZXN1bHQiOiAiUEFTUyIsICJDYXRlZ29yeSI6ICJjb21tdW5pdHkiLCAiUGFja2FnZSI6ICJhdXRvcHJlZml4ZXIiLCAiTWVhc3VyZSI6ICJBY3RpdmUiLCAiVGhyZWFzaG9sZCI6ICJhY3RpdmUifSwgeyJSZXN1bHQiOiAiUEFTUyIsICJDYXRlZ29yeSI6ICJzY29yZSIsICJQYWNrYWdlIjogImJhYmVsLWNvcmUiLCAiTWVhc3VyZSI6ICI4MiIsICJUaHJlYXNob2xkIjogIjcwIn0sIHsiUmVzdWx0IjogIkZBSUwiLCAiQ2F0ZWdvcnkiOiAic2VjdXJpdHkiLCAiUGFja2FnZSI6ICJiYWJlbC1jb3JlIiwgIk1lYXN1cmUiOiAiU2VjdXJpdHkgcmV2aWV3IG5lZWRlZCIsICJUaHJlYXNob2xkIjogIm5vIGtub3duIHNlY3VyaXR5IGlzc3VlcyJ9LCB7IlJlc3VsdCI6ICJQQVNTIiwgIkNhdGVnb3J5IjogInBvcHVsYXJpdHkiLCAiUGFja2FnZSI6ICJiYWJlbC1jb3JlIiwgIk1lYXN1cmUiOiAiS2V5IGVjb3N5c3RlbSBwcm9qZWN0IiwgIlRocmVhc2hvbGQiOiAia2V5IGVjb3N5c3RlbSBwcm9qZWN0In0sIHsiUmVzdWx0IjogIkZBSUwiLCAiQ2F0ZWdvcnkiOiAibWFpbnRlbmFuY2UiLCAiUGFja2FnZSI6ICJiYWJlbC1jb3JlIiwgIk1lYXN1cmUiOiAiU3VzdGFpbmFibGUiLCAiVGhyZWFzaG9sZCI6ICJoZWFsdGh5In0sIHsiUmVzdWx0IjogIlBBU1MiLCAiQ2F0ZWdvcnkiOiAiY29tbXVuaXR5IiwgIlBhY2thZ2UiOiAiYmFiZWwtY29yZSIsICJNZWFzdXJlIjogIkFjdGl2ZSIsICJUaHJlYXNob2xkIjogImFjdGl2ZSJ9LCB7IlJlc3VsdCI6ICJQQVNTIiwgIkNhdGVnb3J5IjogInNjb3JlIiwgIlBhY2thZ2UiOiAid2VicGFjay1tZXJnZSIsICJNZWFzdXJlIjogIjc2IiwgIlRocmVhc2hvbGQiOiAiNzAifSwgeyJSZXN1bHQiOiAiUEFTUyIsICJDYXRlZ29yeSI6ICJzZWN1cml0eSIsICJQYWNrYWdlIjogIndlYnBhY2stbWVyZ2UiLCAiTWVhc3VyZSI6ICJObyBrbm93biBzZWN1cml0eSBpc3N1ZXMiLCAiVGhyZWFzaG9sZCI6ICJubyBrbm93biBzZWN1cml0eSBpc3N1ZXMifSwgeyJSZXN1bHQiOiAiUEFTUyIsICJDYXRlZ29yeSI6ICJwb3B1bGFyaXR5IiwgIlBhY2thZ2UiOiAid2VicGFjay1tZXJnZSIsICJNZWFzdXJlIjogIktleSBlY29zeXN0ZW0gcHJvamVjdCIsICJUaHJlYXNob2xkIjogImtleSBlY29zeXN0ZW0gcHJvamVjdCJ9LCB7IlJlc3VsdCI6ICJGQUlMIiwgIkNhdGVnb3J5IjogIm1haW50ZW5hbmNlIiwgIlBhY2thZ2UiOiAid2VicGFjay1tZXJnZSIsICJNZWFzdXJlIjogIkluYWN0aXZlIiwgIlRocmVhc2hvbGQiOiAiaGVhbHRoeSJ9LCB7IlJlc3VsdCI6ICJGQUlMIiwgIkNhdGVnb3J5IjogImNvbW11bml0eSIsICJQYWNrYWdlIjogIndlYnBhY2stbWVyZ2UiLCAiTWVhc3VyZSI6ICJTdXN0YWluYWJsZSIsICJUaHJlYXNob2xkIjogImFjdGl2ZSJ9XQo='
        f = StringIO()
        with redirect_stdout(f):
            Reporter.json_output(results)
        string_bytes = f.getvalue().encode("ascii")
        base64_string = base64.b64encode(string_bytes)
        assert base64_string.decode("ascii") == expected
        f.close

    def test_standard_output_happy(self):
        results = [
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
        expected = "Ky0tLS0tLS0tKy0tLS0tLS0tLS0tLS0rLS0tLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKwp8IFJlc3VsdCB8ICAgQ2F0ZWdvcnkgIHwgICAgUGFja2FnZSAgICB8ICAgICAgICAgTWVhc3VyZSAgICAgICAgICB8ICAgICAgICBUaHJlc2hvbGQgICAgICAgICB8CistLS0tLS0tLSstLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLSstLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSstLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSsKfCAgG1swOzMyOzQwbVBBU1MbWzBtICB8ICAgIHNjb3JlICAgIHwgIGF1dG9wcmVmaXhlciB8ICAgICAgICAgICAgOTQgICAgICAgICAgICB8ICAgICAgICAgICAgNzAgICAgICAgICAgICB8CnwgIBtbMDszMjs0MG1QQVNTG1swbSAgfCAgIHNlY3VyaXR5ICB8ICBhdXRvcHJlZml4ZXIgfCBObyBrbm93biBzZWN1cml0eSBpc3N1ZXMgfCBubyBrbm93biBzZWN1cml0eSBpc3N1ZXMgfAp8ICAbWzA7MzE7NDBtRkFJTBtbMG0gIHwgIHBvcHVsYXJpdHkgfCAgYXV0b3ByZWZpeGVyIHwgICAgICAgICBQb3B1bGFyICAgICAgICAgIHwgIGtleSBlY29zeXN0ZW0gcHJvamVjdCAgIHwKfCAgG1swOzMyOzQwbVBBU1MbWzBtICB8IG1haW50ZW5hbmNlIHwgIGF1dG9wcmVmaXhlciB8ICAgICAgICAgSGVhbHRoeSAgICAgICAgICB8ICAgICAgICAgaGVhbHRoeSAgICAgICAgICB8CnwgIBtbMDszMjs0MG1QQVNTG1swbSAgfCAgY29tbXVuaXR5ICB8ICBhdXRvcHJlZml4ZXIgfCAgICAgICAgICBBY3RpdmUgICAgICAgICAgfCAgICAgICAgICBhY3RpdmUgICAgICAgICAgfAp8ICAbWzA7MzI7NDBtUEFTUxtbMG0gIHwgICAgc2NvcmUgICAgfCAgIGJhYmVsLWNvcmUgIHwgICAgICAgICAgICA4MiAgICAgICAgICAgIHwgICAgICAgICAgICA3MCAgICAgICAgICAgIHwKfCAgG1swOzMxOzQwbUZBSUwbWzBtICB8ICAgc2VjdXJpdHkgIHwgICBiYWJlbC1jb3JlICB8ICBTZWN1cml0eSByZXZpZXcgbmVlZGVkICB8IG5vIGtub3duIHNlY3VyaXR5IGlzc3VlcyB8CnwgIBtbMDszMjs0MG1QQVNTG1swbSAgfCAgcG9wdWxhcml0eSB8ICAgYmFiZWwtY29yZSAgfCAgS2V5IGVjb3N5c3RlbSBwcm9qZWN0ICAgfCAga2V5IGVjb3N5c3RlbSBwcm9qZWN0ICAgfAp8ICAbWzA7MzE7NDBtRkFJTBtbMG0gIHwgbWFpbnRlbmFuY2UgfCAgIGJhYmVsLWNvcmUgIHwgICAgICAgU3VzdGFpbmFibGUgICAgICAgIHwgICAgICAgICBoZWFsdGh5ICAgICAgICAgIHwKfCAgG1swOzMyOzQwbVBBU1MbWzBtICB8ICBjb21tdW5pdHkgIHwgICBiYWJlbC1jb3JlICB8ICAgICAgICAgIEFjdGl2ZSAgICAgICAgICB8ICAgICAgICAgIGFjdGl2ZSAgICAgICAgICB8CnwgIBtbMDszMjs0MG1QQVNTG1swbSAgfCAgICBzY29yZSAgICB8IHdlYnBhY2stbWVyZ2UgfCAgICAgICAgICAgIDc2ICAgICAgICAgICAgfCAgICAgICAgICAgIDcwICAgICAgICAgICAgfAp8ICAbWzA7MzI7NDBtUEFTUxtbMG0gIHwgICBzZWN1cml0eSAgfCB3ZWJwYWNrLW1lcmdlIHwgTm8ga25vd24gc2VjdXJpdHkgaXNzdWVzIHwgbm8ga25vd24gc2VjdXJpdHkgaXNzdWVzIHwKfCAgG1swOzMyOzQwbVBBU1MbWzBtICB8ICBwb3B1bGFyaXR5IHwgd2VicGFjay1tZXJnZSB8ICBLZXkgZWNvc3lzdGVtIHByb2plY3QgICB8ICBrZXkgZWNvc3lzdGVtIHByb2plY3QgICB8CnwgIBtbMDszMTs0MG1GQUlMG1swbSAgfCBtYWludGVuYW5jZSB8IHdlYnBhY2stbWVyZ2UgfCAgICAgICAgIEluYWN0aXZlICAgICAgICAgfCAgICAgICAgIGhlYWx0aHkgICAgICAgICAgfAp8ICAbWzA7MzE7NDBtRkFJTBtbMG0gIHwgIGNvbW11bml0eSAgfCB3ZWJwYWNrLW1lcmdlIHwgICAgICAgU3VzdGFpbmFibGUgICAgICAgIHwgICAgICAgICAgYWN0aXZlICAgICAgICAgIHwKKy0tLS0tLS0tKy0tLS0tLS0tLS0tLS0rLS0tLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKy0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKwo="
        f = StringIO()
        with redirect_stdout(f):
            Reporter.standard_output(results)
        string_bytes = f.getvalue().encode("ascii")
        base64_string = base64.b64encode(string_bytes)
        assert base64_string.decode("ascii") == expected
        f.close
    
    def test_standard_output_sad(self):
        results = "breakme"
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Reporter.standard_output(results)
        f.close
    
    def test_validate_results_happy(self):
        results = [
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
        expected = ""
        result = Reporter.validate_results(results)
        assert result == expected

    def test_validate_results_sad_string(self):
        results = "breakme"
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Reporter.validate_results(results)
        f.close

    def test_validate_results_sad_entry(self):
        results = ["breakme"]
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Reporter.validate_results(results)
        f.close

    def test_validate_results_sad_count(self):
        results = [
            ['PASS'], 
            ['PASS', 'security', 'autoprefixer', 'No known security issues', 'no known security issues'], 
            ['FAIL', 'popularity', 'autoprefixer', 'Popular', 'key ecosystem project']
        ]
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Reporter.validate_results(results)
        f.close

    def test_validate_results_sad_type(self):
        results = [
            ['PASS', 'security', 'autoprefixer', False, 'no known security issues'], 
            ['FAIL', 'popularity', 'autoprefixer', 'Popular', 'key ecosystem project']
        ]
        f = StringIO()
        with redirect_stdout(f):
            with self.assertRaises(SystemExit):
                Reporter.validate_results(results)
        f.close

if __name__ == "__main__":
    unittest.main()