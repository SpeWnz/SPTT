import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import argparse
import sqlite3
import sys

parser = argparse.ArgumentParser(description="NMAP Service Group By")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT"',type=str,required=True,help='Output folder')
REQUIRED_ARGUMENTS.add_argument('-d',metavar='"DB"',type=str,required=True,help='Output database (can be an existing one)')

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

    services = cursor.execute(f'''
    select DISTINCT ports.service_name
    from ports
    where ports.state {portState}
    ''').fetchall()

    for service in services:
        _s = service[0]

        machines = cursor.execute(f'''
            select DISTINCT hosts.ip, ports.port
            from hosts, ports
            where hosts.id = ports.host_id
            and (ports.service_name like "%{_s}%")
            and ports.state {portState}
            order by hosts.target_group
                                  ''')
        
        outputLines = []

        for machine in machines:
            outputLines.append(machine[0] + ':' + machine[1])


        outputPath = f'{args.o}/{_s}.txt'
        fm.listToFile(outputLines,outputPath)
    

    cursor.close()
