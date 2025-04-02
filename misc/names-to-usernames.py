# small script to convert a list of employee names to a list of possible usernames and nicknames following popular name/surname formats.
# useful in context where usernames have to be enumerated.

import sys
import ZHOR_Modules.fileManager as fm

if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <input list> <output list>")
    print(f"Example: python3 {sys.argv[0]} names.txt nicknames.txt")
    exit()


names = fm.fileToSimpleList(sys.argv[1])
outputList = []

for item in names:
    
    values = item.split(' ')

    # "first last" and "FIRST LAST"
    outputList.append(item.lower())
    outputList.append(item.upper())

    # "first.last" and "FIRST.LAST"
    outputList.append(item.replace(" ",'.').lower())
    outputList.append(item.replace(" ",'.').upper())    

    # "first-last" and "FIRST-LAST"
    outputList.append(item.replace(" ",'-').lower())
    outputList.append(item.replace(" ",'-').upper())

    # "first_last" and "FIRST_LAST"
    outputList.append(item.replace(" ",'_').lower())
    outputList.append(item.replace(" ",'_').upper())


    # "flast" or "fmlast"
    _toAppend = ""
    for i in range(0,len(values) - 1):
        _toAppend += values[i][0]

    _toAppend += values[-1]
    outputList.append(_toAppend)

    # "FLast" or "FMLast"
    _toAppend = ""
    for i in range(0,len(values) - 1):
        _toAppend += values[i][0].upper()

    _last = values[-1][0].upper() + ''.join(values[-1][1:])
    _toAppend += _last
    outputList.append(_toAppend)

    # "f.last" or "f.m.last"
    _toAppend = ""
    for i in range(0,len(values) - 1):
        _toAppend += values[i][0] + "."


    _toAppend += values[-1]
    outputList.append(_toAppend)

    # "f_last" or "f_m_last"
    _toAppend = ""
    for i in range(0,len(values) - 1):
        _toAppend += values[i][0] + "_"


    _toAppend += values[-1]
    outputList.append(_toAppend)

    # "f-last" or "f-m-last"
    _toAppend = ""
    for i in range(0,len(values) - 1):
        _toAppend += values[i][0] + "-"


    _toAppend += values[-1]
    outputList.append(_toAppend)

    

fm.listToFile(outputList,sys.argv[2])
