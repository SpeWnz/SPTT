import json
import os
import sys
import ZHOR_Modules.nicePrints as np

from ZHOR_Modules.csvUtils import getTimeStamp

TARGET_FOLDER = None
OUTPUT_FOLDER = "dump_" + getTimeStamp()

def search(category: str,extList: list):
    print("\n")
    np.infoPrint("--------------------------------> " + key)
    
    for extension in extList:
        print("[>]",extension,"files: ",end='')

        outputFilePath = "{}/{}_files".format(OUTPUT_FOLDER,extension)

        com = 'find "{}" -type f -name "*.{}" > {}'.format(TARGET_FOLDER,extension,outputFilePath)
        os.system(com)

        try:
            lines = 0
            with open(outputFilePath,'r') as file:
                for l in file:
                    lines += 1

            print(lines)

        except:
            print("0")

        

_dict = json.load(open('categories.json','r'))

if __name__ == '__main__':

    if os.getuid() != 0:
        np.errorPrint("Script must be executed as sudo user")
        exit()

    TARGET_FOLDER = str(sys.argv[1])
    os.mkdir(OUTPUT_FOLDER)

    for key in _dict:
        search(key,_dict[key])
