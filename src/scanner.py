
from sys import exit
from sys import path
path.insert(0, '../src')
from src.scraper import Scraper
from src.file_helper import FileHelper
from src.validator import Validator


class Scanner:
    #TODO dep injection to make more testable
    def scan(registry, path):
        scan_results = []
        Scanner.validate_registry(registry)
        Validator.validate_path(path)
        if registry == "npm-package":
            registry_snyk_path = "npm-package"
            packages = FileHelper.get_npm_packages(path)
        if registry == "python":
            registry_snyk_path = "python"
            packages = FileHelper.get_pypi_packages(path)
        for package in packages:
            result = Scraper.check_snyk_advisor(registry_snyk_path, package)
            scan_results.append(result)
        return scan_results
        
    
    def validate_registry(registry):
        allowed_registries = ["npm-package", "python"]
        if registry not in allowed_registries:
            print("[-] Registry invalid")
            exit(254)
        return ""
