# common functions
import json
import ZHOR_Modules.fileManager as fm

# what the script should look for
nmapFilters = []

def makeJsonDictionary(inputList: list,outputFileName: str):

    outDict = {}
    index = 1
    for com in inputList:
        outDict[index] = {'command':com,'state':'todo'}
        index += 1

    with open(outputFileName,'w') as f:
        json.dump(outDict,f)


# specific version for web services to filter http and https
def getTargets_http(gnmapFilePath: str):
    fileLines = fm.fileToSimpleList(gnmapFilePath)
    global nmapFilters
    output = []

    def filterInLine(filters:list, line: str):
        for f in filters:
            if f.lower() in line.lower():
                return True
            
        return False

    for line in fileLines:
        if filterInLine(nmapFilters,line):
            values = line.split('Ports:')
            
            ip = values[0].split(' ')[1]
            

            for item in values[1].split(','):
                if filterInLine(nmapFilters,item):

                    port = item.split('/')[0].replace(' ','') 
                    
                    d = {'ip':ip,
                         'port':port,
                         'ssl':("ssl") in item}
                    
                    
                    output.append(d)

    return output


# generic version with only ip and port
def getTargets_generic(gnmapFilePath: str):
    fileLines = fm.fileToSimpleList(gnmapFilePath)
    global nmapFilters
    output = []

    def filterInLine(filters:list, line: str):
        for f in filters:
            if f.lower() in line.lower():
                return True
            
        return False

    for line in fileLines:
        if filterInLine(nmapFilters,line):
            values = line.split('Ports:')
            
            ip = values[0].split(' ')[1]

            for item in values[1].split(','):
                if filterInLine(nmapFilters,item):

                    port = item.split('/')[0].replace(' ','') 
                    
                    d = {'ip':ip,'port':port}
                    
                    output.append(d)

    return output
