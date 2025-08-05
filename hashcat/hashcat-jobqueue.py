import argparse
import sys
import os
import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.timestampsUtils as tsu
import ZHOR_Modules.jsonUtils as jsu

parser = argparse.ArgumentParser(description="Hashcat \"Job Queue\" - a wrapper for hashcat to queue multiple jobs")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-m',metavar='"MODE"',type=int,required=True,help='Hashcat mode')
REQUIRED_ARGUMENTS.add_argument('-H',metavar='"HASHES"',type=str,required=True,help='Hashes file')
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TEMPLATE"',type=str,required=True,help='Job template to use (ex: example-template.json)')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT"',type=str,required=True,help='Output file')


# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)


def doJob(jobObject,hashcatMode,hashesFile,outputFile):
    if jobObject["mode"] == 0:
        hc_mode0(jobObject,hashcatMode,hashesFile,outputFile)

    if jobObject["mode"] == 3:
        hc_mode3(jobObject,hashcatMode,hashesFile,outputFile)
    


# wordlist attack
def hc_mode0(jobObject,hashcatMode,hashesFile,outputFile):
    session     = f'session_{tsu.getTimeStamp_iso8601()}'
    wordlist    = jobObject['wordlist']
    com = ''
    
    com += f'hashcat -a 0 -m {hashcatMode} "{hashesFile}" "{wordlist}"'

    # add rules if specified
    for r in jobObject['rules']:
        com += f' -r "{r}"'


    com += f' --session {session} -o "{outputFile}"'
    os.system(com)

# mask attack
def hc_mode3(jobObject,hashcatMode,hashesFile,outputFile):
    session         = f'session_{tsu.getTimeStamp_iso8601()}'
    maskParameters  = jobObject['parameters']
    com = ''
    
    com += f'hashcat -a 3 -m {hashcatMode} "{hashesFile}" "{maskParameters}"'

    com += f' --session {session} -o "{outputFile}"'
    os.system(com)

if __name__ == '__main__':
    jobs        = jsu.jsonFile2dict(args.t)
    hashcatMode = args.m
    hashesFile  = args.H
    outputFile  = args.o


    for job in jobs:
        doJob(job,hashcatMode,hashesFile,outputFile)