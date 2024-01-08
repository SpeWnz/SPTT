import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu
import requests
import sys
import threading
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# =========================================================================================================================

parser = argparse.ArgumentParser(description="Is The Domain Up? (itdu) v1")
REQUIRED_ARGUMENTS = parser.add_argument_group("Necessary arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"INPUT FILE"',type=str,required=True,help='Input file path (.txt)')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT FILE"',type=str,required=True,help='Output file path (.csv)')



# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('-t',metavar='"THREADS"',type=int,help="Thread count (default: single thread)")
OPTIONAL_ARGUMENTS.add_argument('-T',metavar='"TIMEOUT"',type=int,help="Timeout for target response (default: 5 seconds)")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)

# =========================================================================================================================

csvLines = ["DOMAIN; REACHABLE (http); REACHABLE (https)"]

def checkDomains(domainList: list):
    global csvLines

    

    for item in domainList:
        http = False
        https = False

        csvLine = item + ";"

        # http
        try:
            URL = "http://" + item
            requests.get(url=URL,verify=False,timeout=TIMEOUT_TIME)
            csvLine += "YES;"
            http = True
        except Exception as e:
            #print(e)
            csvLine += "NO;"
        

        # https
        try:
            URL = "https://" + item
            requests.get(url=URL,verify=False,timeout=TIMEOUT_TIME)
            csvLine += "YES"
            https = True
        except Exception as e:
            #print(e)
            csvLine += "NO"

        #input()

        LOCK.acquire()
        print("HTTPS:",https,"\r\t\tHTTP:",http,"\r\t\t\t\t",item)
        csvLines.append(csvLine)
        LOCK.release()

        

# =========================================================================================================================

LOCK = threading.Lock()
TIMEOUT_TIME = 5
THREAD_COUNT = 1

if "-t" in sys.argv:
    THREAD_COUNT = args.t

if "-T" in sys.argv:
    TIMEOUT_TIME = args.T
    

lines = fm.fileToSimpleList(args.i)

# thread initialization
threadList = []
sublists = lu.splitList(lines, THREAD_COUNT)
for i in range(0,THREAD_COUNT):
    argument = sublists[i]
    t = threading.Thread(target=checkDomains,args=(sublists[i],))
    threadList.append(t)


# starting threads
for thread in threadList:
    thread.start()


# waiting for each thread to finish
for thread in threadList:
    thread.join()



#csvLines = ["DOMAIN; REACHABLE (http); REACHABLE (https)"]

print("Job done, writing results to csv")
fm.listToFile(csvLines, args.o)