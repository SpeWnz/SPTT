# INPUT: List of CVE IDs
# OUTPUT: CSV file containing information about the specified CVEs, taken from the Nist website

import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
from bs4 import BeautifulSoup
import requests
import sys
import os
import time
import argparse

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# ===========================================================================================================================

parser = argparse.ArgumentParser(description="CVE2CSV - Converts a list of CVEs to a nice CSV file (v140923)")
REQUIRED_ARGUMENTS = parser.add_argument_group("Necessary arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"INPUT"',type=str,required=True,help='Input file containing the CVE IDs')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT"',type=str,required=True,help='Output file name (with .csv)')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)

# ===========================================================================================================================

fileLines = fm.fileToSimpleList(args.i)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
SLEEP_TIME = 0.5



# gets data from nist and parses the html page
def getData(cveID: str):
    URL = "https://nvd.nist.gov/vuln/detail/" + cveID
    HEADERS = {
        'User-Agent':USER_AGENT
    }
    r = requests.get(url=URL,headers=HEADERS,verify=False)

    soup = BeautifulSoup(r.text,'lxml')

    # default values
    severityValues_3 = ["N/A","N/A"]
    vector_3 = "N/A"
    severityValues_2 = ["N/A","N/A"]
    vector_2 = "N/A"

    #CVSS 3
    try:
        severity_3 = soup.find('a',{'id':'Cvss3NistCalculatorAnchor'}).text
        vector_3 = soup.find('span',{'class':'tooltipCvss3NistMetrics'}).text
        severityValues_3 = severity_3.split(' ')
    except:
        np.debugPrint("No values for CVSS3")

    #CVSS 2
    try:
        severity_2 = soup.find('a',{'id':'Cvss2CalculatorAnchor'}).text
        vector_2 = soup.find('span',{'class':'tooltipCvss2NistMetrics'}).text
        severityValues_2 = severity_2.split(' ')
    except:
        np.debugPrint("No values for CVSS2")


    return severityValues_3,vector_3,severityValues_2,vector_2



csvHeader = '"{}";"{}";"{}";"{}";"{}";"{}";"{}"'.format(
    "CVE ID",
    "CVSS3.x Value","CVSS3.x Label","CVSS3.x Vector",
    "CVSS2 Value","CVSS2 Label","CVSS2 Vector"
    )
csvLines = [csvHeader]

for line in fileLines:
    np.infoPrint("Getting info for " + line)
    sev3val,sev3vec,sev2val,sev2vec = getData(line)

    csvLine = '"{}";"{}";"{}";"{}";"{}";"{}";"{}"'.format(
        line,
        sev3val[0],sev3val[1],sev3vec,
        sev2val[0],sev2val[1],sev2vec
        )

    csvLines.append(csvLine)
    time.sleep(SLEEP_TIME)



fm.listToFile(csvLines,args.o,mode='w')