'''
PURPOSE:
we have a list of IP addresses, that's our scope.
We found some domains, subdomains, possibly associated/related with the scope.
How many of those domains are actually in our scope?
'''

import ZHOR_Modules.nicePrints as np
import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.listUtils as lu
import ZHOR_Modules.osUtils as osu
import argparse
import sys
import pandas

parser = argparse.ArgumentParser(description="Domains & Subdomains In Scope")
REQUIRED_ARGUMENTS = parser.add_argument_group("Required arguments")
OPTIONAL_ARGUMENTS = parser.add_argument_group("Optional arguments")

# Argomenti necessari
REQUIRED_ARGUMENTS.add_argument('-s',metavar='"SCOPE"',type=str,required=True,help='IPs in scope')
REQUIRED_ARGUMENTS.add_argument('-d',metavar='"DOMAINS"',type=str,required=True,help='Domains list')
REQUIRED_ARGUMENTS.add_argument('-o',metavar='"OUTPUT"',type=str,required=True,help='Output csv file path')



# Argomenti opzionali
OPTIONAL_ARGUMENTS.add_argument('--debug',action="store_true",help="Debug mode")

args = parser.parse_args()

np.DEBUG = ("--debug" in sys.argv)
SCOPE_ONLY = '--so' in sys.argv

def status(domain: str):

    com = f"nslookup {domain}"
    stdout, stderr = osu.commandResult(com)

    # not found
    if "server can't find" in stdout:
        #print("not found")
        return None
    
    # found ---> parse IPs
    lines = stdout.split("\n")
    
    IPs = []
    for l in lines:
        if "Address:" in l:
            IPs.append(l.split(':')[1].strip())

    # there might be multiple ip addresses. Ignore the first one
    return IPs[1:]

def inScope(targetIPs: list, obtainedIPs: list):
    
    for item in targetIPs:
        if item in obtainedIPs:
            return True
        
    return False


if __name__ == '__main__':
    scope = fm.fileToSimpleList(args.s)
    domains = fm.fileToSimpleList(args.d)

    df = pandas.DataFrame(columns=["Subdomain","IP(s)","Scope Result"])

    np.infoPrint("Obtaining info...")
    for d in domains:
        nsLookpResult = status(d)
        scopeResult = ""
        
        if nsLookpResult == None:
            scopeResult = "NOT FOUND"
            msg = f"NOT FOUND \r\t\t\t{d}"
            np.debugPrint(msg)

        else:

            if inScope(scope,nsLookpResult):
                scopeResult = "IN SCOPE"
                msg = f"IN SCOPE \r\t\t\t{d} \t{str(nsLookpResult)}"
                np.debugPrint(msg)

            else:
                scopeResult = "OUT OF SCOPE"
                msg = f"OUT OF SCOPE \r\t\t\t{d} \t{str(nsLookpResult)}"
                np.debugPrint(msg)

        row = {"Subdomain":d, "IP(s)":str(nsLookpResult),"Scope Result":scopeResult}
        df = df._append(row,ignore_index=True)

    
    df.to_csv(args.o,index=False)
            

