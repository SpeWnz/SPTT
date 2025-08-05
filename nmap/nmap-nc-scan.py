'''
A "presumably" quicker port scanner that leverages netcat under the hood.
'''

import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.osUtils as osu
import ZHOR_Modules.logUtils as logu
import ZHOR_Modules.progressBar as prog
import time
import argparse
import threading
import os
import sys

parser = argparse.ArgumentParser(description="NMAP NC SCAN - A quicker and lighter port scanner")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET(s)"',type=str,required=True,help='Target or list of targets')
REQUIRED_ARGUMENTS.add_argument('-T',metavar='"THREADS"',type=int,required=True,help='Threads (i.e. parallel requests)')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT"',type=str,required=True,help='Output path')

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('--proxychains',action="store_true",help="Prepend proxychains")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ============================================================================

USE_PROXYCHAINS = '--proxychains' in sys.argv
LOG_LOCK        = threading.Lock()
STDOUT_LOCK     = threading.Lock()
LOG_PATH        = args.o

# stuff used to track progress
PROGRESS_LOCK   = threading.Lock()
PROGRESS        = 0
TOTAL           = None
JOB_DONE        = False


def portOpen(target: str, port: int):
    com = []

    if USE_PROXYCHAINS:
        com += ['sudo','proxychains']

    com += ['nc',target,str(port),'-vvv','-z','-w','1']
    stdout, stderr = osu.commandResult(com)

    np.debugPrint(f'COM = {lu.concatenate_elements(com,' ')}',STDOUT_LOCK)

    # the result of the scan is in the stderr, not stdout (for some odd reason)
    if 'open' in stderr:
        return True
    else:
        return False
    

def threadFunction(sublist: list):
    global PROGRESS
    global PROGRESS_LOCK

    for item in sublist:
        target = item[0]
        port = item[1]

        if portOpen(target,port):
            msg = f'{target} \t\t{port}'
            logu.logInfo(msg,lock=LOG_LOCK,stdout=False,fileName=LOG_PATH)
            np.infoPrint(msg,lock=STDOUT_LOCK)

        PROGRESS_LOCK.acquire()
        PROGRESS += 1
        PROGRESS_LOCK.release()  
        

def status():

    global PROGRESS
    global PROGRESS_LOCK
    

    while JOB_DONE == False:

        PROGRESS_LOCK.acquire()
        msg = f'PROGRESS: {PROGRESS} / {TOTAL} ({prog.ratioToPercentage(PROGRESS,TOTAL)}%)'
        PROGRESS_LOCK.release()

        np.infoPrint(msg,lock=STDOUT_LOCK)

        time.sleep(5)
        
    



if __name__ == '__main__':

    
    # proxychains requires root
    if USE_PROXYCHAINS:
        if os.getuid() != 0:
            np.errorPrint("Proxychains requires sudo privileges.")
            exit()
    
    
    targets = None

    if os.path.isfile(args.t):
        targets = fm.fileToSimpleList(args.t)
    else:
        targets = [args.t]

    ports = [x for x in range(1,65536)]
    tuples = lu.listsElementsPermutations([targets,ports])
    TOTAL = len(tuples)


    # progress thread
    progressThread = threading.Thread(target=status)
    progressThread.start()

    # threads
    sublists = lu.splitList(tuples,args.T)
    threadList = []
    for i in range(0,args.T):
        t = threading.Thread(target=threadFunction,args=(sublists[i],))
        threadList.append(t)

    for t in threadList:
        t.start()

    for t in threadList:
        t.join()

    JOB_DONE = True
    np.infoPrint("Job Done",STDOUT_LOCK)