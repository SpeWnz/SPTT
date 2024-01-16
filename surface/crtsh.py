import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import sys
import ZHOR_Modules.fileManager as fm
import json

# performs query and returns json object
def query(inputString: str):
    HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    URL = "https://crt.sh/?q={}&output=json".format(inputString)
    r = requests.get(url=URL,verify=False,headers=HEADERS)

    jsonObject = json.loads(r.text)
    return jsonObject

# handles the \n problem
def fixNewLines(inputValue):

    if '\n' in inputValue:
        return inputValue.split('\n')
    else:
        return [inputValue]


# returns the list of domains from the json object
def getDomains(inputJsonObject):
    domains = []
    
    # iterate through results
    for item in inputJsonObject:

        #common name        
        values = fixNewLines(item['common_name'])
        for v in values:
            domains.append(v)
        
        # name value
        values = fixNewLines(item['name_value'])
        for v in values:
            domains.append(v)

    # removes duplicates
    domains = list(dict.fromkeys(domains))

    # remove entries with *
    output = []
    for item in domains:
        if '*' in item:
            pass
        else:
            output.append(item)

    return output




if __name__ == '__main__':
    userInput = str(sys.argv[1])

    print("Querying ...")
    j = query(userInput)
    d = getDomains(j)

    fileName = userInput + "_results.txt"
    print("Writing results to",fileName)
    fm.listToFile(d,fileName)    
