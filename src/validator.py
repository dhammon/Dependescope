
from os import path as path_check
from sys import exit


class Validator():

    def validate_community_threshold(value):
        if value < 0 or value > 2 or not value % 1 == 0:
            print("[-] Community threshold invalid")
            exit(254)
        return ""
    
    def validate_maintenance_threshold(value):
        if value < 0 or value > 2 or not value % 1 == 0:
            print("[-] Maintenance threshold invalid")
            exit(254)
        return ""

    def validate_popularity_threshold(value):
        if value < 0 or value > 5 or not value % 1 == 0:
            print("[-] Popularity threshold invalid")
            exit(254)
        return ""

    def validate_security_threshold(value):
        if value < 0 or value > 2 or not value % 1 == 0:
            print("[-] Security threshold invalid")
            exit(254)
        return ""

    def validate_score_threshold(value):
        if value < 0 or value > 100 or not value % 1 == 0:
            print("[-] Score threshold invalid")
            exit(254)
        return ""

    def validate_output_format(input):
        allowed_values = ["JSON", "STDOUT"]
        if input not in allowed_values:
            print("[-] Output format invalid")
            exit(254)
        return ""

    def validate_input_list(inputs):
        if type(inputs) is not list:
            print("[-] Inputs not a list")
            exit(254)
        return ""

    def validate_path(path):
        allowed_filenames = ["requirements.txt", "package.json"]
        base_name = path_check.basename(path)
        if base_name not in allowed_filenames:
            print("[-] Path basename invalid")
            exit(254)
        if not path_check.isfile(path):
            print("[-] Path invalid")
            exit(254)
        return ""