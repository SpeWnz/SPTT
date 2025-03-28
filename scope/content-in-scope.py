import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu
import argparse
import sys

#__VERSION = "v300623"

parser = argparse.ArgumentParser(description="Content In scope")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"INPUT"',type=str,required=True,help='IPs to find in the compare file')
REQUIRED_ARGUMENTS.add_argument('-c',metavar='"COMPARE"',type=str,required=True,help='Compare file')



# Argomenti opzionali
#REQUIRED_ARGUMENTS.add_argument('--method',metavar='"REQUEST METHOD"',type=int,help='0: GET, 1: POST, 2: PUT')
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = not ("--debug" in sys.argv)

if __name__ == '__main__':
    scope = fm.fileToSimpleList(args.i)
    compare = fm.fileToSimpleList(args.c)


    for target in scope:

        for line in compare:
            if target in line:
                print(target)