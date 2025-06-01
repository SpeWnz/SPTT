# core modules
import core.TextContentManager as TextContentManager
import core.ThreadManager as ThreadManager
import core.DatabaseManager as DatabaseManager

# zhor modules
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.timestampsUtils as tsu
import ZHOR_Modules.osUtils as osu

# standard modules
import shutil
import json
import traceback
import os
import sys
import argparse
import threading
import time
from datetime import timedelta

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


__VERSION = "18052025"

parser = argparse.ArgumentParser(description="Dump Digger - dig for sensitive info in a dump - v" + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Required Arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional Arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-f',metavar='"FOLDER"',type=str,required=True,help='Absolute path of the dump folder')
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"THREADS"',type=int,required=True,help='Number of threads')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT"',type=str,required=True,help='Output DB path')


# Argomenti opzionali
#OPTIONAL_ARGUMENTS.add_argument('-x',metavar='"VALORE OPZIONALE"',type=str,help="Descrizione del primo valore opzionale")
#OPTIONAL_ARGUMENTS.add_argument('--qualcosa',action="store_true",help="Descrizione del primo flag opzionale")
#OPTIONAL_ARGUMENTS.add_argument('--qualcosAltro',action="store_true",help="Descrizione del secondo flag opzionale")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")
OPTIONAL_ARGUMENTS.add_argument('--noperf',action="store_true",help="No performance")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)
PRINT_PERFORMANCE = not ('--noperf' in sys.argv)

# ====================================================================================================================================


# misurazione del progresso
PROGRESS_COUNTER = 0
PROGRESS_LOCK = threading.Lock()
TOTAL = 0

# stdout lock
STDOUT_LOCK = threading.Lock()


def typeHandler(files):
    IMG_EXT = ['gif', 'jpg', 'jpeg', 'png', 'tiff', 'tif'] # gestiti da tesseract

    IMG_LIST = [file for file in files if file.split('.')[-1].lower() in IMG_EXT]
    NON_IMG_LIST = [file for file in files if file.split('.')[-1].lower() not in IMG_EXT]

    return IMG_LIST, NON_IMG_LIST


def thread_targetFunction(filesSublist: list, threadID: int):
    global TOTAL
    global PROGRESS_COUNTER

    ThreadManager.threadMessage_info(threadID,"Thread avviato")

    for f in filesSublist:
        try:
            TextContentManager.analyzeFile(threadID,f)
        except:
            msg = "Eccezione in analyzeFile: {} - File: {}".format(traceback.format_exc(),f)
            ThreadManager.logu.logError(message=msg,fileName=ThreadManager.LOG_PATH)

        PROGRESS_LOCK.acquire()
        PROGRESS_COUNTER += 1
        PROGRESS_LOCK.release()


    ThreadManager.threadMessage_info(threadID,"Thread terminato")

def performanceThread_targetFunction():
    global TOTAL
    global PROGRESS_COUNTER

    sleepTime = 5

    # mostra l'andamento ogni tot secondi
    while True:

        PROGRESS_LOCK.acquire()
        percentage = str(int((PROGRESS_COUNTER / TOTAL) * 100))
        PROGRESS_LOCK.release()

        msg = "[PERFORMANCE STATUS] {} - {}% - {} / {}".format(tsu.getTimeStamp_iso8601(),percentage,PROGRESS_COUNTER,TOTAL)
        ThreadManager.logu.logInfo(message=msg,fileName=ThreadManager.LOG_PATH)

        # se hai finito, esci e interrompi il thread
        if PROGRESS_COUNTER >= TOTAL:                   # se per assurdo fosse maggiore di total
            return
        else:
            time.sleep(sleepTime)


