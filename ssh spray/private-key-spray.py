import paramiko
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import time
import os
import argparse
import sys
import ZHOR_Modules.logUtils as logu
from ZHOR_Modules.csvUtils import getTimeStamp

parser = argparse.ArgumentParser(description="SSH Private Key Spray")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGETS FILE"',type=str,required=True,help='Targets file containing IP or fqdn.')
REQUIRED_ARGUMENTS.add_argument('-d',metavar='"DELAY"',type=int,required=True,help='Delay between each request (in milliseconds)')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USER"',type=str,required=True,help='Username')
REQUIRED_ARGUMENTS.add_argument('-k',metavar='"KEY"',type=str,required=True,help='Path to id_rsa file')


# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ==========================================================================================================================================================

LOG_PATH = f"log_{getTimeStamp()}.txt"


def connect(target:str,user: str, key: str):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # default
    target_IP = target
    target_Port = 22

    # if port is specified
    if ':' in target:
        values = target.split(':')
        target_IP = values[0]
        target_Port = values[1]
    

    log_msg = f"{target_IP} {target_Port} {user} {key}"
    logu.logDebug(f"[DEBUG] testing > {log_msg}",fileName=LOG_PATH)

    try:
        ssh.connect(target_IP,username=user,key_filename=key,port=target_Port)
        ssh.close()

        logu.logInfo(f"[SUCCESS] {log_msg}",fileName=LOG_PATH)

    except Exception as e:
        logu.logDebug(f"[DEBUG] Login failed. Exception: {str(e)} --- {log_msg}",fileName=LOG_PATH)
        logu.logError(f"[FAILED] {log_msg}",fileName=LOG_PATH)


if __name__ == '__main__':
    
    targets = fm.fileToSimpleList(args.t)

    sleepTime = args.d/1000

    for t in targets:
        connect(t,args.u,args.k)
        time.sleep(sleepTime)
