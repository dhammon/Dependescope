
from prettytable import PrettyTable
from sys import exit
import json


class Reporter:

    def output_results(results, output_format):
        if output_format == "STDOUT":
            Reporter.standard_output(results)
        elif output_format == "JSON":
            Reporter.json_output(results)
        else:
            print("[-] Invalid output format")
            exit(255)

    def json_output(results):
        Reporter.validate_results(results)
        formated_results = []
        try:
            for result in results:
                formated_result = {
                    "Result": result[0],
                    "Category": result[1],
                    "Package": result[2],
                    "Measure": result[3],
                    "Threashold": result[4]
                }
                formated_results.append(formated_result)
            json_list = json.dumps(formated_results)
            print(json_list)
        except:
            print("[-] Reporting to JSON failed")
            exit(255)

    def standard_output(results):
        Reporter.validate_results(results)
        red = "\033[0;31;40m"
        green = "\033[0;32;40m"
        reset = "\033[0m"
        try:
            table = PrettyTable()
            table.field_names = ['Result', 'Category', 'Package', 'Measure', 'Threshold']
            for result in results:
                if result[0] == "PASS":
                    result[0] = green + result[0] + reset
                if result[0] == "FAIL":
                    result[0] = red + result[0] + reset
                table.add_row(result)
            print(table)
        except Exception:
            print("[-] Reporting to standard out failed")
            exit(255)
    
    def validate_results(results):
        if type(results) is not list:
            print("[-] Analysis results is not a list")
            exit(254)
        for entry in results:
            if type(entry) is not list:
                print("[-] Analysis results entries not a list")
                exit(254)
            if len(entry) != 5:
                print("[-] Analysis results entry count invalid")
                exit(254)
            for value in entry:
                if type(value) is not str:
                    print("[-] Analysis results value not string")
                    exit(254)
        return ""        