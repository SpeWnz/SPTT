import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import argparse
import sys
import requests
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/spring-actuators
__VERSION = "v1 (170223)"

parser = argparse.ArgumentParser(description="Spring Boot Actuators Tester " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Argomenti necessari")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Argomenti opzionali")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"URL"',type=str,required=True,help='URL / TARGET IP')


# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)

# =======================================================================================================0

actuators = fm.fileToSimpleList('actuators-list.txt')

separator = '=' * os.get_terminal_size()[0]


for a in actuators:
    print(separator)

    URL = args.u + a
    np.debugPrint(URL)

    r = requests.get(url=URL,verify=False)
    np.infoPrint("Results for GET " + a)
    print("\nStatus code: ",r.status_code)
    print("\n\n",r.content)

    r = requests.post(url=URL,verify=False)
    np.infoPrint("Results for POST " + a)
    print("\nStatus code: ",r.status_code)
    print("\n\n",r.content)

    r = requests.put(url=URL,verify=False)
    np.infoPrint("Results for PUT " + a)
    print("\nStatus code: ",r.status_code)
    print("\n\n",r.content)

    r = requests.delete(url=URL,verify=False)
    np.infoPrint("Results for DELETE " + a)
    print("\nStatus code: ",r.status_code)
    print("\n\n",r.content)

    r = requests.delete(url=URL,verify=False)
    np.infoPrint("Results for OPTIONS " + a)
    print("\nStatus code: ",r.status_code)
    print("\n\n",r.content)