
import argparse
from src.analyzer import Analyzer
from src.file_helper import FileHelper
from src.reporter import Reporter
from src.scanner import Scanner
from src.validator import Validator


def handle_args(inputs):
    parser = argparse.ArgumentParser()
    parser.add_argument('--package-file-path', required = True, action='store', help="Path to package file. Example /path/to/package.json")
    parser.add_argument('--output-format', action='store', default="STDOUT", help="Output format in JSON or STDOUT.  Default STDOUT")
    parser.add_argument('--no-banner', action='store_true', default=False, help="Do not display banner. Default False")
    parser.add_argument('--score-threshold', action='store', type=int, default=80, help='Minimum passing overall score. Default 80')
    parser.add_argument('--security-threshold', action='store', type=int, default=0, help='Minimum passing security score. 0-2; 0=Security issues found, 1=Security review needed, 2=No known security issues. Default 0')
    parser.add_argument('--popularity-threshold', action='store', type=int, default=0, help='Minimum passing popularity score. 0-5; 0=Limited, 1=Small, 2=Recognized, 3=Popular, 4=Influential project, 5=Key ecosystem project. Default 0')
    parser.add_argument('--maintenance-threshold', action='store', type=int, default=0, help='Minimum passing maintenance score. 0-2; 0=Inactive, 1=Sustainable, 2=Healthy. Default 0')
    parser.add_argument('--community-threshold', action='store', type=int, default=0, help='Minimum passing community score. 0-2; 0=Limited, 1=Sustainable, 2=Active. Default 0')
    args = parser.parse_args(inputs)
    return args

def banner():
    title = """
  _____                            _                                
 |  __ \                          | |                               
 | |  | | ___ _ __   ___ _ __   __| | ___  ___  ___ ___  _ __   ___ 
 | |  | |/ _ \ '_ \ / _ \ '_ \ / _` |/ _ \/ __|/ __/ _ \| '_ \ / _ \\
 | |__| |  __/ |_) |  __/ | | | (_| |  __/\__ \ (_| (_) | |_) |  __/
 |_____/ \___| .__/ \___|_| |_|\__,_|\___||___/\___\___/| .__/ \___|
             | |                                        | |         
             |_|                                        |_|         


The package health checker

--------------------------------------------------------------------

    """
    print(title)

def validate_inputs(inputs):
    Validator.validate_input_list(inputs)
    for input in inputs:
        if "--package-file-path" in input:
            Validator.validate_path(input.replace("--package-file-path=",""))
        if "--output-format" in input:
            Validator.validate_output_format(input.replace("--output-format=",""))
        if "--score-threshold" in input:
            Validator.validate_score_threshold(input.replace("--score-threshold=",""))
        if "--security-threshold" in input:
            Validator.validate_security_threshold(input.replace("--security-threshold=",""))
        if "--popularity-threshold" in input:
            Validator.validate_popularity_threshold(input.replace("--popularity-threshold=",""))
        if "--maintenance-threshold" in input:
            Validator.validate_maintenance_threshold(input.replace("--maintenance-threshold=",""))
        if "--community-threshold" in input:
            Validator.validate_community_threshold(input.replace("--community-threshold=",""))

def run(inputs):
    if inputs is not None:
        validate_inputs(inputs)
        if "--no-banner" not in inputs:
            banner()
        args = handle_args(inputs)
        path = args.package_file_path
        output_format = args.output_format
        registry = FileHelper.find_registry_type(path)
        # file deepcode ignore PT: Validated downstream
        # deepcode ignore Ssrf: Validated downstream
        scan_results = Scanner.scan(registry, path)
        results = Analyzer.analyze(scan_results)
        Reporter.output_results(results, output_format)
        Analyzer.exit_client(results)
    banner()
    handle_args(["--help"])