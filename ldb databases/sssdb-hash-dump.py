# extract hashes from sssdb database files
# reference here:
# https://labs.portcullis.co.uk/download/eu-18-Wadhwa-Brown-Where-2-worlds-collide-Bringing-Mimikatz-et-al-to-UNIX.pdf

import ZHOR_Modules.nicePrints as np
import re
import sys
import shutil
import os

if (len(sys.argv) < 2):
    print("Usage:",sys.argv[0],"<ldb file>")
    exit()

tdb_executable = shutil.which('tdbdump')
if tdb_executable:
    pass
else:
    np.errorPrint("tdbdump was not found on your system. Please install it first.")
    exit()


temp = "____temp"
file = str(sys.argv[1])

os.system("tdbdump \"{}\" > \"{}\"".format(file,temp))

pattern1 = r'\$6\$.+\\'
#pattern2 = r'\$6\$.{103}'
#pattern3 = r'\$6\$.{86,103}'

s  = open(temp,'r').read()

matches = re.findall(pattern1,s)

if len(matches) == 0:
    print("No hashes found!")
else: 
    for m in matches:
        print(m.split('\\00')[0])

os.system("rm {}".format(temp))