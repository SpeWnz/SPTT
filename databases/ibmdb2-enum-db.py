import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.osUtils as osu
import ZHOR_Modules.SPTT as SPTT

import argparse
import sys
import threading
import os
import time

import _common



parser = argparse.ArgumentParser(description="IBM DB2 database names enumeration - " + _common._VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")



# Required arguments
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET(s)"',type=str,required=True,help='Target IP/fqdn. Can either be a single target or a file')
REQUIRED_ARGUMENTS.add_argument('-d',metavar='"DATABASES',type=str,required=True,help='Wordlist of database names')
REQUIRED_ARGUMENTS.add_argument('-s',metavar='"SLEEP"',type=int,required=True,help='Sleep time between each request (in milliseconds)')
REQUIRED_ARGUMENTS.add_argument('-T',metavar='"THREADS"',type=int,required=True,help='Threads (corresponding to concurrent requests)')


# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('-q',action="store_true",help='"Quiet" mode: Skip the initial recap and the "press enter to continue" message')
OPTIONAL_ARGUMENTS.add_argument('--timeout',type=int,required=False,help='Connection attempt timeout (in milliseconds). By default is 1000ms')
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ========================================================================================================

TupleCacher   = SPTT.TupleCacher('cache/ibm-db2-enum-cache.db',tableName="databases", columnNames=['target','dbName'])


# function used by the threads
def threadWrapperFunction(threadID: int,triplets: list):
    
    # triplet structure
    # [target,databaseName]

    for triplet in triplets:
        
        if TupleCacher.tupleExists((triplet[0],triplet[1])):    
            msg = "[Thread #{}] Skipped cached tuple {} {}".format(str(threadID),triplet[0],triplet[1])
            np.debugPrint(msg,lock=_common.STDOUT_LOCK)
        else:
            msg = "[Thread #{}] Testing {} {}".format(str(threadID),triplet[0],triplet[1])
            np.debugPrint(msg,lock=_common.STDOUT_LOCK)
            
            #res = _common.attemptConnection(triplet[0],triplet[1],triplet[2])
            res = _common.enum_IBMDB2_database(triplet[0],triplet[1])

            if res == 1:
                TupleCacher.insertSuccess((triplet[0],triplet[1]))                

            if res == 0:
                TupleCacher.insertFail((triplet[0],triplet[1]))

            time.sleep(sleepTime)


if __name__ == '__main__':
 
    quiet = '-q' in sys.argv

    
    targets = []
    if os.path.isfile(args.t):
        targets = fm.fileToSimpleList(args.t)
    else:
        targets = [args.t]
    
    databaseNames = fm.fileToSimpleList(args.d)
    sleepTime = int(args.s) / 1000
    threadCount = args.T


    if '--timeout' in sys.argv:
        if args.timeout == 0:
            _common.CONNECTION_TIMEOUT = 0
        else:
            _common.CONNECTION_TIMEOUT = int(args.timeout) / 1000


    # organizing triplets
    triplets = lu.listsElementsPermutations([targets,databaseNames])
    threadList = []
    sublists = lu.splitList(triplets, threadCount)
    for i in range(0,threadCount):
        argument = sublists[i]
        t = threading.Thread(target=threadWrapperFunction,args=(i+1,sublists[i],))
        threadList.append(t)


    if not quiet:
        totalRequests = len(targets) * len(databaseNames)
        msg = "Testing {} targets with {} database names. Total requests: {}".format(
            str(len(targets)),
            str(len(databaseNames)),
            totalRequests
        )
        np.infoPrint(msg)
        osu.pressEnterToContinue()


    # starting threads
    np.debugPrint("Starting threads")
    for thread in threadList:
        thread.start()


    # waiting for each thread to finish
    for thread in threadList:
        thread.join()

    TupleCacher.dumpToDB()
    np.infoPrint("Job done. Check log for results")