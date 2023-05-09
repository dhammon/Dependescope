```
  _____                            _                                
 |  __ \                          | |                               
 | |  | | ___ _ __   ___ _ __   __| | ___  ___  ___ ___  _ __   ___ 
 | |  | |/ _ \ '_ \ / _ \ '_ \ / _` |/ _ \/ __|/ __/ _ \| '_ \ / _ \
 | |__| |  __/ |_) |  __/ | | | (_| |  __/\__ \ (_| (_) | |_) |  __/
 |_____/ \___| .__/ \___|_| |_|\__,_|\___||___/\___\___/| .__/ \___|
             | |                                        | |         
             |_|                                        |_|         
```

*The package health checker*

----
Are your projects' dependencies well maintained?  Do they have good community support?  How about their levels of popularity or security issues? Inspired by and built on top of Snyk Advisor, Dependescope scans repository packages health status and returns pass/fail results against threshold settings.  Scan your projects today and discovery if they meet your expectations for overall health!

Tool features include:
- Stand alone/CLI python file
- CI/CD pipeline friendly
- NPM (package.json) and PYPI (requirements.txt) support
- JSON or Standard output

# Installation
```
git clone https://github.com/dhammon/Dependescope
cd dependescope
pip3 install -r requirements.txt
```

# Usage and Examples
**Quick start**
```
python3 dependescope.py --package-file-path=/path/to/package.json
```

**Help Menu**
```
python3 dependescope.py --help --no-banner
usage: dependescope.py [-h] --package-file-path PACKAGE_FILE_PATH [--output-format OUTPUT_FORMAT] [--no-banner] [--score-threshold SCORE_THRESHOLD] [--security-threshold SECURITY_THRESHOLD]
                       [--popularity-threshold POPULARITY_THRESHOLD] [--maintenance-threshold MAINTENANCE_THRESHOLD] [--community-threshold COMMUNITY_THRESHOLD]

optional arguments:
  -h, --help            show this help message and exit
  --package-file-path PACKAGE_FILE_PATH
                        Path to package file. Example /path/to/package.json
  --output-format OUTPUT_FORMAT
                        Output format in JSON or STDOUT. Default STDOUT
  --no-banner           Do not display banner. Default False
  --score-threshold SCORE_THRESHOLD
                        Minimum passing overall score. Default 80
  --security-threshold SECURITY_THRESHOLD
                        Minimum passing security score. 0-2; 0=Security issues found, 1=Security review needed, 2=No known security issues. Default 0
  --popularity-threshold POPULARITY_THRESHOLD
                        Minimum passing popularity score. 0-5; 0=Limited, 1=Small, 2=Recognized, 3=Popular, 4=Influential project, 5=Key ecosystem project. Default 0
  --maintenance-threshold MAINTENANCE_THRESHOLD
                        Minimum passing maintenance score. 0-2; 0=Inactive, 1=Sustainable, 2=Healthy. Default 0
  --community-threshold COMMUNITY_THRESHOLD
                        Minimum passing community score. 0-2; 0=Limited, 1=Sustainable, 2=Active. Default 0
```

**Output results to JSON file**
```
python3 dependescope.py --package-file-path=/path/to/package.json --output-format=JSON --no-banner > results.txt
```

**Set Pass Thresholds**
```
python3 dependescope.py \
    --package-file-path=/path/to/package.json \
    --score-threshold=50 \
    --security-threshold=2 \
    --popularity-threshold=1 \
    --maintenance-threshold=1 \
    --community-threshold=1
```

**Example Results (standard output)**
```
python3 dependescope.py --no-banner --package-file-path=requirements.txt 
+--------+-------------+----------------+--------------------------+-----------------------+
| Result |   Category  |    Package     |         Measure          |       Threshold       |
+--------+-------------+----------------+--------------------------+-----------------------+
|  FAIL  |    score    | beautifulsoup4 |            72            |           80          |
|  PASS  |   security  | beautifulsoup4 | No known security issues | security issues found |
|  PASS  |  popularity | beautifulsoup4 |   Influential project    |        limited        |
|  PASS  | maintenance | beautifulsoup4 |         Healthy          |        inactive       |
|  PASS  |  community  | beautifulsoup4 |         Limited          |        limited        |
|  PASS  |    score    |  prettytable   |            97            |           80          |
|  PASS  |   security  |  prettytable   | No known security issues | security issues found |
|  PASS  |  popularity |  prettytable   |  Key ecosystem project   |        limited        |
|  PASS  | maintenance |  prettytable   |         Healthy          |        inactive       |
|  PASS  |  community  |  prettytable   |          Active          |        limited        |
|  PASS  |    score    |    requests    |            97            |           80          |
|  PASS  |   security  |    requests    | No known security issues | security issues found |
|  PASS  |  popularity |    requests    |  Key ecosystem project   |        limited        |
|  PASS  | maintenance |    requests    |         Healthy          |        inactive       |
|  PASS  |  community  |    requests    |          Active          |        limited        |
|  PASS  |    score    |   validators   |            85            |           80          |
|  PASS  |   security  |   validators   | No known security issues | security issues found |
|  PASS  |  popularity |   validators   |  Key ecosystem project   |        limited        |
|  PASS  | maintenance |   validators   |       Sustainable        |        inactive       |
|  PASS  |  community  |   validators   |       Sustainable        |        limited        |
+--------+-------------+----------------+--------------------------+-----------------------+
```

# Wiki

**Registries Supported**
- npm = npm-package
- PiPY = python

**Thresholds Measures**
| Measure | Default | Accepted Values | Description |
| --- | --- | --- | --- |
| Score | 80 | 0-100 | Package health score out of 100 maximum |
| Security | 0 | 0-2 | 0=No Known Security Issues, 1=Security Issues Found, 2=Security Review Needed |
| Popularity | 0 | 0-5 | 0=Limited, 1=Small, 2=Recognized, 3=Popular, 4=Influential project, 5=Key ecosystem project |
| Maintenance | 0 | 0-2 | 0=Inactive, 1=Sustainable, 2=Healthy |
| Community | 0 | 0-2 | 0=Limited, 1=Sustainable, 2=Active |


**Exit Codes**
- 0 = No tests failed
- 1 = Tests failed
- 254 = Validation Error
- 255 = App Error

# Testing Notes
- `python3 tests/test_client.py TestClient.test_run_happy` 
- `python3 -m unittest discover tests/`
- `python3 -m debugpy --listen 5678 --wait-for-client tests/test_accounts.py TestAccounts.test_displayMessage` -> then Run Debug Attach
- `alias debug="python3 -m debugpy --listen 5678 --wait-for-client"`
- `export PYTHONPATH=$(pwd)`

## Credits
Snyk Advisor - https://snyk.io/advisor/

# TO-DO
- ignores
- yarn support
- go support
- Github Action example