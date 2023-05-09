
from sys import exit

class Analyzer:

    security_values = ["security issues found", "security review needed", "no known security issues"]
    popularity_values = ["limited", "small", "recognized", "popular", "influential project", "key ecosystem project"]
    maintenance_values = ["inactive", "sustainable", "healthy"]
    community_values = ["limited", "sustainable", "active"]

    def exit_client(results):
        for result in results:
            if "FAIL" in result[0]:
                exit(1)
        return exit(0)

    #TODO analysis checks little stinky
    def analyze(scan_results, score_threshold=80, security_threshold=0, popularity_threshold=0, maintenance_threshold=0, community_threshold=0):
        results = []
        Analyzer.validate_scan_results(scan_results)
        try:
            for scan_result in scan_results:
                package_name = scan_result[1]
                score = scan_result[2]
                security = scan_result[3]
                popularity = scan_result[4]
                maintenance = scan_result[5]
                community = scan_result[6]
                #score analysis
                test = "score"
                result = "FAIL"
                if score >= str(score_threshold):
                    result = "PASS"
                entry = [result, test, package_name, score, str(score_threshold)]
                results.append(entry)
                #security analysis
                test = "security"
                index = Analyzer.security_values.index(security.lower())
                result = "FAIL"
                if index >= security_threshold:
                    result = "PASS"
                entry = [result, test, package_name, security, Analyzer.security_values[security_threshold]]
                results.append(entry)
                #popularity analysis
                test = "popularity"
                index = Analyzer.popularity_values.index(popularity.lower())
                result = "FAIL"
                if index >= popularity_threshold:
                    result = "PASS"
                entry = [result, test, package_name, popularity, Analyzer.popularity_values[popularity_threshold]]
                results.append(entry)
                #maintenance analysis
                test = "maintenance"
                index = Analyzer.maintenance_values.index(maintenance.lower())
                result = "FAIL"
                if index >= maintenance_threshold:
                    result = "PASS"
                entry = [result, test, package_name, maintenance, Analyzer.maintenance_values[maintenance_threshold]]
                results.append(entry)
                #community analysis
                test = "community"
                index = Analyzer.community_values.index(community.lower())
                result = "FAIL"
                if index >= community_threshold:
                    result = "PASS"
                entry = [result, test, package_name, community, Analyzer.community_values[community_threshold]]
                results.append(entry)
            return results
        except Exception:
            print("[-] Failed analysis")
            exit(255)

    def validate_scan_results(scan_results):
        if type(scan_results) is not list:
            print("[-] Scan results is not a list")
            exit(254)
        for entry in scan_results:
            if type(entry) is not list:
                print("[-] Scan results entries not a list")
                exit(254)
            if len(entry) != 8:
                print("[-] Scan results entry count invalid")
                exit(254)
            for value in entry:
                if type(value) is not str:
                    print("[-] Scan results value not string")
                    exit(254)
        return ""
    