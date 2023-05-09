
import json
from os import path as path_check
from sys import exit
from src.validator import Validator


class FileHelper:

    def find_registry_type(path):
        Validator.validate_path(path)
        file_name = path_check.basename(path)
        if file_name == "requirements.txt":
            return "python"
        if file_name == "package.json":
            return "npm-package"
        else:
            print("[-] Resgistry not found")
            exit(255)

    def get_npm_packages(path):
        Validator.validate_path(path)
        package_file = open(path)
        data = json.load(package_file)
        packages = list(data['dependencies'].keys())
        package_file.close()
        return packages

    def get_pypi_packages(path):
        Validator.validate_path(path)
        packages = []
        package_file = open(path)
        for line in package_file:
            line = line.replace("=", " ")
            words = line.split()
            packages.append(words[0])
        package_file.close()
        return packages
