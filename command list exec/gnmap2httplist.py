import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import sys
import _common

# what should the script look for
_common.nmapFilters = ["http","https"]


if __name__ == '__main__':    

    if len(sys.argv) != 2:
        msg = "Usage: python3 {} <gnmap file>".format(sys.argv[0])
        np.infoPrint(msg)
        exit()

    
    targets = _common.getTargets_http(str(sys.argv[1]))
    for item in targets:

        target = ""
        if (item['ssl']):
            target = "https://"
        else:
            target = "http://"
        
        target += '{}:{}'.format(item['ip'],item['port'])

        print(target)
        
        

        


    
