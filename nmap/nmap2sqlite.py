'''
Slightly modified and improved version of the original nmap-to-sqlite.py from "hackertarget":
https://github.com/hackertarget/nmap-did-what

The resulting DB file can be used with manual queries in a sqlite proejct, or in a data visualization toool
such as grafana (as the original author intended).


Original description:
Script to parse nmap xml files and populate an SQLite DB
use with Grafana Dashboard - https://hackertarget.com/nmap-dashboard-with-grafana/

'''

from datetime import datetime
import argparse
import sys
import sqlite3
import xml.etree.ElementTree as ET
import ZHOR_Modules.nicePrints as np


def parse_nmap_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    nmap_version = root.get('version', '')
    command_line = root.get('args', '')

    scan_start_time = root.get('start')
    if scan_start_time is not None:
        # timestamps set to match native grafana format
        scan_start_timestamp = int(scan_start_time) * 1000

    elapsed_time = ''
    elapsed_time_elem = root.find('runstats/finished')
    if elapsed_time_elem is not None:
        elapsed_time = elapsed_time_elem.get('elapsed')


    total_hosts = 0
    total_open_ports = 0

    hosts = []
    for host in root.findall('host'):
        total_hosts += 1
        ip = host.find('address').get('addr', '')
        
        hostname_elems = host.findall('hostnames/hostname')
        hostname = hostname_elems[0].get('name', '') if hostname_elems else ''
        
        os = 'Unknown'
        os_element = host.find('os')
        if os_element:
            os_match = os_element.find('osmatch')
            os = os_match.get('name', 'Unknown') if os_match else 'Unknown'
        
        ports_tested = 0
        ports_open = 0
        ports_closed = 0
        ports_filtered = 0

        ports = []
        ports_element = host.find('ports')
        if ports_element is not None:
            for port in ports_element.findall('port'):
                port_id = port.get('portid')
                protocol = port.get('protocol')
                state = port.find('state').get('state')
                if state == 'open':
                    ports_open += 1
                    total_open_ports += 1
                elif state == 'closed':
                    ports_closed += 1
                elif state == 'filtered':
                    ports_filtered += 1

                service = port.find('service')

                service_name = service.get('name', None)       if (service != None) else None
                service_product = service.get('product', None) if (service != None) else None
                service_version = service.get('version', None) if (service != None) else None
                service_ostype = service.get('ostype', None)   if (service != None) else None
                service_info = (service_product if (service_product != None) else '') + (' ' + service_version if (service_version != None) else '')
                http_title = None
                ssl_common_name = None
                ssl_issuer = None

                scripts = port.findall('script')
                for script in scripts:
                    if script.get('id') == 'http-title':
                        http_title = script.get('output')
                    elif script.get('id') == 'ssl-cert':
                        for table in script.findall('table'):
                            if table.get('key') == 'subject':
                                cn_elem = table.find("elem[@key='commonName']")
                                if cn_elem is not None:
                                    ssl_common_name = cn_elem.text
                            elif table.get('key') == 'issuer':
                                issuer_elems = {elem.get('key'): elem.text for elem in table.findall('elem')}
                                if 'commonName' in issuer_elems:
                                    ssl_issuer = f"{issuer_elems.get('commonName')} {issuer_elems.get('organizationName', '')}".strip()

                if service_ostype and os == 'Unknown':
                    os = service_ostype
                
                ports.append({
                    'port': port_id,
                    'protocol': protocol,
                    'state': state,
                    'service_name': service_name,
                    'service_info': service_info,
                    'http_title': http_title,
                    'ssl_common_name': ssl_common_name,
                    'ssl_issuer': ssl_issuer
                })

            extraports = ports_element.find('extraports')
            
            if extraports != None:                
                extraports_count = int(extraports.get('count', '0'))
                extraports_state = extraports.get('state', '')
                if extraports_state == 'closed':
                    ports_closed += extraports_count
                elif extraports_state == 'filtered':
                    ports_filtered += extraports_count
                ports_tested += extraports_count

        host_start_time = host.get('starttime')
        host_end_time = host.get('endtime')
        start_timestamp = int(host_start_time) * 1000 if host_start_time else None
        end_timestamp = int(host_end_time) * 1000 if host_end_time else None

        hosts.append({
            'ip': ip,
            'hostname': hostname,
            'os': os,
            'ports_tested': ports_tested,
            'ports_open': ports_open,
            'ports_closed': ports_closed,
            'ports_filtered': ports_filtered,
            'start_time': start_timestamp,
            'end_time': end_timestamp,
            'ports': ports
        })

    scan = {
        'nmap_version': nmap_version,
        'command_line': command_line,
        'start_time': scan_start_time,
        'elapsed_time': elapsed_time,
        'total_hosts': total_hosts,
        'total_open_ports': total_open_ports
    }

    return scan, hosts

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # scans table
    c.execute('''CREATE TABLE IF NOT EXISTS scans
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nmap_version TEXT,
                 command_line TEXT,
                 start_time INTEGER,
                 elapsed_time TEXT,
                 total_hosts INTEGER,
                 total_open_ports INTEGER)''')
    
    # hosts table
    c.execute('''CREATE TABLE IF NOT EXISTS hosts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 scan_id INTEGER,
                 target_group TEXT,
                 ip TEXT,
                 hostname TEXT,
                 os TEXT,
                 ports_tested INTEGER,
                 ports_open INTEGER,
                 ports_closed INTEGER,
                 ports_filtered INTEGER,
                 start_time INTEGER,
                 end_time INTEGER,
                 FOREIGN KEY (scan_id) REFERENCES scans (id))''')

    # ports table
    c.execute('''CREATE TABLE IF NOT EXISTS ports
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 scan_id INTEGER,
                 host_id INTEGER,
                 port TEXT,
                 protocol TEXT,
                 state TEXT,
                 service_name TEXT,
                 service_info TEXT,
                 http_title TEXT,
                 ssl_common_name TEXT,
                 ssl_issuer TEXT,
                 FOREIGN KEY (scan_id) REFERENCES scans (id),
                 FOREIGN KEY (host_id) REFERENCES hosts (id))''')
    
    conn.commit()
    return conn

