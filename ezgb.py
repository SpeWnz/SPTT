import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.listUtils as lu
import sys
import json
import os
import threading



np.DEBUG = True

if ((len(sys.argv) < 3) or ('-h' in sys.argv)):
    np.infoPrint("Utilizzo: python3 ezgb.py <target> <output folder> [exclude] [https] [wildcard] [api] [auth] [wordlist]")
    exit()


TARGET_IP = str(sys.argv[1])
OUTPUT_FOLDER = str(sys.argv[2])

# se è specificata una porta
TARGET_PORT = "80"
if ":" in TARGET_IP:
    TARGET_IP.split(':')[1]

# se voglio escludere uno o più status codes
excludeStatusCodes=""
if "exclude" in sys.argv:
    np.infoPrint("Inserire gli status code da escludere (Sintassi: num,num,num,...)")
    s = str(input("> "))
    excludeStatusCodes = ' -b "404,{}"'.format(s)


#fix path
if OUTPUT_FOLDER[-1] != "/":
    OUTPUT_FOLDER += "/"

# se voglio enumerare api invece che path di cartelle/file
if ("api" in sys.argv):
    wordlist = "/home/cyberoot/Documents/sharedData/Wordlist/SecLists/Discovery/Web-Content/api/all.txt"
else:
    wordlist = "/home/cyberoot/Documents/sharedData/Wordlist/SecLists/Discovery/Web-Content/directory-list-2.3-big.txt"

if ("wordlist" in sys.argv):
    wordlist = str(input("Wordlist\n>"))


wildcard = ""
if "wildcard" in sys.argv:
    wildcard = " --wildcard"

mode = "http"
if "https" in sys.argv:
    mode = "https"

outputFileName = OUTPUT_FOLDER + TARGET_IP.replace('.','-').replace(':','---').replace("/","__")


threadCount = str(input("Threads \n> "))

# se serve basic auth
command = ""
if ("auth" in sys.argv):
    np.infoPrint("Credenziali Basic Auth")

    user = str(input("Nome utente \n> "))
    passwd = str(input("Password \n> "))
    command = 'gobuster dir -u "{}://{}" -t {} -w "{}" -k{} --output "{}"{} -U "{}" -P "{}" --random-agent --timeout 3s --delay 0.5s'.format(mode,TARGET_IP,threadCount,wordlist,wildcard,outputFileName,excludeStatusCodes,user,passwd)
else:
    command = 'gobuster dir -u "{}://{}" -t {} -w "{}" -k{} --output "{}"{} --random-agent --timeout 3s --delay 0.5s'.format(mode,TARGET_IP,threadCount,wordlist,wildcard,outputFileName,excludeStatusCodes)


np.debugPrint(command)
os.system(command)
