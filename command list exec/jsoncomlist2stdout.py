# reads the json commands list and prints all commands
import json
import sys

jsonfile = str(sys.argv[1])
j = None
with open(jsonfile,'r') as f: j = json.load(f)

for id in j: print(j[id]['command'])