import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import argparse
import sys

__VERSION = "v221123"

parser = argparse.ArgumentParser(description="GNMAP format parser " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-i',metavar='"FILE"',type=str,required=True,help='GNMAP FILE')
REQUIRED_ARGUMENTS.add_argument('-f',metavar='"FILTERS"',type=str,required=True,help='One or more quoted words separated by a comma. Example: "ftp,sftp"')
# Argomenti opzionali
REQUIRED_ARGUMENTS.add_argument('-m',metavar='"PRINT METHOD"',type=int,help='1:Fancy, 2:List')
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)

# ================================================================================================================================================

fileLines = fm.fileToSimpleList(str(args.i))
nmapFilters = args.f.split(',')
MODE = 1

if '-m' in sys.argv:
    MODE = int(args.m)

# true if filter appears in line
# false otherwise
def filterInLine(filters:list, line: str):
    for f in filters:
        if f.lower() in line.lower():
            return True
        
    return False

def fancy_print():
    for line in fileLines:
        if filterInLine(nmapFilters,line):
            values = line.split('Ports:')
            
            print("\n\n")
            np.infoPrint(values[0])

            for item in values[1].split(','):
                if filterInLine(nmapFilters,item):
                    print("[ ]",item)

def list_print():
    for line in fileLines:
        if filterInLine(nmapFilters,line):
            values = line.split('Ports:')
            
            host = values[0].split(': ')[1].split(' (')[0] 

            for item in values[1].split(','):
                if filterInLine(nmapFilters,item):
                    port = item.split('/')[0][1:]
                    print(host,port,sep=':')

if __name__ == '__main__':

    if MODE == 1:
        fancy_print()
        exit()

    if MODE == 2:
        list_print()
        exit()


    np.errorPrint("Uknown print mode.")
    exit()


    