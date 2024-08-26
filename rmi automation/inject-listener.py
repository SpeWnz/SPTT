'''
Purpose: 
single target
multiple gadgets

Use this to find how many deserializable gadgets a specific target is vulnerable to
'''

import _common
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import time
import os
import argparse
import sys

parser = argparse.ArgumentParser(description="rmi automation - inject listener")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGETS FILE"',type=str,required=True,help='Targets file containing IP or fqdn')
#REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PORT"',type=str,required=True,help='Target port')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--auto',action="store_true",help="Don't prompt the user to press enter to continue")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ==============================================================================================================

if __name__ == '__main__':
    
    np.infoPrint("Choose java version to use:")
    lu.fancyPrint(_common.CONFIG['java-executables'])
    _common.CHOSEN_JAVA_VERSION = int(input("> ")) -1

    targets = fm.fileToSimpleList(args.t)


    for t in targets:

            values = t.split(":")

            _common.RMGListen.listenerInject(values[0],values[1])
            
            if ('--auto' not in sys.argv):        
                np.infoPrint("Press enter to continue")
                input()
            else:
                time.sleep(1)
                np.infoPrint("Proceeding with next target")