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
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)




if __name__ == '__main__':
    conn = sqlite3.connect(args.d)
    cursor = conn.cursor()

    hosts_wPorts = cursor.execute('''
    SELECT DISTINCT h.ip AS host, 
        GROUP_CONCAT(p.port, ',') AS open_ports
    FROM hosts h
    JOIN ports p ON h.id = p.host_id
    WHERE p.state = 'open'
    GROUP BY h.id;
    ''').fetchall()

    lines = []
    for h in hosts_wPorts:
        output = f"nmap -vvv -sC -sV -n -Pn --open --max-retries 3 -p {h[1]} -oA {h[0]}_sC-sV-openports {h[0]}"
        lines.append(output)
    

    cursor.close()

    fm.listToFile(lines,args.o)
