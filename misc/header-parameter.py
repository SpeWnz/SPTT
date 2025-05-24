# small script to convert a headers.txt file into a line of commandline arguments.
# useful for tools that do not support a headers.txt file but feature headers arguments


import sys
import ZHOR_Modules.requestUtils as requ

if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <headers file> <headers prefix>")
    print(f"Example: python3 {sys.argv[0]} headers.txt \"-H\"")
    exit()

headers = requ.requestFile2Headers(sys.argv[1])
prefix = sys.argv[2]

for item in headers:
    print(f"{prefix} '{item}: {headers[item]}'",sep=' ',end=' ')