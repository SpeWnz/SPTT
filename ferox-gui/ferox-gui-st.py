'''
interactive version of feroxbuster.
Used for single-target scan.

NOTE: the usage of this script assumes the following
1. you have configured the ferox toml configuration file according to your needs
2. you have configured the config.json for this script to accomodate your needs and preferences
    i.e. ---> correct wordlists, correct output folder

'''
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.jsonUtils as jsu
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.osUtils as osu
import readline
import os

def getOutputFileName(inputStr: str):
    return inputStr.replace(".","-").replace(":",'-').replace("/",'-')


CONFIG = jsu.loadConfig()
HEADERS = fm.fileToSimpleList('headers.txt')

wordlistIndex = None
targetURL = None


np.infoPrint("Select worldlist:")

for i in range(0,len(CONFIG['wordlists'])):
    print(i+1,". ",CONFIG['wordlists'][i]['label'],sep='')


wordlistIndex = int(input("> ")) - 1

np.infoPrint("Insert target: ")
targetURL = str(input("> "))

outputFile = getOutputFileName(targetURL)

com = 'feroxbuster -w "{}" --url "{}" -o "{}/{}"'.format(
    CONFIG['wordlists'][wordlistIndex]['path'],
    targetURL,
    CONFIG['outputFolder'],
    outputFile
)

# append headers, if there are any
if len(HEADERS) > 0:
    for h in HEADERS:
        com += f" -H '{h}'"

print("Please review the command before proceeding\n\n")
print(com)
print("\n")
osu.pressEnterToContinue()
os.system(com)
