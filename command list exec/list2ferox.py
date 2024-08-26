import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import sys
import _common

# what should the script look for
_common.nmapFilters = ["http","https"]

def getOutputFileName(inputStr: str):
    return inputStr.replace(".","-").replace(":",'-').replace("/",'-')



if __name__ == '__main__':    

    if len(sys.argv) != 3:
        msg = "Usage: python3 {} <http/https targets list> <output json file name>".format(sys.argv[0])
        np.infoPrint(msg)
        exit()

    out = []
    targets = fm.fileToSimpleList(str(sys.argv[1]))
    
    for target in targets:
        
        target_formatted = getOutputFileName(target)
        com = 'feroxbuster -w "YOUR/WORDLIST/HERE.txt" --url "{}" -o "YOUR/OUTPUT/FOLDER/HERE/{}"'.format(
            target,
            target_formatted
            )
        
        
        
        out.append(com)
    

    _common.makeJsonDictionary(out,str(sys.argv[2]))

    