# get "interesting files based on their extension"
def getInterestingFiles(dump_path: str):
    _dict = json.load(open('core/categories.json','r'))

    for key in _dict:
        # example
        # find /path/ -type f -iname "*.key"
        for extension in _dict[key]:
            com = ['find',dump_path, "-type", "f","-iname",f"*.{extension}"]
            #print(com)
            stdout, stderr = osu.commandResult(com)

            _files = stdout.split("\n")

            for item in _files:
                if len(item) > 0:
                    DatabaseManager.insert_interestingFile(item,key,extension)

# gets all the files in that dump folder using linux utils
def getFilesList(dump_path: str):
    com = ['find',dump_path, "-type", "f"]
    stdout, stderr = osu.commandResult(com)
    return stdout.split("\n")



# ====================================================================================================================================

if __name__ == '__main__':

    #filesList = fm.fileToSimpleList(args.f)
    #database = args.o
    dump_path = args.f
    DatabaseManager.DATABASE = args.o
    DatabaseManager.initializeTables()
    
    ThreadManager.logu.logInfo(message="Script avviato",fileName=ThreadManager.LOG_PATH)
    ThreadManager.logu.logInfo(message="Categorizzo file interessanti ...",fileName=ThreadManager.LOG_PATH)

    getInterestingFiles(dump_path)

    ThreadManager.logu.logInfo(message="Ottengo lista di tutti i file ...",fileName=ThreadManager.LOG_PATH)
    filesList = getFilesList(dump_path)

    msg = "Verranno analizzati {} file.".format(len(filesList))
    ThreadManager.logu.logInfo(message=msg,fileName=ThreadManager.LOG_PATH)


    

    # separa le immagini dal resto
    IMG_LIST, NON_IMG_LIST = typeHandler(filesList)

    TOTAL = len(IMG_LIST) + len(NON_IMG_LIST)

    # threads
    threadList = []

    # single threading: unisci le liste
    if args.t <= 1:
        ThreadManager.logu.logDebug(message="Avvio script in single thread.",fileName=ThreadManager.LOG_PATH)
        t = threading.Thread(target=thread_targetFunction,args=(IMG_LIST + NON_IMG_LIST, 1,))
        threadList.append(t)
    
    # multi threading
    else:
        
        ThreadManager.logu.logDebug(message="Avvio script con {} thread".format(str(args.t)),fileName=ThreadManager.LOG_PATH)

        # 1 solo thread che gestisce immagini
        t = threading.Thread(target=thread_targetFunction,args=(IMG_LIST, 1,))
        threadList.append(t)
        
        # gli altri thread gestistono il resto
        # dividere equamente i path che non sono immagini per poi spawnare un thread per ogni sublist
        SUB_NON_IMGS = lu.splitList(NON_IMG_LIST, args.t - 1)

        for i in range(0,args.t - 1):
            t = threading.Thread(target=thread_targetFunction,args=(SUB_NON_IMGS[i], i+2,))
            threadList.append(t)

    # avvio thread
    startTime = time.time()
    msg = "Avvio thread ({})".format(tsu.getTimeStamp_iso8601())
    ThreadManager.logu.logInfo(msg,fileName=ThreadManager.LOG_PATH)

    # avvio thread performance
    threadPerformance = threading.Thread(target=performanceThread_targetFunction)
    if PRINT_PERFORMANCE: 
        threadPerformance.start()

    for t in threadList:
        t.start()

    # attesa del termine dei lavori
    for t in threadList:
        t.join()


    ThreadManager.logu.logInfo(f"Inserting final results into db...",fileName=ThreadManager.LOG_PATH)
    DatabaseManager.insertMatches(TextContentManager.WORDLIST_MATCHES,TextContentManager.REGEX_MATCHES)


    endTime = time.time()
    totalTime = str(timedelta(seconds=int(endTime - startTime)))
    msg = "Operazione completata ({}). Tempo impiegato: {}".format(tsu.getTimeStamp_iso8601(),totalTime)


    if PRINT_PERFORMANCE:
        threadPerformance.join()    
    
    ThreadManager.logu.logInfo(msg,fileName=ThreadManager.LOG_PATH)