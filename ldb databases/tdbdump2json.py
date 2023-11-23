import json
import shutil
import sys
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np

if (len(sys.argv) < 3):
    print("Usage:",sys.argv[0],"<tdb dump file> <json output path>")
    exit()

tdb_executable = shutil.which('tdbdump')
if tdb_executable:
    pass
else:
    np.errorPrint("tdbdump was not found on your system. Please install it first.")
    exit()


jsonObject = []
lines = fm.fileToSimpleList(str(sys.argv[1]))

keys = []
values = []

for l in lines:

    if l == '{' or l == '}':
        pass
    else:
        if 'key(' in l:
            _v = l.split(') = ')[1][1:-1]
            keys.append(_v)

        if 'data(' in l:
            _v = l.split(') = ')[1][1:-1]
            values.append(_v)
        

if len(keys) == len(values):
    pass
else:
    print("Error: amount mismatch between keys and values")
    print(len(keys),"keys and",len(values),"values")


for i in range(0,len(keys)):
    d = {
        'key':keys[i],
        'value':values[i]
        }
    
    jsonObject.append(d)

jsonFile = str(sys.argv[2])
with open(jsonFile,'w') as f:
    json.dump(jsonObject,f)