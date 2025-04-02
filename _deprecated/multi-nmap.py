import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.terminalUtils as tu
import ZHOR_Modules.fileManager as fm
import sys
import json
import os
import threading
import argparse


__VERSION = "v120623"

parser = argparse.ArgumentParser(description="Multi NMAP " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Argomenti necessari")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Argomenti opzionali")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"IP LIST"',type=str,required=True,help='Input IP list')
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"THREADS"',type=int,required=True,help='Threads (concurrent nmap scans)')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT FOLDER"',type=str,required=True,help='Path of the output folder')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)

# =================================================================================================================

LOCK = threading.Lock()
OUTPUT_FOLDER_PATH = str(args.o)
threadCount = int(args.t)
targetsList = fm.fileToSimpleList(str(args.i))
targetsCount = len(targetsList)
PROGRESS_COUNTER = 0


def threadWrapper(targetIP_sublist,threadID):
    global PROGRESS_COUNTER
    LOCK.acquire()
    np.infoPrint("[Thread #{}] Thread started".format(str(threadID)))
    LOCK.release()


    for ip in targetIP_sublist:
        nmapScan(ip, threadID)

        LOCK.acquire()
        PROGRESS_COUNTER += 1
        percenteage = int((PROGRESS_COUNTER/targetsCount) * 100)
        np.infoPrint("Progress: {} / {} --- {}%".format(PROGRESS_COUNTER,targetsCount,str(percenteage)))
        LOCK.release()

    LOCK.acquire()
    np.infoPrint("[Thread #{}] Thread's job done".format(str(threadID)))
    LOCK.release()



def nmapScan(targetIP,threadID):
    LOCK.acquire()
    np.infoPrint("[Thread #{}] [Target IP: {}] Scan started".format(str(threadID),str(targetIP)))
    LOCK.release()

    com = "nmap -Pn -p80,443,7001,8880,8081,9080,9090,9081,1080-1100,4443,5443,6443,7443,8443,9000,9443,10443,10000,10080,2181,3000,5000,5432,5701,7742,8093,8180,8301,8302,8300,8400,8500,8600,8761,9000,9001,9042,9060,21,22,23,53,123,139,135,179,445,88,389,636,4500,3389,5985,5986,18264,2000,5060,3306,1433,1521,5432,1434,2484,1723,1194 -sV {} -oN {}/{}_.txt".format(targetIP,OUTPUT_FOLDER_PATH,targetIP)

    LOCK.acquire()
    np.debugPrint("[Thread #{}] [Target IP: {}] Command: {}".format(str(threadID),str(targetIP),com))
    LOCK.release()

    tu.spawn_xterm(com, "NMAP ISTANCE #{} --- IP: {}".format(str(threadID),str(targetIP)),None,False)


    LOCK.acquire()
    np.infoPrint("[Thread #{}] [Target IP: {}] Scan completed".format(str(threadID),str(targetIP)))
    LOCK.release()



# split lists
sublists = lu.splitList(targetsList, threadCount)

threadList = []
for i in range(0,len(sublists)):
    t = threading.Thread(target=threadWrapper,args=(sublists[i],i+1))
    threadList.append(t)


# avvio thread
for t in threadList:
    t.start()


# attesa thread
for t in threadList:
    t.join()


np.infoPrint("All scans completed.")