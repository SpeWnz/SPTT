import json
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import argparse
import sys

__VERSION = "v1 (150223)"

parser = argparse.ArgumentParser(description="Har extractor " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Needed arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"INPUT"',type=str,required=True,help='Input ".har" file')


# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('-u',metavar='"URL"',type=str,help="Finds results for that specific url/domain only.") #cerca quelle response la cui request viene solo da quell'url
OPTIONAL_ARGUMENTS.add_argument('-b',metavar='"BLACKLIST FILE"',type=str,help="Specify a file with unwanted text, to exlude results.")
OPTIONAL_ARGUMENTS.add_argument('--headers',action="store_true",help="Gets results for headers instead of resource paths.")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = not ("--debug" in sys.argv)

# ==========================================================================================================================

filePath = args.i
jsonObj = json.load(open(filePath,'r'))


# restituisce una lista contenente tutti gli url di tutte le risorse (tutti gli href e tutti gli src, ecc..)
def getResources(inputJsonObj,url=None):
    
    
    entries = jsonObj['log']['entries']
    outputList = []
    for e in entries:

        if (url is None):
            outputList.append(e['request']['url'])
        else:
            if(url in e['request']['url']):
                outputList.append(e['request']['url'])

    return outputList



def getResources_v2(inputJsonObj,url=None):
    
    if url is None:
        url = ""

    entries = jsonObj['log']['entries']
    outputList = []
    for e in entries:

        #print(url,"in",e['request']['url'], (url in e['request']['url']))
        if(url in e['request']['url']):
                outputList.append("[CONN #" + str(e['connection']) + "]   " + e['request']['url'])
            

    return outputList


def getResponseHeaders(inputJsonObj,url=None):
    entries = jsonObj['log']['entries']
    outputList = []
    for e in entries:

        if (url is None):
            for h in e['response']['headers']:
                outputList.append(h['name'] + ";" + h['value'])

        else:
            if(url in e['request']['url']):
                for h in e['response']['headers']:
                    outputList.append(h['name'] + ";" + h['value'])

    return outputList

def getResponseHeaders_v2(inputJsonObj,url=None):
    
    if url is None:
        url = ""

    entries = jsonObj['log']['entries']
    outputList = []
    for e in entries:
        
        if(url in e['request']['url']):
            for h in e['response']['headers']:
                outputList.append("[CONN #" + str(e['connection']) + "]   " + h['name'] + ";" + h['value'])

    return outputList


# rimuove tutto i testo specificato nella blacklist
def removeBlacklistedText(blackListFilePath: str, inputList: list):
    
    def containsBlackListItem(_item: str,_blacklist: list):
        for b in _blacklist:
            if b in item:
                return True

        return False


    blacklist = fm.fileToSimpleList(blackListFilePath)    
    outputList = []

    for item in inputList:
        if not containsBlackListItem(item, blacklist):
            outputList.append(item)
            


    return outputList

    
# header mode
if ("--headers" in sys.argv):
    L = lu.removeDuplicates(getResponseHeaders_v2(jsonObj,args.u))
else:
    L = lu.removeDuplicates(getResources_v2(jsonObj,args.u))

# blacklist
if args.b is not None:
    L = removeBlacklistedText(args.b, L)

L.sort()
lu.fancyPrint(L)