import jsbeautifier
import sys
import os

files = sys.argv[1:]


def unminifyFile(inputFile: str):
    res = jsbeautifier.beautify_file(inputFile)
                
    outputPath = inputFile + "_UNMINIFIED.js"
    with open(outputPath,'w') as f:
        f.write(res)


for f in files:
    print("unminifying",f,"...")
    path = os.path.abspath(f)
    unminifyFile(f)
