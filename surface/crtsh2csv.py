from bs4 import BeautifulSoup
import sys
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu

# REPLACE <br> WITH SPACE

htmlFile = open(str(sys.argv[1]),'r')

soup = BeautifulSoup(htmlFile,'lxml')

tableBody = soup.find('table').find('tbody')

tr = tableBody.findAll('tr')

lines = ['"Common Name";"Matching Identities"']

for item in tr:
    tds = item.findAll('td')
    
    if (len(tds) > 0):
        firstValue = tds[4].get_text(separator='\n').strip()
        secondValue = tds[5].get_text(separator='\n').strip()
        line = '"{}";"{}"'.format(firstValue,secondValue)
        
        lines.append(line)


fm.listToFile(lines,str(sys.argv[2]))
    
    
    