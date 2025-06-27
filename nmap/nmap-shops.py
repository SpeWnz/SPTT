import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import argparse
import sqlite3
import sys

parser = argparse.ArgumentParser(description="NMAP SHOPS - Single Hosts Open Ports Scans")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-d',metavar='"DB"',type=str,required=True,help='Input database (can be an existing one)')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT"',type=str,required=True,help='Output file')

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('-f',action="store_true",help="Also include filtered ports")
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)




if __name__ == '__main__':
    conn = sqlite3.connect(args.d)
    cursor = conn.cursor()

    portState = None

    if args.f != None:
        portState = '!= "closed"'
    else:
        portState = '= "open"'

    hosts_wPorts = cursor.execute(f'''
    SELECT DISTINCT h.ip AS host, 
        GROUP_CONCAT(p.port, ',') AS open_ports
    FROM hosts h
    JOIN ports p ON h.id = p.host_id
    WHERE p.state {portState}
    GROUP BY h.id;
    ''').fetchall()

    lines = []
    for h in hosts_wPorts:

        _host              = h[0]
        _concatenatedPorts = h[1]

        # if you have a different nmap template to use, change it here
        output = f"nmap -vvv -sC -sV -n -Pn --open --max-retries 3 -p {_concatenatedPorts} -oA {_host}_sC-sV-openports {_host}"
        lines.append(output)
    

    cursor.close()

    fm.listToFile(lines,args.o)
