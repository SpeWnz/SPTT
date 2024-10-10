import time
import sys
import ZHOR_Modules.nicePrints as np

import os
import argparse
import sys

parser = argparse.ArgumentParser(description="<<Semi-Persistent>> resolv.conf")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-f',metavar='"FILE"',type=str,required=True,help='Custom resolv.conf file')
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TIME"',type=int,required=True,help='Time (in seconds) between each "re-install" of the custom resolv.conf')

# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

# ==========================================================================================================================================


def replace(customResolvConfPath: str):
    com = f'cp "{customResolvConfPath}" /etc/resolv.conf'

    try:
        np.debugPrint(com)
        os.system(com)
        np.infoPrint("Custom reslov.conf copied!")
    except Exception as e:
        np.errorPrint("Exception:")
        print(e)

if __name__ == '__main__':

    path = args.f
    sleepTime = args.t

    if os.getuid() != 0:
        np.errorPrint("Script must be executed as root or as user with elevated privileges")
        exit()

    np.infoPrint(f'The custom resolv.conf file will be re-installed every {str(sleepTime)} seconds. Press ctrl+c to exit at any time.')

    while True:
        replace(path)
        time.sleep(sleepTime)

