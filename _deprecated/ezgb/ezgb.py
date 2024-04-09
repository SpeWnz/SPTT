import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.argparseUtils as apu
import sys
import json
import os
import threading
import argparse


__VERSION = "v260723"

parser = argparse.ArgumentParser(description="EZGB - easy gobuster " + __VERSION)
REQUIRED_ARGUMENTS = parser.add_argument_group("Argomenti necessari")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Argomenti opzionali")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-T',metavar='"TARGET"',type=str,required=True,help='URL / TARGET IP (without http:// or https://)')
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TEMPLATE"',type=str,required=True,help='JSON template')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT FOLDER"',type=str,required=True,help='Path of the folder to store the output ')

# Argomenti opzionali
#REQUIRED_ARGUMENTS.add_argument('--method',metavar='"REQUEST METHOD"',type=int,help='0: GET, 1: POST, 2: PUT')
OPTIONAL_ARGUMENTS.add_argument('--exclude',action="store_true",help="(interactive) prompt status codes to exclude (MUTEX with --exclude-range)")
OPTIONAL_ARGUMENTS.add_argument('--exclude-range',metavar='"LENGTH RANGE"',type=str,help='Specifies a range of response content length to exclude, e.g. 6100-6300 (MUTEX with --exclude)')
OPTIONAL_ARGUMENTS.add_argument('--https',action="store_true",help="Prepend https:// to the target, instead of http://")
OPTIONAL_ARGUMENTS.add_argument('--cookie-file',metavar='"COOKIE FILE"',type=str,help='Path of a txt file containing the cookies string')
OPTIONAL_ARGUMENTS.add_argument('--print',action="store_true",help="Prints out the constructed gobuster command instead of executing it.")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)

if (apu.checkMutExArgs(sys.argv,['--exclude','--exclude-range']) is True):
    exit()

# ===============================================================================================

JSON_DATA = json.load(open(args.t,'r'))

TARGET_IP = args.T
OUTPUT_FOLDER = args.o



# exclude status codes interactively
excludeStatusCodes=""
if "--exclude" in sys.argv:
    np.infoPrint("Insert status(es) to exclude (Syntax: num,num,num,...)")
    s = str(input("> "))
    excludeStatusCodes = ' -b "404,{}"'.format(s)

excludeLengths = ""
if "--exclude-range" in sys.argv:

    values = args.exclude_range.split('-')
    parameter = ' --exclude-length '
    startingIndex = int(values[0])
    endingIndex = int(values[1])


    for i in range(startingIndex,endingIndex+1,):
        parameter += str(i) + ","
        np.debugPrint(parameter)

    # remove ending comma
    excludeLengths = parameter[:-1]



# fix path
if OUTPUT_FOLDER[-1] != "/":
    OUTPUT_FOLDER += "/"

# prepend 
mode = "http"
if "--https" in sys.argv:
    mode = "https"

outputFileName = OUTPUT_FOLDER + TARGET_IP.replace('.','-').replace(':','---').replace("/","__")


command = ""
command += "gobuster " + JSON_DATA['gobuster-mode']
command += ' -u "{}://{}"'.format(mode,TARGET_IP)
command += ' -t ' + str(JSON_DATA['threads'])
command += ' -w "{}"'.format(JSON_DATA['wordlist'])
command += ' -k'
command += ' --output "{}"'.format(outputFileName)

if (JSON_DATA['random-agent'] is True):
    command += ' --random-agent'

command += ' --timeout {}s'.format(str(JSON_DATA['timeout']))
command += ' --delay {}s'.format(str(JSON_DATA['delay']))
command += excludeStatusCodes
command += excludeLengths


np.debugPrint(command)

if ('--print' in sys.argv):
    np.infoPrint("Constructed command:\n" + command)
else:
    os.system(command)

