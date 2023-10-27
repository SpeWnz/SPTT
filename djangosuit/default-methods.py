# testing for default djangosuit api methods

import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.requestUtils as requ
import ZHOR_Modules.cookiesUtils as cookieUt
import sys
import requests
import argparse

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


__VERSION = "v210723"

parser = argparse.ArgumentParser(description="DjangoSuit default methods scanner " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Argomenti necessari")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Argomenti opzionali")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"BASE URL"',type=str,required=True,help='Base target url WITHOUT ending slash. Example https://testtarget.com')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('-c',metavar='"COOKIES"',type=str,help='Cookie string')
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)


# User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
}

methods = fm.fileToSimpleList('djangosuit-methods.txt')
URL = args.u
COOKIES = None
if ("-c" in sys.argv):
    COOKIES = cookieUt.cookieStringToDict(args.c)




#determine largest string for printing nicely
maxLen = len(max(methods,key=len))
print(maxLen)

spacer = ' ' * (maxLen + len(URL)) + '     '

np.infoPrint("Scannin methods. Format:\nMethod --- get post put options")
for m in methods:
    outmsg = ""
    
    u = URL + m

    r = requests.get(url=u,headers=HEADERS,verify=False)
    outmsg += str(r.status_code) + ' '

    r = requests.post(url=u,headers=HEADERS,verify=False)
    outmsg += str(r.status_code) + ' '

    r = requests.put(url=u,headers=HEADERS,verify=False)
    outmsg += str(r.status_code) + ' '

    r = requests.options(url=u,headers=HEADERS,verify=False)
    outmsg += str(r.status_code) + ' '

    print(spacer,outmsg,'\r',u)