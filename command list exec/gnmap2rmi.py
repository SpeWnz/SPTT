import ZHOR_Modules.fileManager as fm
import ZHOR_Modules.nicePrints as np
import sys
import _common

# what should the script look for
_common.nmapFilters = ["java-rmi"]

# path of the executable jar (for remote-method-guesser)
# https://github.com/qtc-de/remote-method-guesser
jar_location = "INSERT PATH HERE"

if __name__ == '__main__':    

    if len(sys.argv) != 3:
        msg = "Usage: python3 {} <gnmap file> <output json file name>".format(sys.argv[0])
        np.infoPrint(msg)
        exit()

    out = []
    targets = _common.getTargets_generic(str(sys.argv[1]))
    for item in targets:

        # BUILD COMMAND HERE

        # example command:
        # rmg scan IP
        # rmg enum IP PORT
        
        # scan
        com = 'java -jar {} scan {}'.format(jar_location, item['ip'])
        out.append(com)

        # enum
        com = 'java -jar {} enum {} {}'.format(jar_location,item['ip'],item['port'])
        out.append(com)
    

    _common.makeJsonDictionary(out,str(sys.argv[2]))