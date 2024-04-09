import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import sys
import _common

# what should the script look for
_common.nmapFilters = ["rpc"]

if __name__ == '__main__':    

    if len(sys.argv) != 3:
        msg = "Usage: python3 {} <gnmap file> <output json file name>".format(sys.argv[0])
        np.infoPrint(msg)
        exit()

    out = []
    targets = _common.getTargets_generic(str(sys.argv[1]))
    for item in targets:

        # BUILD COMMAND HERE
        
        # scan
        com ='rpcinfo {}'.format(item['ip'])
        out.append(com)
    

    _common.makeJsonDictionary(out,str(sys.argv[2]))