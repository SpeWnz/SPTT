import sqlite3
import os
import re
import ZHOR_Modules.osUtils as osu
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.osUtils as osu
import textract
import pandas as pd
import openpyxl

import core.ThreadManager as ThreadManager
import core.DatabaseManager as DatabaseManager

# nostre regex
from core.regexes import regexes as REGEXES

# nostra wordlist
WORDLIST = fm.fileToSimpleList('wordlist.txt')

MATCHES_LENGTH_LIMIT    = 1000
REGEX_MATCHES           = []
WORDLIST_MATCHES        = []

TEXTRACT_SUPPORTED_EXTENSIONS = ["csv","doc","docx","eml","epub","gif","jpg","jpeg","json","html","htm","mp3","msg","odt","ogg","pdf","png","pptx","ps","rtf","tiff","tif","txt","wav","xlsx","xls"]

np.DEBUG = True




# ottiene estensione da un path
def getExtension(threadID: int, path: str):
    ThreadManager.threadMessage_debug(threadID,"Ottengo estensione per il file " + path)
    _, extension = os.path.splitext(path)
    ThreadManager.threadMessage_debug(threadID,"Estensione ottenuta per  " + path)

    return extension

# (caso speciale) gestisci excel a parte con openpyxl per prevenire l'eccezione
def parseTextFromExcel(threadID: int, path: str,extension:str):
    
    ThreadManager.threadMessage_debug(threadID,"Estraggo testo da " + path)

    dict_of_dataframes = None
    
    # xlsx
    if 'xlsx' in extension:
        dict_of_dataframes = pd.read_excel(path,engine='openpyxl',sheet_name=None)
    # xls
    else:
        dict_of_dataframes = pd.read_excel(path,sheet_name=None)


    content = ""

    for key in dict_of_dataframes:
        content += str(dict_of_dataframes[key]) + "\n"        
        #input("ENTER TO CONTINUE")

    return content


def parseTextFromFile(threadID: int,path: str):

    text = None    

    # (caso speciale) gestisci excel a parte per prevenire l'eccezione
    ext = getExtension(threadID,path)
    
    if 'xls' in ext or 'xlsx' in ext:
        text = parseTextFromExcel(threadID,path,ext)
        return text
    
    # l'estensione ricade in una delle supportate?
    if ext[1:] in TEXTRACT_SUPPORTED_EXTENSIONS:    

        ThreadManager.threadMessage_debug(threadID,"Estraggo testo da " + path)
        text = textract.process(path).decode('utf-8')
        #print(text)
    else:
        ThreadManager.threadMessage_debug(threadID,"Nessun estensione supportata. Leggo con in maniera grezza con strings " + path)
        _stdout, _stderr = osu.commandResult(["strings",path])
        text = _stdout
    
    
    return text

# match con parole dalla wordlist
# restituisce una lista contenente ogni parola (nella wordlist) che si trova nel file
# esempio:
# file1.txt contiene ["password","hash","passwd"]
def getWordsMatches(threadID: int, textContent: str,path: str):
    ThreadManager.threadMessage_debug(threadID,"Controllo match in wordlist per il file " + path)
    
    outputMatches = []

    for word in WORDLIST:
        if word in textContent:
            outputMatches.append(word)

    return outputMatches



# match con regex
# restituisce una lista di tuple in cui ogni tupla contiene il tipo di regex trovata nel file e il suo valore.
# esempio:
# file1.txt contiene: [("Kubernetes Token","abcdef.123123123"),("Google Oauth","asdasdasd.213123123")]
def getRegexMatches(threadID: int, textContent: str, path: str):
    ThreadManager.threadMessage_debug(threadID,"Controllo match in regex per il file " + path)
    outputMatches = []
    
    for key in REGEXES:
        matches = re.findall(REGEXES[key],textContent)
        if len(matches) > 0:

            for m in matches:

                if len(m) > 0:
                    _resultTuple = (key,m)
                    outputMatches.append(_resultTuple)

    return outputMatches

# crea il csv di output se non esiste
def checkCSVExists():
    global OUTPUT_CSV_NAME
    global USE_CSV_HEADERS
    
    if (os.path.exists(OUTPUT_CSV_NAME)):
        USE_CSV_HEADERS = False
        return
    
    USE_CSV_HEADERS = True
    return



# prende in input il path del file e fa le analisi
# return true ---> almeno 1 risultato
# return false ---> nessun risultato
def analyzeFile(threadID: str, path: str):
    global WORDLIST_MATCHES
    global REGEX_MATCHES
    
    ThreadManager.threadMessage_debug(threadID,"Sto analizzando il file " + path)
    
    try:
        content = parseTextFromFile(threadID,path)
    except textract.exceptions.ExtensionNotSupported:
        ThreadManager.threadMessage_error(threadID,"Eccezione: estensione non supportata da textract. File:" + path)
        return


    totalMatchesCount = 0

    # get results
    wm = getWordsMatches(threadID,content,path)
    rm = getRegexMatches(threadID,content,path)

    # remove duplicates
    wm = lu.removeDuplicates(wm)
    rm = lu.removeDuplicates(rm)

    if len(wm) > 0:
        totalMatchesCount += len(wm)

    if len(rm) > 0:
        totalMatchesCount += len(rm)

    
    ThreadManager.threadMessage_debug(threadID,"Analisi completata per il file " + path)
    if totalMatchesCount >= 1:
        extension = getExtension(threadID, path)

        # INSERIMENTO RISULTATI 
        ThreadManager.GLOBAL_MATCHES_LOCK.acquire()
        ThreadManager.threadMessage_debug(threadID,"Aggiungo risultati alle liste globali")
        WORDLIST_MATCHES.append((path,extension,wm))
        REGEX_MATCHES.append((path,extension,rm))

        ThreadManager.threadMessage_debug(threadID,f"Global lists length = {len(WORDLIST_MATCHES)} {len(REGEX_MATCHES)}")

        ThreadManager.GLOBAL_MATCHES_LOCK.release() 

        # dump to db if necessary
        if (len(WORDLIST_MATCHES) >= MATCHES_LENGTH_LIMIT) or (len(REGEX_MATCHES) >= MATCHES_LENGTH_LIMIT):
            ThreadManager.GLOBAL_MATCHES_LOCK.acquire()

            ThreadManager.threadMessage_info(threadID,"In-memory lists are full. Dumping to db...")

            DatabaseManager.insertMatches(WORDLIST_MATCHES,REGEX_MATCHES)

            WORDLIST_MATCHES = []
            REGEX_MATCHES = []

            ThreadManager.threadMessage_info(threadID,f"Dumped. Lists are now empty.")

            ThreadManager.GLOBAL_MATCHES_LOCK.release()

        return
    else:
        ThreadManager.threadMessage_debug(threadID,"Non ci sono risultati per il file " + path)
        return


