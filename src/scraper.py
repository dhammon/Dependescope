
import requests
from bs4 import BeautifulSoup
from sys import exit
import re
import validators


class Scraper:
    
    def check_snyk_advisor(registry, package_name):
        url = "https://snyk.io/advisor/" + registry + "/" + package_name
        response = requests.get(url)
        parsed_html = BeautifulSoup(response.content, 'html.parser')
        try:
            scoreBlob = parsed_html.body.find('div', attrs={'class':'number'})
            score = scoreBlob.get_text().replace("Package Health Score ","")
            score = score.replace(" / 100","")
            detail = parsed_html.body.find('ul', attrs={'class':'scores'})
            tag = detail.parent
            li_tag = tag.parent
            securityBlob = li_tag.findNext('li')
            popularityBlob = securityBlob.findNext('li')
            maintenanceBlob = popularityBlob.findNext('li')
            communityBlob = maintenanceBlob.findNext('li')
            security = securityBlob.contents[2].text
            popularity = popularityBlob.contents[2].text
            maintenance = maintenanceBlob.contents[2].text
            community = communityBlob.contents[2].text
            results = [registry, package_name, score, security, popularity, maintenance, community, url]
            Scraper.validate_snyk_results(results)
            return results
        except Exception:
            print("[-] Failed Check Snyk Advisor!")
            exit(255)
    
    def validate_snyk_results(results):
        allowed_strings = [
            "npm-package", "python", "no known security issues", "security issues found", "security review needed",
            "limited", "key ecosystem project", "influential project", "recognized", "small", "inactive", 
            "sustainable", "healthy", "active", "popular"
        ]
        if results[0].lower() not in allowed_strings:
            print("[-] Snyk Reponse - Registry invalid")
            exit(254)
        pattern = re.compile(r"^[A-Za-z0-9\-\_\.]{1,30}$")
        if not re.fullmatch(pattern, results[1]):
            print("[-] Snyk Response - Package invalid")
            exit(254)
        pattern = re.compile(r"^[0-9]{1,3}$")
        if not re.fullmatch(pattern, results[2]):
            print("[-] Snyk Response - Score invalid")
            exit(254)
        if results[3].lower() not in allowed_strings:
            print("[-] Snyk Response - Security invalid")
            exit(254)
        if results[4].lower() not in allowed_strings:
            print("[-] Snyk Response - Popularity invalid")
            exit(254)
        if results[5].lower() not in allowed_strings:
            print("[-] Snyk Response - Maintenance invalid")
            exit(254)
        if results[6].lower() not in allowed_strings:
            print("[-] Snyk Response - Community invalid")
            exit(254)
        if not validators.url(results[7]):
            print("[-] Snyk Response - Url invalid")
            exit(254)
        return ""