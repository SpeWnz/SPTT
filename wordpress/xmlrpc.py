import json
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import argparse
import sys
import requests
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# TO DO

__VERSION = "v130623 - TODO --- INCOMPLETE!!!"

parser = argparse.ArgumentParser(description="XMLRPC.php tester " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Needed arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"URL"',type=str,required=True,help='URL (without /xmlrpc.php')


# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)


# =========================================================================0

HEADERS = {
    "User-Agent":"User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept":"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}
URL = args.u + "/xmlrpc.php"

def listMethods():
    payload = "<methodCall><methodName>system.listMethods</methodName><params></params></methodCall>"
    r = requests.post(url=URL,headers=HEADERS,data=payload)
    print(r.content)


listMethods()