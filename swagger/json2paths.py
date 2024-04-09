'''
Given a swagger.json file, extract all the paths and print them
'''

import sys
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.jsonUtils as jsu

def printPaths(jsonPath: str):
    jsonObject = jsu.jsonFile2dict(jsonPath)

    paths = jsonObject['paths']

    for p in paths:
        print(p)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        msg = "Usage: python3 {} <swagger.json file>".format(sys.argv[0])
        np.infoPrint(msg)
        exit()
    
    jsonPath = str(sys.argv[1])

    printPaths(jsonPath)