from bs4 import BeautifulSoup
import sys
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu


htmlFile = open(str(sys.argv[1]),'r')

soup = BeautifulSoup(htmlFile,'lxml')


divs = soup.findAll('div',class_='SearchResult result')



def parse_ipAndDomain(value):
    newValue = value.replace('(','').replace(')','').replace('   ','').replace('  ','').replace('\n','').replace('\r','').split(' ')

    newValue =  list(filter(lambda a: a != '', newValue))

    return newValue[0],newValue[1]

def parse_ports(value):
    newValue = value.replace('(','').replace(')','').replace('   ','').replace('  ','').replace('\n',' ').replace('\r','').split(' ')

    newValue =  list(filter(lambda a: a != '', newValue))

    newValue = lu.concatenate_elements(newValue,'\n')

    return newValue

def parse_info(value):
    newValue = value.replace('(','').replace(')','').replace('   ','').replace('  ','').replace('\n',' ').replace('\r','').replace('\t','')


    return newValue

lines = ["IP;DOMAIN;PORTS;INFO"]

for d in divs:

    # ip e dominio
    ip, domain = parse_ipAndDomain(d.find('a').text)

    # porte
    ports = parse_ports(d.find('div',class_='services-results').text)

    # info 
    info = parse_info(d.find('div',class_='').text)

    line = '"{}";"{}";"{}";"{}"'.format(ip,domain,ports,info)

    lines.append(line)

fm.listToFile(lines,str(sys.argv[2]))