def insert_data(conn, scan, hosts, targetGroup):
    c = conn.cursor()
    
    # scan data
    c.execute("INSERT INTO scans (nmap_version, command_line, start_time, elapsed_time, total_hosts, total_open_ports) VALUES (?, ?, ?, ?, ?, ?)",
              (scan['nmap_version'], scan['command_line'], scan['start_time'], scan['elapsed_time'], scan['total_hosts'], scan['total_open_ports']))
    scan_id = c.lastrowid
    
    # hosts data
    for host in hosts:
        c.execute("INSERT INTO hosts (scan_id, target_group, ip, hostname, os, ports_tested, ports_open, ports_closed, ports_filtered, start_time, end_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (scan_id, targetGroup, host['ip'], host['hostname'], host['os'], host['ports_tested'], host['ports_open'], host['ports_closed'], host['ports_filtered'], host['start_time'], host['end_time']))
        host_id = c.lastrowid
        
        for port in host['ports']:
            c.execute("INSERT INTO ports (scan_id, host_id, port, protocol, state, service_name, service_info, http_title, ssl_common_name, ssl_issuer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (scan_id, host_id, port['port'], port['protocol'], port['state'], port['service_name'], port['service_info'], port['http_title'], port['ssl_common_name'], port['ssl_issuer']))
     
    conn.commit()


parser = argparse.ArgumentParser(description="NMAP to SQLite DB")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Required arguments
REQUIRED_ARGUMENTS.add_argument('-x',metavar='"XML"',type=str,required=True,help='Nmap XML file')
REQUIRED_ARGUMENTS.add_argument('-t',metavar='"TARGET GROUP"',type=str,required=True,help='Name of the target group the scan belongs to')
REQUIRED_ARGUMENTS.add_argument('-d',metavar='"DB"',type=str,required=True,help='Output database (can be an existing one)')

# Optional arguments
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ('--debug' in sys.argv)


if __name__ == '__main__':

    xml_file    = args.x
    db_name     = args.d
    targetGroup = args.t

    scan, hosts = parse_nmap_xml(xml_file)
    conn = create_database(db_name)
    insert_data(conn, scan, hosts, targetGroup)

    conn.close()