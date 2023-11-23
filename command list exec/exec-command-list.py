import threading
import sys
import os
import json

import ZHOR_Modules.terminalUtils as tu
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.argparseUtils as apu
from ZHOR_Modules.csvUtils import getTimeStamp

import argparse


__VERSION = "v161123"

parser = argparse.ArgumentParser(description="Exec Command List " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"INPUT"',type=str,required=True,help='Input json file containing the commands')
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"THREADS"',type=str,required=True,help='Threads')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('-o',metavar='"OUTPUT FOLDER"',type=str,help='Path of the folder to store the output. By default it is called "commands_\{timestamp\}" (MUTEX with --noOut)')
OPTIONAL_ARGUMENTS.add_argument('--noOut',action="store_true",help="Do not save stdout in the files (MUTEX with --err2out and -o)")
OPTIONAL_ARGUMENTS.add_argument('--err2out',action="store_true",help="Also redirect stderr to stdout (MUTEX with --noOut)")
OPTIONAL_ARGUMENTS.add_argument('--reset',action="store_true",help="Reset the json file before starting the jobs")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()
np.DEBUG = ('--debug' in sys.argv)


# mutex args
if (apu.checkMutExArgs(sys.argv,['--noOut','-o']) is True):
    exit()

if (apu.checkMutExArgs(sys.argv,['--noOut','--err2out']) is True):
    exit()


# locks
STDOUT_LOCK = threading.Lock()
PROGRESS_LOCK = threading.Lock()

# output folders
OUTPUT_FOLDER = "commands_" + getTimeStamp()
if "-o" in sys.argv:
    OUTPUT_FOLDER = args.o

# progress tracking
#PROGRESS = 0
#TOTAL = 0

# stdout
ERR2OUT = False
if '--err2out' in sys.argv:
    ERR2OUT = True

NO_OUT = False
if '--noOut' in sys.argv:
    NO_OUT = True

# reset
RESET = False
if '--reset' in sys.argv:
    RESET = True

# ================================================================================================================
class _jsonFileManager():
    def __init__(self):
        pass
    
    SAVE_FILE_DICTIONARY = {}           # where the info is stored in memory
    SAVE_FILE_PATH = None               # where the info is stored on disk
    DICT_LENGTH = None                  

    FILE_LOCK = threading.Lock()        # lock used for file save and load
    DICT_LOCK = threading.Lock()        # lock used for dictionary

    __fake_save_dict = {
        1:{"command":"blablabla","state":"wip"},
        2:{"command":"blablabla","state":"done"},
        3:{"command":"blablabla","state":"todo"},
    }

    # returns true if there are commands to execute, false otherwise
    # used by threads to know when to quit
    def jobAvailable(self):
        self.DICT_LOCK.acquire()
        
        for key in self.SAVE_FILE_DICTIONARY:
            if self.SAVE_FILE_DICTIONARY[key]['state'] == 'todo':

                # theres work to do
                self.DICT_LOCK.release()
                return True
            
        # theres no work to do
        self.DICT_LOCK.release()
        return False

    # returns how many "todo" are left (used for progress %)
    def getTodoAmount(self,autoLock=True):
        amount = 0
        if autoLock:
            self.DICT_LOCK.acquire()
        
        for key in self.SAVE_FILE_DICTIONARY:
            if self.SAVE_FILE_DICTIONARY[key]['state'] == 'todo':

                amount += 1
            
        # theres no work to do
        if autoLock:
            self.DICT_LOCK.release()
        return amount
    

    # returns how many "done" are left (used for progress %)
    def getDoneAmount(self,autoLock=True):
        amount = 0
        if autoLock:
            self.DICT_LOCK.acquire()
        
        for key in self.SAVE_FILE_DICTIONARY:
            if self.SAVE_FILE_DICTIONARY[key]['state'] == 'done':

                amount += 1
            
        # theres no work to do
        if autoLock:
            self.DICT_LOCK.release()
        return amount
        

    # sets a state knowing the command id
    def setCommandState(self,commandID: int,state: str,autoLock=True):
        
        if autoLock:
            self.DICT_LOCK.acquire()

        np.debugPrint("Setting command {} as {}".format(str(commandID),state))
        self.SAVE_FILE_DICTIONARY[commandID]['state'] = state
        
        if autoLock:
            self.DICT_LOCK.release()

    # returns the total amount of jobs in the dictionary
    def getTotalAmount(self):
        if self.DICT_LENGTH == None:
            self.DICT_LENGTH = len(self.SAVE_FILE_DICTIONARY)
        
        return self.DICT_LENGTH

    # returns an undone command and sets it as wip
    def getTodoCommand(self):
        self.DICT_LOCK.acquire()
        
        for key in self.SAVE_FILE_DICTIONARY:
            #print(self.SAVE_FILE_DICTIONARY)
            if self.SAVE_FILE_DICTIONARY[key]['state'] == 'todo':

                com, comID = self.SAVE_FILE_DICTIONARY[key]['command'], key
                self.setCommandState(key,'wip',autoLock=False)
                self.saveFile(autoLock=False)
                self.DICT_LOCK.release()
                return com, comID

        # no job available
        com, comID = None, None
        self.DICT_LOCK.release()
        return com, comID

    # gets % of work done
    def getPercenteageCompletion(self):
        self.DICT_LOCK.acquire()

        perc = int((self.getDoneAmount(autoLock=False) / self.DICT_LENGTH) * 100)

        self.DICT_LOCK.release()
        return perc

    # load from file to in-memory json dict object
    def loadFile(self):

        np.debugPrint("Loading json save file",lock=STDOUT_LOCK)
        self.FILE_LOCK.acquire()

        with open(self.SAVE_FILE_PATH,'r') as f:
            self.SAVE_FILE_DICTIONARY = json.load(f)

        self.FILE_LOCK.release()

    # save from json dict object to file
    def saveFile(self, autoLock=True):
        np.debugPrint("Saving json save file",lock=STDOUT_LOCK)
        
        if autoLock:
            self.FILE_LOCK.acquire()

        with open(self.SAVE_FILE_PATH,'w') as f:
            json.dump(self.SAVE_FILE_DICTIONARY,f)

        if autoLock:
            self.FILE_LOCK.release()

    # (NO LOCKS) used at the beginning of the script
    def resetWIP(self):
        np.debugPrint("Resetting WIP",lock=STDOUT_LOCK)
        for key in self.SAVE_FILE_DICTIONARY:
            if self.SAVE_FILE_DICTIONARY[key]['state'] == 'wip':
                self.SAVE_FILE_DICTIONARY[key]['state'] = 'todo'


    # (NO LOCKS) used at the beginning of the script
    def resetALL(self):
        np.debugPrint("Resetting ALL",lock=STDOUT_LOCK)
        for key in self.SAVE_FILE_DICTIONARY:
                self.SAVE_FILE_DICTIONARY[key]['state'] = 'todo'
    
jsonFileManager = _jsonFileManager()

# ================================================================================================================


# target function executed by threads
# for each command, launch an xterm window and log the result with tee
def threadTargetFunction(threadID: int):
    global PROGRESS
    global TOTAL
    
    while True:
                
        command , comIndex = jsonFileManager.getTodoCommand()
        if command == None:
            np.infoPrint("[Thread #{}] Thread job done.".format(str(threadID),lock=STDOUT_LOCK))
            return
        
        # should we grab output with Tee?
        if NO_OUT == False:
            
            # should Tee also grab stderr?
            if ERR2OUT == True:
                command += " 2>&1 | tee {}/command-{}.txt".format(OUTPUT_FOLDER,str(comIndex))
            else:
                command += " | tee {}/command-{}.txt".format(OUTPUT_FOLDER,str(comIndex))


        perc = jsonFileManager.getPercenteageCompletion()
        np.infoPrint("[{}%] [Thread #{}] Executing command #{}".format(str(perc),str(threadID),comIndex),lock=STDOUT_LOCK)
        np.debugPrint("[Thread #{}] Command id:{} --- Command: {}".format(str(threadID),comIndex,command),lock=STDOUT_LOCK)

        #np.infoPrint("[Thread #{}] Executing command #{}".format(str(threadID),comIndex),lock=STDOUT_LOCK)
        tu.spawn_xterm_b64(
            command=command,
            windowTitle="Thread #{} - Command #{}".format(str(threadID),str(comIndex)),
            executeInBackground=False
            )
        
        # update current progress
        jsonFileManager.setCommandState(comIndex,'done')
        jsonFileManager.saveFile()

        #PROGRESS_LOCK.acquire()
        #PROGRESS += 1        
        #PROGRESS_LOCK.release()
        

# converts the raw command list into an indexed command list
def commandList2indexedCommandList(commandList: list):
    out = []

    for i in range(0,len(commandList)):
        t = (i+1,commandList[i])
        out.append(t)

    return out

        
        
if __name__ == '__main__':

    jsonFileManager.SAVE_FILE_PATH = args.i
    jsonFileManager.loadFile()

    # is there actually work to do?
    if jsonFileManager.jobAvailable():
        pass
    else:
        np.infoPrint("No work left for this json file.")
        exit()

    if NO_OUT == False:         
        os.system('mkdir ' + OUTPUT_FOLDER)

    if RESET:
        jsonFileManager.resetALL()
    else:
        jsonFileManager.resetWIP()

    PROGRESS = jsonFileManager.getTodoAmount()
    TOTAL = jsonFileManager.getTotalAmount()

    threadCount = int(args.t)

    threadList = []

    for i in range(0,threadCount):
        t = threading.Thread(target=threadTargetFunction,args=(i+1,))
        threadList.append(t)

    for t in threadList:
        t.start()

    for t in threadList:
        t.join()


    np.infoPrint("Job completed. All commands have been executed.")
