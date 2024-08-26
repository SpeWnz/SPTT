'''
Purpose:
execute "rmg enum" on multiple ip addresses

run this by issuing the following command:
python3 -u script.py 2>&1 | tee rmg-enum.output
'''

import _common
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import time
import os
import argparse
import sys

SEPARATOR = "\n\n============================================================================\n\n"

if __name__ == '__main__':

    if len(sys.argv) != 2:
        np.infoPrint("Usage: python3 -u {} <targets file> 2>&1 | tee rmg-enum.output".format(sys.argv[0]))
        exit()

    targets = fm.fileToSimpleList(str(sys.argv[1]))

    for t in targets:
        values = t.split(":")
        ip = values[0]
        port = values[1]

        com = "java -jar {} enum {} {}".format(_common.CONFIG["rmg-executable-location"],ip,port)
        np.infoPrint("{} TARGET --- {}:{}".format(SEPARATOR,ip,port))
        os.system(com)
        

